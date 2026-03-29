"use client";
import React, { useState } from "react";

export default function Home() {
  const [story, setStory] = useState("");
  const [testCases, setTestCases] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const generateTests = async () => {
    setLoading(true);
    setError("");
    setTestCases([]);
    
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const response = await fetch(`${apiUrl}/api/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_story: story,
          provider: "openai"
        })
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.statusText}`);
      }

      const data = await response.json();
      setTestCases(data.test_cases || []);
    } catch (err: any) {
      setError(err.message || "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: "1200px", margin: "0 auto", padding: "2rem" }}>
      <h1>AI Test Case Generator MVP</h1>
      <p style={{ color: "#666" }}>Paste a user story below to validate LLM generation using the 5-Lens method.</p>
      
      <div style={{ marginBottom: "2rem" }}>
        <textarea 
          style={{ width: "100%", height: "150px", padding: "1rem", fontSize: "16px" }}
          placeholder="As a user, I want to reset my password using my email so I can regain access."
          value={story}
          onChange={(e) => setStory(e.target.value)}
        />
        <br />
        <button 
          onClick={generateTests} 
          disabled={loading || story.trim().length < 10}
          style={{ 
            marginTop: "1rem", 
            padding: "0.75rem 1.5rem", 
            backgroundColor: loading ? "#ccc" : "#0070f3", 
            color: "white", 
            border: "none",
            borderRadius: "4px",
            cursor: loading ? "not-allowed" : "pointer"
          }}
        >
          {loading ? "Generating Tests..." : "Generate Test Cases"}
        </button>
      </div>

      {error && <div style={{ color: "red", padding: "1rem", backgroundColor: "#ffebee", border: "1px solid red", marginBottom: "2rem" }}>{error}</div>}

      {testCases.length > 0 && (
        <div>
          <h2>Generated Test Cases: {testCases.length}</h2>
          <table style={{ width: "100%", borderCollapse: "collapse", marginTop: "1rem" }}>
            <thead>
              <tr style={{ backgroundColor: "#f5f5f5", textAlign: "left" }}>
                <th style={{ border: "1px solid #ddd", padding: "8px" }}>ID</th>
                <th style={{ border: "1px solid #ddd", padding: "8px" }}>Type</th>
                <th style={{ border: "1px solid #ddd", padding: "8px" }}>Priority</th>
                <th style={{ border: "1px solid #ddd", padding: "8px" }}>Description</th>
                <th style={{ border: "1px solid #ddd", padding: "8px" }}>Steps</th>
                <th style={{ border: "1px solid #ddd", padding: "8px" }}>Expected</th>
              </tr>
            </thead>
            <tbody>
              {testCases.map((tc, idx) => (
                <tr key={idx}>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>{tc.test_case_id}</td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}><strong>{tc.test_type}</strong></td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>{tc.priority}</td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>{tc.description}</td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                    <ul style={{ margin: 0, paddingLeft: "20px" }}>
                      {Array.isArray(tc.steps) ? tc.steps.map((step: string, sIdx: number) => (
                        <li key={sIdx}>{step}</li>
                      )) : <li>{tc.steps}</li>}
                    </ul>
                  </td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>{tc.expected_result}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
