"""
generate.py  —  Phase 5: Generation
Builds a grounded prompt and returns an answer using the retrieved context.
If no API key is configured, it falls back to a simple answer based on the
retrieved chunks so the project still works locally.
"""

from __future__ import annotations

import os
from typing import Sequence


GROUNDING_INSTRUCTION = (
    'Answer only from the context below. If the answer is not in the context, '
    'say "I don\'t know".'
)


def build_prompt(question: str, context_chunks: Sequence[str]) -> str:
    """Create a prompt that asks the model to answer only from the provided chunks."""
    cleaned_context = [chunk.strip() for chunk in context_chunks if chunk and chunk.strip()]
    if not cleaned_context:
        context_block = "No relevant context found."
    else:
        context_block = "\n\n".join(
            f"[Context {index}]\n{chunk}" for index, chunk in enumerate(cleaned_context, start=1)
        )

    return (
        f"{GROUNDING_INSTRUCTION}\n\n"
        f"Question: {question}\n\n"
        f"Context:\n{context_block}\n"
    )


def fallback_answer(question: str, context_chunks: Sequence[str]) -> str:
    """Return a local, grounded answer when no LLM is configured."""
    if not context_chunks:
        return "I don't know"

    joined = " ".join(context_chunks)
    if not joined.strip():
        return "I don't know"

    # A simple rule: if the question's important words appear in the context,
    # use the most relevant chunk as the answer source.
    lower_q = question.lower()
    lower_text = joined.lower()
    if not any(word in lower_text for word in lower_q.split() if len(word) > 3):
        return "I don't know"

    return joined[:800].strip()


def generate_answer(
    question: str,
    context_chunks: Sequence[str],
    api_key: str | None = None,
    model: str = "gpt-4o-mini",
):
    """Generate an answer from retrieved context.

    If OPENAI_API_KEY is available, this calls the OpenAI Responses API.
    Otherwise it falls back to a local answer so the project remains runnable.
    """
    prompt = build_prompt(question, context_chunks)
    key = api_key or os.getenv("OPENAI_API_KEY")

    if not key:
        return fallback_answer(question, context_chunks)

    try:
        from openai import OpenAI

        client = OpenAI(api_key=key)
        response = client.responses.create(
            model=model,
            input=[{"role": "user", "content": prompt}],
        )
        text = getattr(response, "output_text", None)
        if text:
            return text.strip()
    except Exception:
        pass

    return fallback_answer(question, context_chunks)
