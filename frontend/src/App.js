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
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-10">
      <h1 className="text-4xl font-bold mb-8">AI Wushu Coach</h1>

      <div className="bg-white p-6 rounded-xl shadow-md w-full max-w-md">
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          className="w-full border border-gray-300 rounded-lg p-3 mb-4"
        />

        <button
          onClick={handleUpload}
          className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
        >
          Analyze Stance
        </button>

        {feedback && (
          <div className="mt-6 bg-gray-50 p-4 rounded-lg border">
            <h3 className="text-xl font-semibold mb-3">Wushu Stance Feedback</h3>

            {Object.entries(feedback).map(([key, value]) => (
              <p key={key} className="mb-1">
                <span className="font-medium">{key.replace(/_/g, " ")}:</span>{" "}
                {value}
              </p>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
