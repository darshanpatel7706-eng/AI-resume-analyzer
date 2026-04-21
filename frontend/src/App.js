import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [jobDesc, setJobDesc] = useState("");
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async () => {
    if (!file) {
      alert("Please upload resume");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("job_description", jobDesc);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/upload",
        formData
      );

      setResult(response.data);
    } catch (error) {
      console.error("Error:", error);
      alert("Error analyzing resume");
    }
  };

  return (
    <div className="App">
      <h1>AI Resume Analyzer</h1>

      <div className="upload-section">
        <input type="file" onChange={handleFileChange} />

        <textarea
          placeholder="Paste Job Description..."
          value={jobDesc}
          onChange={(e) => setJobDesc(e.target.value)}
        />

        <button onClick={handleSubmit}>Analyze Resume</button>
      </div>

      {result && (
        <div className="result">
          <h2>Results</h2>

          <p>
            <strong>Score:</strong> {result.score || "N/A"}
          </p>

          <p>
            <strong>Match Score:</strong> {result.match_score || "N/A"}%
          </p>

          <p>
            <strong>Skills:</strong>{" "}
            {result.skills
              ? result.skills.join(", ")
              : "No skills detected"}
          </p>

          <p>
            <strong>Job Role:</strong>{" "}
            {result.job_role || "Not detected"}
          </p>

          <p>
            <strong>Feedback:</strong>{" "}
            {result.match_feedback || "No feedback"}
          </p>

          <div>
            <strong>Suggestions:</strong>
            <ul>
              {result.suggestions &&
                result.suggestions.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;