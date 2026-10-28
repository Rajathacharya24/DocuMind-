# DocuMind: Project Plan

**Goal:** Build a working RAG app that answers questions from a PDF, and understand every step of how it works.

**Time:** about 2 weeks, 1-2 hours per day.

## The flow

```
PDF -> Extract text -> Chunks -> Embeddings -> Vector DB
                                                  |
Question -> Embedding -> Search similar chunks -> Prompt (question + chunks) -> LLM -> Answer + Sources
```

The top line runs once per document. The bottom line runs for every question.

---

## Phase 1: Setup (Day 1)

- [ ] Install Python and create a virtual environment
- [ ] Install `pypdf`, `sentence-transformers`, `chromadb`, and one LLM library
- [ ] Pick one PDF (10-20 pages) that you know well
- [ ] Create a GitHub repo and make the first commit

**Done when:** all packages import without errors.

## Phase 2: Load and chunk (Day 2-3)

- [ ] Extract text from the PDF and print it
- [ ] Look at the problems (headers, footers, page numbers, broken lines)
- [ ] Clean the text
- [ ] Split into chunks of about 400 words with 50 words overlap
- [ ] Print 5 chunks and read them

**Done when:** every chunk is readable and makes sense by itself.

## Phase 3: Embeddings and vector DB (Day 4-5)

- [ ] Create an embedding for each chunk with `sentence-transformers`
- [ ] Print the shape of one embedding (how many numbers it has)
- [ ] Store chunks, embeddings, and page numbers in ChromaDB
- [ ] Check the number of stored chunks matches your chunk count

**Done when:** the database is filled and can be reloaded without re-embedding.

## Phase 4: Retrieval (Day 6-7)

- [ ] Take a question and create its embedding
- [ ] Get the top 4 most similar chunks
- [ ] Print the chunks with their similarity scores
- [ ] Try 10 questions and check if the right chunk comes back

**Done when:** retrieval finds the right chunk for most of your questions. Do not move on before this works.

## Phase 5: Generation (Day 8-9)

- [ ] Write the prompt: *"Answer only from the context below. If the answer is not in the context, say 'I don't know'."*
- [ ] Send the question and chunks to the LLM
- [ ] Print the answer and the sources (chunks and page numbers)
- [ ] Ask a question that is NOT in the document and check it says "I don't know"

**Done when:** answers are correct, grounded, and show sources.

## Phase 6: Test and improve (Day 10-12)

- [ ] Write 10 test questions with known answers (include 2 that are not in the document)
- [ ] Run all 10 and mark each as correct or wrong
- [ ] For each wrong answer, find the cause: bad chunk, bad retrieval, or bad prompt
- [ ] Compare chunk sizes: 200, 500, 800
- [ ] Compare top-k: 2, 4, 6
- [ ] Record every result in `notes.md`

**Done when:** you can explain why each failure happened and which settings work best.

## Phase 7: Finish (Day 13-14)

- [ ] Add a Streamlit UI (upload PDF, ask question, show answer and sources)
- [ ] Clean the code and add comments
- [ ] Finish the README with your learnings
- [ ] Push to GitHub

**Done when:** someone else can clone the repo and run it using only the README.

---

## What to notice while building

1. **Check the retrieved chunks before the LLM answer.** If the chunks are wrong, the answer will be wrong.
2. **Chunk size changes everything.** Too big gives vague search. Too small loses context.
3. **Overlap prevents cut answers** between two chunks.
4. **Messy PDFs pollute chunks.** Tables, headers, and footers are the usual problem.
5. **The prompt controls hallucination.** Without "answer only from the context", the LLM adds its own knowledge.
6. **Test questions that are not in the document.** A good RAG says "I don't know".
7. **Write notes after every experiment.** This becomes your interview material.

## Common mistakes to avoid

- Using LangChain before understanding the basic steps
- Starting with a very large PDF
- Skipping the testing phase
- Not committing to GitHub regularly
- Changing many settings at once (change one thing, then test)

## Test question template

| # | Question | Expected answer | Actual answer | Correct? | Reason if wrong |
|---|----------|-----------------|---------------|----------|-----------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

## Stretch goals (after the 2 weeks)

- [ ] Multiple documents
- [ ] Chat history for follow-up questions
- [ ] Re-ranking of retrieved chunks
- [ ] Rebuild the same project in Java with Spring AI or LangChain4j

## Final result

- A working RAG app
- Clear understanding of embeddings, chunking, retrieval, and prompting
- A GitHub project with a good README to show in interviews