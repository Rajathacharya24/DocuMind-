"""
embed.py  —  Phase 3: Embeddings & Vector DB
Embeds every chunk with sentence-transformers and stores chunks + embeddings
+ page numbers in a persistent ChromaDB collection.
"""

import chromadb
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
DB_DIR = "chroma"
COLLECTION_NAME = "documind"


def get_collection(persist_dir: str = DB_DIR):
    """Open (or create) the persistent ChromaDB collection."""
    client = chromadb.PersistentClient(path=persist_dir)
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def embed_chunks(
    chunks: list[dict],
    model_name: str = MODEL_NAME,
    persist_dir: str = DB_DIR,
):
    """
    Embed chunks and store everything in ChromaDB.

    Args:
        chunks:      List of dicts from chunk_pages(): {'chunk_id', 'text', 'word_count', 'page'}
        model_name:  sentence-transformers model to use.
        persist_dir: Where ChromaDB stores its data on disk.

    Returns:
        The number of chunks stored.
    """
    print(f"\n[Phase 3] Loading embedding model: {model_name}")
    model = SentenceTransformer(model_name)

    texts = [c["text"] for c in chunks]
    print(f"  ✓ Encoding {len(texts)} chunks...")
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True,
    )

    collection = get_collection(persist_dir)

    # Wipe old entries for a fresh index of this document
    existing = collection.get()
    if existing["ids"]:
        collection.delete(ids=existing["ids"])
        print(f"  ✓ Cleared {len(existing['ids'])} old entries")

    collection.add(
        ids=[str(c["chunk_id"]) for c in chunks],
        embeddings=embeddings.tolist(),
        documents=texts,
        metadatas=[{"page": c["page"], "word_count": c["word_count"]} for c in chunks],
    )
    print(f"  ✓ Stored {collection.count()} chunks in ChromaDB ({persist_dir}/)")

    return collection.count()


def search(
    query: str,
    top_k: int = 4,
    collection=None,
    model_name: str = MODEL_NAME,
):
    """
    Embed a query and return the top_k most similar chunks.

    Returns:
        List of dicts: {'chunk_id', 'text', 'page', 'score'}
        sorted from most to least similar (score = cosine similarity, 0..1).
    """
    if collection is None:
        collection = get_collection()

    if collection.count() == 0:
        raise ValueError("Index is empty — run --index first")

    print(f"\n[Phase 4] Embedding question: {query!r}")
    model = SentenceTransformer(model_name)
    query_emb = model.encode(
        [query],
        normalize_embeddings=True,
    )

    print(f"  ✓ Searching top-{top_k} chunks...")
    result = collection.query(
        query_embeddings=query_emb.tolist(),
        n_results=min(top_k, collection.count()),
    )

    hits = []
    for text, meta, dist, idx in zip(
        result["documents"][0],
        result["metadatas"][0],
        result["distances"][0],
        result["ids"][0],
    ):
        hits.append(
            {
                "chunk_id": int(idx),
                "text": text,
                "page": meta["page"],
                "score": 1.0 - dist,  # cosine space: distance → similarity (0..1)
            }
        )

    return hits


def preview_hits(hits: list[dict], n: int | None = None) -> None:
    """Print retrieved chunks with their similarity scores."""
    if n is None:
        n = len(hits)
    for hit in hits[:n]:
        print(f"\n--- Hit chunk {hit['chunk_id']}  (page {hit['page']}, score {hit['score']:.4f}) ---")
        print(hit["text"])
        print()
