from src.generate import build_prompt


def test_build_prompt_contains_grounding_instructions():
    prompt = build_prompt(
        question="What is RAG?",
        context_chunks=["RAG combines retrieval and generation.", "It is useful for document Q&A."],
    )

    assert "Answer only from the context below" in prompt
    assert "What is RAG?" in prompt
    assert "RAG combines retrieval and generation." in prompt
