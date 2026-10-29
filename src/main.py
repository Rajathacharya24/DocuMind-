"""
main.py  —  Entry point (Phases 1 & 2 only for now)
Run:
    python src/main.py --index data/problem_statements.pdf
"""

import argparse
import sys
import os

# Allow running as: python src/main.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.load import extract_pages, clean_text, chunk_pages, preview_chunks


def phase2_index(pdf_path: str) -> list[dict]:
    """Run Phase 2: load → clean → chunk and print a preview."""
    print(f"\n[Phase 2] Loading PDF: {pdf_path}")

    # Step 1: extract per-page text
    pages = extract_pages(pdf_path)
    print(f"  ✓ Extracted {len(pages)} pages")

    # Step 2: show a sample of raw text so you can spot problems
    raw_sample = pages[0]["text"][:500] if pages else ""
    print(f"\n--- Raw text sample (first 500 chars of page 1) ---\n{raw_sample}\n")

    # Step 3: clean and chunk
    chunks = chunk_pages(pages, chunk_size=400, overlap=50)
    print(f"  ✓ Created {len(chunks)} chunks (chunk_size=400, overlap=50)")

    # Step 4: preview 5 chunks
    preview_chunks(chunks, n=5)

    print("\n[Phase 2] Done. Every chunk above should be readable on its own.")
    return chunks


def main():
    parser = argparse.ArgumentParser(description="DocuMind – RAG over your PDF")
    parser.add_argument("--index", metavar="PDF", help="Load and chunk a PDF (Phase 2)")
    args = parser.parse_args()

    if args.index:
        phase2_index(args.index)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
