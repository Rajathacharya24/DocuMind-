import os
from pathlib import Path

import streamlit as st

from src.embed import embed_chunks, get_collection, search
from src.generate import generate_answer
from src.load import chunk_pages, extract_pages


st.set_page_config(page_title="DocuMind", page_icon="📚")
st.title("📚 DocuMind")
st.caption("Ask questions about a PDF using retrieval-augmented generation.")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
question = st.text_input("Question")


if uploaded_file is not None:
    temp_pdf = Path("data") / uploaded_file.name
    temp_pdf.parent.mkdir(exist_ok=True)
    temp_pdf.write_bytes(uploaded_file.read())

    if st.button("Index and search"):
        pages = extract_pages(str(temp_pdf))
        chunks = chunk_pages(pages, chunk_size=400, overlap=50)
        embed_chunks(chunks)
        st.success(f"Indexed {len(chunks)} chunks from {uploaded_file.name}.")

if question:
    collection = get_collection()
    if collection.count() == 0:
        st.warning("No indexed document found yet. Upload and index a PDF first.")
    else:
        hits = search(question, top_k=4, collection=collection)
        context = [hit["text"] for hit in hits]
        answer = generate_answer(question, context, api_key=os.getenv("OPENAI_API_KEY"))

        st.subheader("Answer")
        st.write(answer)

        st.subheader("Source chunks")
        for hit in hits:
            st.markdown(f"**Page {hit['page']}** — score {hit['score']:.4f}")
            st.write(hit["text"])
