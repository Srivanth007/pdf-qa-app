from typing import Optional, Tuple, List
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from dotenv import load_dotenv
import pdfplumber
import tempfile
import os
import re

# 📄 Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY is not set in .env")

# 🚀 FastAPI app
app = FastAPI()

# 🌐 CORS setup for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🗂️ Global state
state = {
    "retriever": None,
    "history": []
}


def extract_qa_pairs(text: str) -> List[Document]:
    """
    🔍 Parse text and extract Q/A pairs as individual documents.
    """
    pattern = r"Question:\s*(.*?)\s*Answer:\s*(.*?)(?=\nQuestion:|\Z)"
    matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)

    docs = []
    for q, a in matches:
        content = f"Question: {q.strip()}\nAnswer: {a.strip()}"
        docs.append(Document(page_content=content))
    return docs


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    📤 Upload a PDF, extract Q&A pairs, and build the retriever.
    """
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        return {"error": "Only PDF files are supported."}

    # Save uploaded PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        text = ""
        with pdfplumber.open(tmp_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    finally:
        os.remove(tmp_path)

    if not text.strip():
        return {"error": "Uploaded PDF has no extractable text."}

    qa_docs = extract_qa_pairs(text)

    if not qa_docs:
        return {"error": "Could not extract any Q&A pairs from the PDF."}

    # Build embeddings & retriever
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_documents(qa_docs, embeddings)
    retriever = db.as_retriever()

    # Reset state
    state["retriever"] = retriever
    state["history"] = []

    return {"message": "✅ PDF uploaded and Q&A pairs processed successfully!"}


@app.post("/ask")
async def ask_question(question: str = Form(...)):
    """
    🤔 Ask a question and get the most relevant answer from the PDF.
    """
    retriever = state.get("retriever")
    if retriever is None:
        return {"error": "❌ No PDF uploaded yet. Please upload a PDF first."}

    # Find the most relevant Q/A pair
    docs = retriever.get_relevant_documents(question)

    if not docs:
        answer = "❌ Sorry, the answer to this question was not found in the uploaded PDF."
    else:
        # Parse out the Answer
        content = docs[0].page_content
        match = re.search(r"Answer:\s*(.*)", content, re.IGNORECASE | re.DOTALL)
        if match:
            answer = match.group(1).strip()
        else:
            answer = "❌ Sorry, could not extract the answer properly."

    state["history"].append((question, answer))

    return {
        "answer": answer,
        "history": state["history"]
    }


@app.post("/reset")
def reset():
    """
    🔄 Reset the conversation history.
    """
    state["history"] = []
    return {"message": "✅ Conversation history reset."}
