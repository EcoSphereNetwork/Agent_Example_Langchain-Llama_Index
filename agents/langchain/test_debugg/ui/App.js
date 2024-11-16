import React, { useState } from "react";
import axios from "axios";

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [logs, setLogs] = useState([]);

  const handleQuery = async () => {
    try {
      const res = await axios.post("http://localhost:5000/api/query", { query });
      setResponse(res.data.response);
    } catch (err) {
      console.error("Error:", err);
      setResponse("Error occurred while processing the query.");
    }
  };

  const fetchLogs = async () => {
    try {
      const res = await axios.get("http://localhost:5000/api/logs");
      setLogs(res.data);
    } catch (err) {
      console.error("Error:", err);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Multi-Agent Assistant</h1>
      <div>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your query"
          style={{ padding: "10px", width: "300px" }}
        />
        <button onClick={handleQuery} style={{ padding: "10px", marginLeft: "10px" }}>
          Submit
        </button>
      </div>
      <h2>Response:</h2>
      <p>{response}</p>
      <button onClick={fetchLogs} style={{ padding: "10px", marginTop: "20px" }}>
        Fetch Logs
      </button>
      <h2>Logs:</h2>
      <pre style={{ backgroundColor: "#f4f4f4", padding: "10px", overflowX: "auto" }}>
        {JSON.stringify(logs, null, 2)}
      </pre>
    </div>
  );
}

export default App;
