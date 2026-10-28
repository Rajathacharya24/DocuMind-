# DocuMind

A simple RAG (Retrieval-Augmented Generation) project that answers questions from your own PDF, and shows which part of the document it used.

Built as a learning project to understand how RAG works: theory, technical details, and practice.

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

## Usage

```bash
# Index your PDF
python src/main.py --index data/your_file.pdf

# Ask a question
python src/main.py --ask "What is the leave policy?"

# Run the UI (optional)
streamlit run app.py
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

## Future improvements

- Support multiple documents
- Add a test set of questions with known answers
- Try a re-ranking step to improve retrieval
- Chat history (follow-up questions)

## License

MIT