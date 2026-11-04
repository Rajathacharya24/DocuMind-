# DocuMind

A simple RAG (Retrieval-Augmented Generation) project that answers questions from your own PDF, and shows which part of the document it used.

Built as a learning project to understand how RAG works: theory, technical details, and practice.

## 🗓️ Project checklist

### ✅ Done
- [x] Set up the Python project and virtual environment
- [x] Installed dependencies: `pypdf`, `sentence-transformers`, `chromadb`, `streamlit`, `openai`
- [x] Added project requirements in `requirements.txt`
- [x] Selected a PDF for the project: `data/problem_statements.pdf`
- [x] Extracted text page by page from the PDF
- [x] Cleaned PDF noise like page numbers and broken line breaks
- [x] Split the text into overlapping chunks with a 400-word chunk size and 50-word overlap
- [x] Verified chunk output looks readable and useful

### ⏳ Still to do
- [ ] Phase 3: Create embeddings for each chunk using `sentence-transformers`
- [ ] Phase 3: Store chunks, embeddings, and page numbers in ChromaDB
- [ ] Phase 3: Verify the database count matches the chunk count
- [ ] Phase 4: Embed a question and retrieve the top 4 similar chunks
- [ ] Phase 4: Check retrieval quality with several sample questions
- [ ] Phase 5: Build a grounded prompt and call the LLM
- [ ] Phase 5: Show the answer together with source chunks/pages
- [ ] Phase 5: Test a question not in the document and confirm it says “I don’t know”
- [ ] Phase 6: Write 10 test questions and evaluate results
- [ ] Phase 6: Tune chunk size and top-k settings
- [ ] Phase 7: Add a Streamlit UI
- [ ] Phase 7: Clean code and add comments
- [ ] Phase 7: Finish the README and learning notes
- [ ] Phase 7: Push the final repo to GitHub

### Verified status
- Ran `python src/main.py --index data/problem_statements.pdf`
- Result: PDF pages were extracted and chunking worked as expected
- Current status: setup and chunking are complete; embedding and vector DB work is the next active step

---

## What it does

1. You load a PDF (for example a policy, manual, or textbook chapter).
2. You ask a question in plain English.
3. DocuMind finds the most relevant parts of the PDF.
4. An LLM writes the answer using only those parts.
5. The answer is shown together with its sources.

If the answer is not in the document, DocuMind says "I don't know" instead of guessing.

## How it works

```
PDF -> Extract text -> Chunks -> Embeddings -> Vector DB
                                                  |
Question -> Embedding -> Search similar chunks -> Prompt (question + chunks) -> LLM -> Answer + Sources
```

- **Indexing (runs once per document):** extract text, split into chunks, create embeddings, store in the vector database.
- **Querying (runs for every question):** embed the question, retrieve the top chunks, send them to the LLM, show the answer and sources.

## Tech stack

| Part | Tool |
|------|------|
| Language | Python 3.10+ |
| PDF reading | `pypdf` |
| Embeddings | `sentence-transformers` (local, free) |
| Vector database | `chromadb` |
| LLM | OpenAI / Anthropic / Gemini API (any one) |
| UI (optional) | Streamlit |

## Project structure

```
documind/
├── README.md
├── PLAN.md
├── requirements.txt
├── data/              # put your PDF here
├── src/
│   ├── load.py        # read PDF and extract text
│   ├── chunk.py       # split text into chunks
│   ├── embed.py       # create embeddings and store in ChromaDB
│   ├── retrieve.py    # find the most relevant chunks
│   ├── generate.py    # build prompt and call the LLM
│   └── main.py        # connect everything
├── app.py             # Streamlit UI (optional)
└── notes.md           # experiment log
```

## Setup

```bash
# 1. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install packages
pip install pypdf sentence-transformers chromadb streamlit

# 3. Install your LLM library (choose one)
pip install openai              # or: anthropic / google-generativeai

# 4. Set your API key
export OPENAI_API_KEY="your-key-here"
```



## Key settings to experiment with

| Setting | Starting value | What to try |
|---------|----------------|-------------|
| Chunk size | 400 words | 200, 500, 800 |
| Chunk overlap | 50 words | 0, 50, 100 |
| Chunks retrieved (top-k) | 4 | 2, 4, 6 |

## What I learned

Add your findings here as you build. Example:

- Chunk size of 200 lost context, 500 gave the best answers.
- Without overlap, some answers were cut between two chunks.
- Adding "answer only from the context" to the prompt stopped hallucinations.
