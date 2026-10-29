"""Markdown ingestion, multilingual-e5 embeddings, and Chroma retrieval."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from backend.config import DATA_DIR, EMBEDDING_MODEL, SPECIALTIES, VECTOR_DIR

_collection = None
_encoder = None


def _normalize_specialty(path: Path, metadata: dict) -> str:
    """Use the folder as canonical specialty; metadata may name a sub-specialty."""
    name = str(path).casefold()
    raw = metadata.get("specialty", "").casefold()
    if "noi_tiet" in name or "nội tiết" in raw:
        return "Nội tiết"
    if "hohap" in name or "hô hấp" in raw:
        return "Hô hấp"
    if "tim" in name or "tim mạch" in raw:
        return "Tim mạch"
    return metadata.get("specialty", "Chưa phân loại")


def _parse_frontmatter(text: str) -> tuple[str, dict]:
    match = re.search(r"(?ms)^---\s*\n(.*?)\n---\s*", text)
    if not match:
        return text, {}
    metadata = {}
    for line in match.group(1).splitlines():
        field = re.match(r"([\w-]+):\s*(.*)", line)
        if field:
            metadata[field.group(1)] = field.group(2).strip().strip("\"'")
    return text[match.end():], metadata


def _split_document(text: str, path: Path) -> list[dict]:
    """Split at Markdown headings and attach source information to each chunk."""
    # Recover the UTF-8 text from a small subset of files saved as UTF-8 interpreted
    # through Windows-1252. Proper Vietnamese UTF-8 remains untouched.
    try:
        text = text.encode("cp1252").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass

    body, metadata = _parse_frontmatter(text)
    specialty = _normalize_specialty(path, metadata)
    pieces = re.split(r"(?m)^(#{1,3})\s+(.+?)\s*$", body)
    fallback_heading = Path(path).stem.replace("_", " ")
    chunks = []

    def add(content: str, heading: str) -> None:
        content = content.strip()
        if len(content) < 80:
            return
        for start in range(0, len(content), 1400):
            excerpt = content[start:start + 1800].strip()
            if len(excerpt) < 80:
                continue
            chunks.append({
                "text": f"{heading}\n{excerpt}",
                "specialty": specialty,
                "disease": metadata.get("title", Path(path).stem),
                "section": heading,
                "source": str(path.relative_to(DATA_DIR)).replace("\\", "/"),
                "review_status": metadata.get("review_status", "not specified"),
            })

    if pieces and pieces[0].strip():
        add(pieces[0], fallback_heading)
    for index in range(1, len(pieces), 3):
        heading = pieces[index + 1].strip()
        content = pieces[index + 2] if index + 2 < len(pieces) else ""
        add(content, heading)
    return chunks


def read_documents() -> list[dict]:
    """Read all Markdown files under the configured knowledge directory."""
    documents = []
    if not DATA_DIR.exists():
        return documents
    for path in sorted(DATA_DIR.rglob("*.md")):
        try:
            documents.extend(_split_document(path.read_text(encoding="utf-8"), path))
        except (OSError, UnicodeError):
            continue
    return documents


def document_inventory() -> dict:
    """Return file/chunk totals and source metadata for the management page."""
    files = {}
    for chunk in read_documents():
        source = chunk["source"]
        files.setdefault(source, {
            "source": source,
            "specialty": chunk["specialty"],
            "disease": chunk["disease"],
            "review_status": chunk["review_status"],
            "chunks": 0,
        })["chunks"] += 1
    return {
        "total_files": len(files),
        "total_chunks": sum(item["chunks"] for item in files.values()),
        "specialties": {name: sum(item["specialty"] == name for item in files.values()) for name in SPECIALTIES},
        "documents": list(files.values()),
    }


def _get_encoder():
    global _encoder
    if _encoder is None:
        from sentence_transformers import SentenceTransformer

        _encoder = SentenceTransformer(EMBEDDING_MODEL)
    return _encoder


def _get_collection():
    global _collection
    if _collection is None:
        import chromadb

        client = chromadb.PersistentClient(path=str(VECTOR_DIR))
        _collection = client.get_or_create_collection(
            "clinical_guidelines", metadata={"hnsw:space": "cosine"}
        )
    return _collection


def ingest_documents(documents: list[dict] | None = None, *, reset: bool = True) -> int:
    """Embed and upsert a document set, optionally replacing the existing index."""
    collection = _get_collection()
    encoder = _get_encoder()
    if reset and collection.count():
        collection.delete(where={"source": {"$ne": "__none__"}})
    documents = read_documents() if documents is None else documents
    for start in range(0, len(documents), 64):
        batch = documents[start:start + 64]
        ids = [
            hashlib.sha1((item["source"] + item["section"] + item["text"][:120]).encode()).hexdigest()
            for item in batch
        ]
        vectors = encoder.encode(
            ["passage: " + item["text"] for item in batch], normalize_embeddings=True
        ).tolist()
        collection.upsert(
            ids=ids,
            embeddings=vectors,
            documents=[item["text"] for item in batch],
            metadatas=[{key: value for key, value in item.items() if key != "text"} for item in batch],
        )
    return len(documents)


def ensure_index():
    """Load the persisted collection and create it from Markdown when empty."""
    collection = _get_collection()
    if collection.count() == 0:
        ingest_documents(reset=False)
    return collection


def search_documents(query: str, specialty: str, top_k: int) -> list[dict]:
    collection = ensure_index()
    vector = _get_encoder().encode(["query: " + query], normalize_embeddings=True).tolist()[0]
    where = None if specialty in ("Tất cả", "Tự động") else {"specialty": specialty}
    result = collection.query(
        query_embeddings=[vector], n_results=top_k, where=where,
        include=["documents", "metadatas", "distances"],
    )
    return [
        {"text": text, **metadata, "score": round(1 - distance, 4), "citation_id": f"S{index + 1}"}
        for index, (text, metadata, distance) in enumerate(zip(
            result["documents"][0], result["metadatas"][0], result["distances"][0]
        ))
    ]
