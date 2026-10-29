"""
load.py  —  Phase 2: Load and chunk
Reads a PDF, cleans the raw text, and splits it into overlapping chunks.
"""

import re
import pypdf


# ─── 1. Extract raw text ──────────────────────────────────────────────────────

def extract_text(pdf_path: str) -> str:
    """
    Read every page of the PDF and join them with a newline.
    Returns the raw text as a single string.
    """
    raw_pages = []
    with open(pdf_path, "rb") as f:
        reader = pypdf.PdfReader(f)
        for page_num, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text() or ""
            raw_pages.append((page_num, page_text))

    # Join all pages; we'll keep page numbers for later use in chunking
    full_text = "\n".join(text for _, text in raw_pages)
    return full_text


def extract_pages(pdf_path: str) -> list[dict]:
    """
    Return a list of dicts: {'page': int, 'text': str}
    Keeps page-level granularity so chunks can carry a page number.
    """
    pages = []
    with open(pdf_path, "rb") as f:
        reader = pypdf.PdfReader(f)
        for page_num, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text() or ""
            pages.append({"page": page_num, "text": page_text})
    return pages


# ─── 2. Clean text ────────────────────────────────────────────────────────────

def clean_text(text: str) -> str:
    """
    Remove common PDF noise: headers, footers, page numbers, broken hyphenated
    line-breaks, and excessive whitespace.
    """
    # Remove lines that are only a page number (e.g. "3", "— 3 —", "Page 3")
    text = re.sub(r"(?m)^\s*(Page\s*)?\d+\s*$", "", text)

    # Reconnect words broken across lines with a hyphen  (e.g. "algo-\nrithm")
    text = re.sub(r"-\n(\S)", r"\1", text)

    # Replace single newlines inside a paragraph with a space
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    # Collapse multiple blank lines into one
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Strip leading/trailing whitespace from each line
    lines = [line.strip() for line in text.splitlines()]
    text = "\n".join(lines)

    # Collapse multiple spaces
    text = re.sub(r" {2,}", " ", text)

    return text.strip()


# ─── 3. Chunking ─────────────────────────────────────────────────────────────

def chunk_text(
    text: str,
    chunk_size: int = 400,
    overlap: int = 50,
) -> list[dict]:
    """
    Split *text* into word-based overlapping chunks.

    Args:
        text:       The cleaned full document text.
        chunk_size: Target number of words per chunk.
        overlap:    Number of words shared between consecutive chunks.

    Returns:
        List of dicts: {'chunk_id': int, 'text': str, 'word_count': int}
    """
    words = text.split()
    chunks = []
    start = 0
    chunk_id = 0

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text_str = " ".join(chunk_words)

        chunks.append(
            {
                "chunk_id": chunk_id,
                "text": chunk_text_str,
                "word_count": len(chunk_words),
            }
        )

        chunk_id += 1
        start += chunk_size - overlap  # slide forward with overlap

    return chunks


def chunk_pages(
    pages: list[dict],
    chunk_size: int = 400,
    overlap: int = 50,
) -> list[dict]:
    """
    Same as chunk_text but preserves the approximate page number for each chunk.
    Joins all page texts first, then chunks, and records the page of the first
    word in each chunk.

    Returns:
        List of dicts: {'chunk_id': int, 'text': str, 'word_count': int, 'page': int}
    """
    # Build a word list that also tracks which page each word came from
    all_words = []
    all_pages = []

    for page_info in pages:
        cleaned = clean_text(page_info["text"])
        words = cleaned.split()
        all_words.extend(words)
        all_pages.extend([page_info["page"]] * len(words))

    chunks = []
    start = 0
    chunk_id = 0

    while start < len(all_words):
        end = start + chunk_size
        chunk_words = all_words[start:end]
        chunk_page = all_pages[start]  # page of the first word in this chunk

        chunks.append(
            {
                "chunk_id": chunk_id,
                "text": " ".join(chunk_words),
                "word_count": len(chunk_words),
                "page": chunk_page,
            }
        )

        chunk_id += 1
        start += chunk_size - overlap

    return chunks


# ─── 4. Quick inspection helper ───────────────────────────────────────────────

def preview_chunks(chunks: list[dict], n: int = 5) -> None:
    """Print the first *n* chunks so you can verify they look clean."""
    print(f"\n{'='*60}")
    print(f"Total chunks: {len(chunks)}")
    print(f"{'='*60}")
    for chunk in chunks[:n]:
        page_info = f"  page {chunk['page']}" if "page" in chunk else ""
        print(f"\n--- Chunk {chunk['chunk_id']}{page_info} ({chunk['word_count']} words) ---")
        print(chunk["text"])
        print()
