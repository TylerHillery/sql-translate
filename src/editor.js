import { basicSetup } from "codemirror";
import { indentWithTab } from "@codemirror/commands";
import { drawSelection, EditorView, keymap } from "@codemirror/view";
import { EditorState } from "@codemirror/state";

// Theme
import { oneDark } from "@codemirror/theme-one-dark";

// Language
import { sql } from "@codemirror/lang-sql";

function createEditorState(initialContents, options = {}) {
  let extensions = [basicSetup, keymap.of([indentWithTab]), sql()];

  if (options.oneDark) extensions.push(oneDark);

  // read only extensions
  if (options.readOnly) {
    extensions.push(EditorState.readOnly.of(true));
    extensions.push(drawSelection({ cursorBlinkRate: 0 }));
  }

  if (options.htmxTarget && options.htmxEvent) {
    const updateListener = EditorView.updateListener.of((update) => {
      if (update.docChanged) {
        const editorContents = update.state.doc.toString();
        htmx.trigger(options.htmxTarget, options.htmxEvent, {
        // TODO: figure out how to access htmx event object in hx-vals
          sql: editorContents,
        });
      }
    });
    extensions.push(updateListener);
  }

  return EditorState.create({
    doc: initialContents,
    extensions,
  });
}

function createEditorView(state, parent) {
  return new EditorView({ state, parent });
}

export { createEditorState, createEditorView };
