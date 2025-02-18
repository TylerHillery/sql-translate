// Initialize input editor
const inputView = cm6.createEditorView(undefined, document.getElementById("input-editor"));
const inputOptions = {
    oneDark: true,
    readOnly: false,
    htmxTarget: "#output-textarea-container",
    htmxEvent: "editor-changed"
};
const inputInitialState = cm6.createEditorState("select * from table", inputOptions);
inputView.setState(inputInitialState);

// Initialize output editor
const outputView = cm6.createEditorView(undefined, document.getElementById("output-editor"));
const outputOptions = {
    oneDark: true,
    readOnly: true
};
const outputInitialState = cm6.createEditorState("", outputOptions);
outputView.setState(outputInitialState);

// Function to handle the HTMX response
document.body.addEventListener('htmx:afterSwap', function (event) {
    if (event.target.id === "output-textarea-container") {
        const newOutputContent = document.getElementById('output-textarea').value;
        outputView.setState(cm6.createEditorState(newOutputContent, outputOptions));
    }
});
