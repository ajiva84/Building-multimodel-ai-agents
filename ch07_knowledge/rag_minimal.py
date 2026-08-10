"""Chapter 7 — the minimal honest RAG stack (chromadb)."""
import json
import chromadb

client_db = chromadb.PersistentClient(path="./kb")
kb = client_db.get_or_create_collection("knowledge")

def chunk_text(text: str, target_tokens: int = 500, overlap: float = 0.1):
    """STUB: split on headers/paragraphs, ~target size, ~10% overlap.
    Respect natural boundaries — never split mid-sentence (Ch. 7.3)."""
    paras = [p for p in text.split("\n\n") if p.strip()]
    return paras  # replace with real boundary-aware chunking

def index_document(doc_id: str, text: str, source: str):
    chunks = chunk_text(text)
    kb.add(
        ids=[f"{doc_id}-{i}" for i in range(len(chunks))],
        documents=chunks,
        metadatas=[{"source": source, "chunk": i} for i in range(len(chunks))],
    )

def search_knowledge(query: str, k: int = 5) -> str:
    """Search the knowledge base. If results look irrelevant, call again
    with different phrasing before concluding the answer isn't there."""
    hits = kb.query(query_texts=[query], n_results=k)
    if not hits["documents"][0]:
        return json.dumps({"results": [], "hint": "try different phrasing"})
    return json.dumps([
        {"id": i, "source": m["source"], "text": d}
        for i, (d, m) in enumerate(
            zip(hits["documents"][0], hits["metadatas"][0]))
    ])
