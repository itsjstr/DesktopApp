const electron = require("electron");
const request = require("request");

let {BrowserWindow} = electron;
let {app} = electron;

app.on("ready", () => {
    let win = new BrowserWindow({
        width: 800,
        height: 600
    })
    win.loadURL("http://127.0.0.1:5000");
    win.show();
    win.on("closed", () => {
        request("http://127.0.0.1:5000/end")
        win = null;
    })
})