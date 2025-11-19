import os
from typing import List, Dict
from io import BytesIO

from PyPDF2 import PdfReader
from docx import Document

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

VECTORSTORE_DIR = "data/faiss_langchain"

def _get_embeddings() -> OpenAIEmbeddings:
    model = (
        os.getenv("EMBEDDING_MODEL")
        or os.getenv("OPENAI_EMBEDDING_MODEL")
        or "text-embedding-3-small"
    )
    return OpenAIEmbeddings(model=model)

def _load_vectorstore():
    if not os.path.isdir(VECTORSTORE_DIR):
        return None
    try:
        vs = FAISS.load_local(
            VECTORSTORE_DIR,
            _get_embeddings(),
            allow_dangerous_deserialization=True,
        )
        return vs
    except Exception:
        return None

def _save_vectorstore(vs: FAISS):
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    vs.save_local(VECTORSTORE_DIR)

def clear_index():
    if os.path.isdir(VECTORSTORE_DIR):
        for root, _, files in os.walk(VECTORSTORE_DIR, topdown=False):
            for name in files:
                try:
                    os.remove(os.path.join(root, name))
                except OSError:
                    pass
            try:
                os.rmdir(root)
            except OSError:
                pass

def extract_text(file_bytes: bytes, filename: str) -> str:
    name = filename.lower()
    try:
        if name.endswith(".pdf"):
            reader = PdfReader(BytesIO(file_bytes))
            if reader.is_encrypted:
                try:
                    reader.decrypt("")
                except Exception:
                    pass
            parts = [(p.extract_text() or "") for p in reader.pages]
            return "\n".join(parts).strip()
        elif name.endswith(".docx"):
            doc = Document(BytesIO(file_bytes))
            return "\n".join(p.text for p in doc.paragraphs if p.text).strip()
        else:
            return file_bytes.decode("utf-8", errors="ignore")
    except Exception:
        return file_bytes.decode("utf-8", errors="ignore")

def _split_text(text: str) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_text(text)

def upsert_documents(docs: List[Dict]):
    texts: List[str] = []
    metas: List[Dict] = []
    for d in docs:
        raw_text = d.get("text", "") or ""
        base_meta = d.get("meta", {}) or {}
        for chunk in _split_text(raw_text):
            if not chunk.strip():
                continue
            texts.append(chunk)
            metas.append(base_meta.copy())
    if not texts:
        return
    embeddings = _get_embeddings()
    vs = _load_vectorstore()
    if vs is None:
        vs = FAISS.from_texts(texts=texts, embedding=embeddings, metadatas=metas)
    else:
        vs.add_texts(texts=texts, metadatas=metas)
    _save_vectorstore(vs)

def query(q: str, k: int = 8) -> List[Dict]:
    vs = _load_vectorstore()
    if vs is None:
        return []
    docs = vs.similarity_search(q, k=k)
    results: List[Dict] = []
    for d in docs:
        meta = d.metadata or {}
        item = {"text": d.page_content}
        item.update(meta)
        results.append(item)
    return results
