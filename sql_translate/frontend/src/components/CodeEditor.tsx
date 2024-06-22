import { useEffect, useRef, useState } from "react";
import { Editor } from "@monaco-editor/react";
import DialectSelector from "./DialectSelector";

const CodeEditor = () => {
  const editorRef = useRef<any>(null);
  const [sql, setSQL] = useState<string>("select * from table");
  const [translatedSQL, setTranslatedSQL] = useState<string>("");
  const [fromDialect, setFromDialect] = useState<string>("mysql");
  const [toDialect, setToDialect] = useState<string>("postgres");

  const onMount = (editor: any) => {
    editorRef.current = editor;
    editor.focus();
  };

  const handleDialectSelectFrom = (dialect: string) => {
    setFromDialect(dialect);
  };

  const handleDialectSelectTo = (dialect: string) => {
    setToDialect(dialect);
  };

  const handleTranslateClick = async () => {
    console.log("Translate button clicked");
    console.log("SQL input:", sql);
    if (sql) {
      try {
        const response = await fetch("http://localhost:8000/translate", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            sql: sql,
            from_dialect: fromDialect,
            to_dialect: toDialect,
            options: {},
          }),
        });
        if (response.ok) {
          const data = await response.json();
          console.log("Translation response:", data);
          // Assuming the translated SQL is in data.sql
          if (data.sql) {
            setTranslatedSQL(data.sql);
          } else {
            console.error("Translated SQL is missing in the response");
          }
        } else {
          console.error("Translation request failed:", response.statusText);
        }
      } catch (err) {
        console.log("Translation error:", err);
      }
    } else {
      console.log("SQL input is empty");
    }
  };

  return (
    <div style={{ display: "flex", justifyContent: "center", padding: "1%" }}>
      <div style={{ width: "40%" }}>
        <div
          style={{ marginBottom: "5px", display: "flex", alignItems: "center" }}
        >
          <span
            style={{ marginRight: "10px", fontFamily: "'Arial', sans-serif" }}
          >
            From Dialect:
          </span>
          <DialectSelector
            onSelect={handleDialectSelectFrom}
            defaultValue={fromDialect}
          />
        </div>
        <div style={{ border: "1px solid grey" }}>
          <Editor
            height="75vh"
            width="100%"
            defaultLanguage="sql"
            defaultValue="select * from table"
            theme="light"
            onMount={onMount}
            value={sql}
            onChange={(value) => setSQL(value ?? "")}
            options={{
              minimap: { enabled: false },
              overviewRulerLanes: 0, // Disable the vertical overview ruler
            }}
          />
        </div>
      </div>
      <div style={{ alignSelf: "center", padding: "0 5px", margin: "0" }}>
        <button
          onClick={handleTranslateClick}
          style={{ padding: "10px 20px", margin: "0" }}
        >
          Translate
        </button>
      </div>
      <div style={{ width: "40%" }}>
        <div
          style={{ marginBottom: "5px", display: "flex", alignItems: "center" }}
        >
          <span
            style={{ marginRight: "10px", fontFamily: "'Arial', sans-serif" }}
          >
            To Dialect:
          </span>
          <DialectSelector
            onSelect={handleDialectSelectTo}
            defaultValue={toDialect}
          />
        </div>
        <div style={{ border: "1px solid grey" }}>
          <Editor
            height="75vh"
            width="100%"
            defaultLanguage="sql"
            value={translatedSQL}
            theme="light"
            options={{
              minimap: { enabled: false },
              overviewRulerLanes: 0, // Disable the vertical overview ruler
              readOnly: true, // Make this editor read-only
            }}
          />
        </div>
      </div>
    </div>
  );
};

export default CodeEditor;
