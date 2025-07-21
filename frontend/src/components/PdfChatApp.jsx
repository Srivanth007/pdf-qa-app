import React, { useState, useRef } from "react";

const PdfChatApp = () => {
  const [chatHistory, setChatHistory] = useState([]);
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const questionInputRef = useRef();

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setChatHistory((prev) => [
      ...prev,
      { type: "info", message: "📤 Uploading PDF…" },
    ]);

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();

    setChatHistory((prev) => [
      ...prev,
      { type: data.error ? "error" : "success", message: data.message || data.error },
    ]);
    setLoading(false);
  };

  const handleAsk = async (e) => {
    e.preventDefault();
    const question = questionInputRef.current.value.trim();
    if (!question) return;

    setChatHistory((prev) => [
      ...prev,
      { type: "question", message: question },
    ]);

    const formData = new FormData();
    formData.append("question", question);

    const res = await fetch("http://127.0.0.1:8000/ask", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();

    if (data.answer) {
      setChatHistory((prev) => [
        ...prev,
        { type: "answer", message: data.answer },
      ]);
    } else {
      setChatHistory((prev) => [
        ...prev,
        { type: "error", message: data.error },
      ]);
    }

    questionInputRef.current.value = "";
  };

  return (
    <div className="bg-gradient-to-br from-slate-100 to-slate-200 min-h-screen flex items-center justify-center p-4">
      <div className="bg-white shadow-lg rounded-xl p-8 max-w-2xl w-full">
        <h1 className="text-3xl font-bold text-center text-indigo-600 mb-6">
          📄 Chat with your <span className="text-gray-800">PDF</span>
        </h1>

        <div className="flex space-x-4 mb-6">
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            className="border border-gray-300 rounded px-3 py-2 w-full"
          />
          <button
            onClick={handleUpload}
            disabled={loading}
            className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded shadow disabled:opacity-50"
          >
            Upload PDF
          </button>
        </div>

        <div className="border rounded p-4 h-64 overflow-y-auto bg-gray-50 space-y-3 mb-4 text-sm">
          {chatHistory.length === 0 && (
            <p className="text-gray-400">📝 Your chat history will appear here…</p>
          )}
          {chatHistory.map((item, idx) => (
            <div key={idx}>
              {item.type === "question" && (
                <div>
                  <span className="font-bold text-gray-700">Q:</span> {item.message}
                </div>
              )}
              {item.type === "answer" && (
                <div>
                  <span className="font-bold text-green-700">A:</span> {item.message}
                </div>
              )}
              {item.type === "error" && (
                <div className="text-red-600">❌ {item.message}</div>
              )}
              {item.type === "success" && (
                <div className="text-green-600">{item.message}</div>
              )}
              {item.type === "info" && (
                <div className="text-blue-600">{item.message}</div>
              )}
            </div>
          ))}
        </div>

        <form onSubmit={handleAsk} className="flex space-x-4">
          <input
            type="text"
            placeholder="Type your question..."
            ref={questionInputRef}
            className="border border-gray-300 rounded px-3 py-2 w-full"
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded shadow disabled:opacity-50"
          >
            Ask
          </button>
        </form>
      </div>
    </div>
  );
};

export default PdfChatApp;
