"""
main.py  —  Entry point (Phases 1–4)
Run:
    python src/main.py --index data/problem_statements.pdf
    python src/main.py --ask "What is RAG?"
"""

import argparse
import sys
import os

# Allow running as: python src/main.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.load import extract_pages, preview_chunks
from src.load import chunk_pages
from src.embed import embed_chunks, search, preview_hits, get_collection


def phase2_index(pdf_path: str, show_chunks=False) -> list[dict]:
    """Run Phase 2: load → clean → chunk (and optionally preview)."""
    print(f"\n[Phase 2] Loading PDF: {pdf_path}")

    # Step 1: extract per-page text
    pages = extract_pages(pdf_path)
    print(f"  ✓ Extracted {len(pages)} pages")

    # Step 2: clean and chunk
    chunks = chunk_pages(pages, chunk_size=400, overlap=50)
    print(f"  ✓ Created {len(chunks)} chunks (chunk_size=400, overlap=50)")

    # Step 3: preview chunks so you can verify they're readable
    if show_chunks:
        preview_chunks(chunks, n=5)

    return chunks


def index_pipeline(pdf_path: str) -> list[dict]:
    """Full indexing: Phase 2 (load → chunk) + Phase 3 (embed → store)."""
    chunks = phase2_index(pdf_path)
    embed_chunks(chunks)
    print("\n[Phase 3] Done. Index is ready — try: python src/main.py --ask \"your question\"")
    return chunks


def ask_pipeline(question: str, top_k: int = 4) -> list[dict]:
    """Full query: Phase 4 (embed question → search top-k chunks)."""
    collection = get_collection()
    hits = search(question, top_k=top_k, collection=collection)
    preview_hits(hits)
    print(f"\n[Phase 4] Done. Retrieved {len(hits)} chunks — next up: Phase 5 (LLM answer).")
    return hits


def main():
    parser = argparse.ArgumentParser(description="DocuMind – RAG over your PDF")
    parser.add_argument("--index", metavar="PDF", help="Index a PDF: load, chunk, embed, store (Phases 2–3)")
    parser.add_argument("--ask", metavar="QUESTION", help="Search the index for the top-k relevant chunks (Phase 4)")
    parser.add_argument("--top-k", type=int, default=4, help="How many chunks to retrieve (default: 4)")
    args = parser.parse_args()

    if args.index:
        index_pipeline(args.index)
    elif args.ask:
        ask_pipeline(args.ask, top_k=args.top_k)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
