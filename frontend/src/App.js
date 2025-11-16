import React, { useState } from "react";

function App() {

  const [selectedFile, setSelectedFile] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);
  const [loading, setLoading] = useState(false); //for when we are waitiing for analysis.



  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]); //e tells you which input changed e.target is the input element itself
  };

  const handleUpload = async () => {
    if (!selectedFile) return alert("Please upload an image!");

      setLoading(true);   // start loading
      setFeedback(null);  // clear old results

    const formData = new FormData();
    formData.append("file", selectedFile);

    try{

      // const res = await fetch("https://ai-wushu-coach-add5.onrender.com/analyze", {
      const res = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setFeedback(data);
      setProcessedImage(`data:image/jpeg;base64,${data.image}`); 
      
    } finally {
      setLoading(false);  // stop loading always
    }    
  };


  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="flex flex-col items-center w-full max-w-lg">
        <h1 className="text-3xl font-bold mb-6 text-center text-gray-800">
          AI Wushu Coach
        </h1>

        <div className="bg-white w-full rounded-2xl shadow-xl p-8 border border-gray-200">

          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-700 
                      border border-gray-300 rounded-lg cursor-pointer 
                      bg-gray-50 p-2 focus:outline-none focus:ring-2 
                      focus:ring-blue-500"
          />

          <button
            onClick={handleUpload}
            className="mt-4 w-full bg-blue-600 text-white py-3 rounded-lg 
                      font-semibold hover:bg-blue-700 active:bg-blue-800 
                      transition shadow-sm"
          >
            Analyze Stance
          </button>

          {loading && (
            <div className="mt-4 flex flex-col items-center">
              <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
              <p className="text-blue-600 font-medium mt-2">Analyzing stance…</p>
            </div>
          )}





          {processedImage && (
            <div className="mt-6 flex justify-center">
              <img
                src={processedImage}
                alt="Processed pose"
                className="rounded-lg shadow-md max-w-full"
              />
            </div>
          )}


          {feedback && (
            <div className="mt-6 bg-gray-50 p-4 rounded-lg border">
              <h3 className="text-xl font-semibold mb-3">Wushu Stance Feedback</h3>

              {Object.entries(feedback).filter(([key]) => key !== "image").map(([key, value]) => (
                <p key={key} className="mb-1">
                  <span className="font-medium">{key.replace(/_/g, " ")}:</span>{" "}
                  {value}
                </p>
              ))}
            </div>
          )}

        </div>
      </div>
    </div>
  );
}

export default App;
