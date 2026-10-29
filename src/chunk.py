"""
chunk.py  —  Phase 2 companion
Re-exports the chunking helpers from load.py so other modules import cleanly.
"""

from src.load import chunk_text, chunk_pages, preview_chunks

__all__ = ["chunk_text", "chunk_pages", "preview_chunks"]
