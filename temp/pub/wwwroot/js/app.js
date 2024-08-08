

// Desc: Configures requirejs to load monaco-editor
require.config({
    paths: {
        vs: '/monaco-editor/vs'
    }
});

// todo: probably need a map of editors
editor = null;


window.loadMonaco = (id, language, codeText) => {
    // Desc: Loads monaco-editor
    console.log("loading monaco-editor");
    require(['vs/editor/editor.main'], function () {
        editor = monaco.editor.create(document.getElementById(id), {
            value: codeText,
            language: language,
            automaticLayout: true,
            theme: "vs-dark"
        });

        editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, function () {
            console.log("Ctrl+Enter pressed");
            // todo: send code to server
        });
    });
}

window.getMonacoText = () => {
    return editor.getValue();
}

// file downloads

// funciton that initiates file download in the browser
// accepts two arguments - filename and string data
window.downloadFile = (filename, data) => {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(data));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}