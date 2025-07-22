# 📚 PDF Question-Answer App

This is a full-stack application that allows you to upload a PDF containing **Questions and Answers** and then ask questions.  
The app retrieves the most relevant answer from the uploaded PDF.

---

## 🌟 Features
✅ Upload a PDF with Q&A pairs  
✅ Ask questions and get the most relevant answer  
✅ Conversation history persists per session  
✅ Clean, responsive frontend (React)  
✅ FastAPI backend with LangChain, HuggingFace embeddings and FAISS

---

## 🖇️ Project Structure

pdf-qa-app/
├── backend/
│ ├── app.py # FastAPI backend
│ ├── requirements.txt # Python dependencies
│ └── .env.example # Sample environment variables
├── frontend/
│ └── (your React app) # JSX frontend code
├── README.md

---

## 🚀 Setup Instructions

### 🧰 Prerequisites
- Python 3.10+
- Node.js & npm (for frontend)
- A valid OpenAI API key

---

### 🔷 Backend Setup

cd backend/
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create your .env file
cp .env.example .env
# Add your OpenAI API key to .env

Run backend:
uvicorn app:app --reload
Backend runs at: http://127.0.0.1:8000

Frontend Setup:
cd frontend/
npm install
npm start
Frontend runs at: http://localhost:3000

🧪 API Endpoints
Endpoint	Method	 Description
/upload	        POST	 Upload PDF file
/ask	        POST	 Ask a question
/reset	        POST	 Reset conversation history

Once the web app is running, either use test.pdf to verify its functionality or generate a PDF based on the specified format.

Example PDF Format:

Question: What is the capital of France?
Answer: Paris

Question: Who wrote Hamlet?
Answer: William Shakespeare
