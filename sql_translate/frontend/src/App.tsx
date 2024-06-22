import CodeEditor from "./components/CodeEditor";

function App() {
  return (
    <div className="App">
      <div style={{ textAlign: "center", marginBottom: "20px" }}>
        <img
          src="megaphone.svg"
          alt="Megaphone"
          style={{ height: "50px", verticalAlign: "middle" }}
        />
        <h1
          style={{
            display: "inline",
            marginLeft: "10px",
            verticalAlign: "middle",
            fontFamily: "'Arial', sans-serif", // Set the font family here
          }}
        >
          SQL Translator
        </h1>
        <p style={{ marginTop: "10px", fontFamily: "'Arial', sans-serif" }}>
          Translate between various SQL dialects
        </p>
      </div>
      <CodeEditor />
    </div>
  );
}

export default App;
