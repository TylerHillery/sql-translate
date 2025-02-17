// TODO:
// - Support Light & Dark Mode
import { basicSetup } from "codemirror";
import { indentWithTab } from "@codemirror/commands";
import { EditorView, keymap } from "@codemirror/view";
import { EditorState } from "@codemirror/state";
import { sql } from "@codemirror/lang-sql";
import { oneDark } from "@codemirror/theme-one-dark";

// TODO:
// - optional vim mode
let input_editor = new EditorView({
  extensions: [basicSetup, sql(), oneDark, keymap.of([indentWithTab])],
  parent: document.getElementById("input-editor"),
});

// TODO:
// - It's read only but cursor still blinks when editor is active
// - There should be an easy copy all button
let output_editor = new EditorView({
  extensions: [basicSetup, sql(), oneDark, EditorState.readOnly.of(true)],
  parent: document.getElementById("output-editor"),
});
