"""
retrieve.py  —  Phase 4: Retrieval
Thin wrapper around embed.search() so other modules import cleanly.
Finds the top-k most similar chunks for a question, with similarity scores.
"""

from src.embed import search, preview_hits

__all__ = ["search", "preview_hits"]
