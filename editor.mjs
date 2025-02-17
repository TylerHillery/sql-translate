// editor.js
import { basicSetup } from "codemirror";
import { EditorView } from "@codemirror/view";
import { EditorState } from "@codemirror/state";
import { sql } from "@codemirror/lang-sql";
import { oneDark } from "@codemirror/theme-one-dark";

let input_editor = new EditorView({
  extensions: [basicSetup, sql(), oneDark],
  parent: document.getElementById("input-editor"),
});

let output_editor = new EditorView({
  extensions: [basicSetup, sql(), oneDark, EditorState.readOnly.of(true)],
  parent: document.getElementById("output-editor"),
});
