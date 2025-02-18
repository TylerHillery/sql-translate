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

  // write only extensions
  if (!options.readOnly) {
    const updateListener = EditorView.updateListener.of((update) => {
      if (update.docChanged) {
        htmx.trigger("#output-textarea-container", "editor-changed");
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
