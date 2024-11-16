import React, { useState, useEffect } from "react";
import axios from "axios";
import { io } from "socket.io-client";

const socket = io("http://localhost:5000");

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [logs, setLogs] = useState([]);
  const [realTimeLogs, setRealTimeLogs] = useState([]);

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

  useEffect(() => {
    socket.on("log_update", (data) => {
      setRealTimeLogs((prev) => [...prev, { file: data.file, lines: data.lines }]);
    });
    return () => socket.disconnect();
  }, []);

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
      <h2>Real-Time Log Updates:</h2>
      {realTimeLogs.map((log, index) => (
        <div key={index}>
          <h4>File: {log.file}</h4>
          <pre style={{ backgroundColor: "#f4f4f4", padding: "10px", overflowX: "auto" }}>
            {log.lines.join("")}
          </pre>
        </div>
      ))}
    </div>
  );
}

export default App;
