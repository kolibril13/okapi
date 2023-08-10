import React, { useState, useEffect } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";

function App() {
  const [testData, setTestData] = useState(null);

  useEffect(() => {
    fetch("/TEST.json")
      .then((response) => response.json())
      .then((data) => setTestData(data))
      .catch((error) => console.error("There was an error!", error));
  }, []);

  return (
    <div>
      {testData && <pre>{JSON.stringify(testData, null, 2)}</pre>}
    </div>
  );
}

export default App;
