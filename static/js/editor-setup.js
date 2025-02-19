// Initialize input editor
const inputView = cm6.createEditorView(
  undefined,
  document.getElementById("input-editor")
);

const htmxTarget = "#output-textarea-container"
const htmxEvent = "editor-changed"

const inputOptions = {
  oneDark: true,
  readOnly: false,
  htmxTarget: htmxTarget,
  htmxEvent: htmxEvent
};
const inputInitialState = cm6.createEditorState(
  // "select date_format(now(), '%Y-%m-%d') as formatted_date;",
  "select columna,columnb,columnc,columd from my_table where 1=1",
  inputOptions
);
inputView.setState(inputInitialState);

// Initialize output editor
const outputView = cm6.createEditorView(
  undefined,
  document.getElementById("output-editor")
);
const outputOptions = {
  oneDark: true,
  readOnly: true,
};
const outputInitialState = cm6.createEditorState(
  "",
  outputOptions
);
outputView.setState(outputInitialState);

// Function to handle the HTMX response
document.body.addEventListener("htmx:afterSwap", function (event) {
  if (event.target.id === "input-textarea-container") {
    const newOutputContent = document.getElementById("input-textarea").value;
    inputView.setState(cm6.createEditorState(newOutputContent, inputOptions));
    htmx.trigger(htmxTarget, htmxEvent);
  }
  if (event.target.id === "output-textarea-container") {
    const newOutputContent = document.getElementById("output-textarea").value;
    outputView.setState(cm6.createEditorState(newOutputContent, outputOptions));
  }
});
