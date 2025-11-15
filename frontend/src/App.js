import './App.css';
import React, { useState } from "react";

function App() {

  const [selectedFile, setSelectedFile] = useState(null);
  const [feedback, setFeedback] = useState(null);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]); //e tells you which input changed e.target is the input element itself
  };

  const handleUpload = async () => {
    if (!selectedFile) return alert("Please upload an image!");

    const formData = new FormData();
    formData.append("file", selectedFile);

    const res = await fetch("https://ai-wushu-coach-add5.onrender.com/analyze", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setFeedback(data);

  };


  return (
    <div style={{ padding: 40 }}>
      <h1>AI Wushu Coach</h1>

      <input type="file" accept="image/*" onChange={handleFileChange} />

      <button onClick={handleUpload} style={{ marginLeft: 10 }}>
        Analyze Stance
      </button>

      {feedback && (
        <pre style={{ marginTop: 20, background: "#eee", padding: 20 }}>
          {JSON.stringify(feedback, null, 2)}
        </pre>
      )}
    </div>
  );
}

export default App;
