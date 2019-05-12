let backup;
let returnable = [];
let baseStr = '<div id="replay"><span id="name"><input id="val-{}" value="[fullpath]" /><br>Date Modified: {time}</span><span class="{}" id="right"><button id="download" onclick="select(this)">Select</button></span></div><hr>';
const homedir = require('os').homedir();
const fs = require("fs");
const settings = JSON.parse(fs.readFileSync(__dirname+"\\settings.json", "utf8"));
let path = homedir+settings.replays_path
fs.readdir(path, (err, items) => {
    backup = [...items];
    console.log(backup)
    for (let i = 0; i < items.length; i++) {
        let stats = fs.statSync(homedir+settings.replays_path+"\\"+backup[i].replace(".replay", "")+".replay")
        let x = baseStr.replace("[fullpath]", path+"\\"+items[i]);
        x = x.replace("{}", backup[i].replace(".replay", ""))
        x = x.replace("{}", backup[i].replace(".replay", ""))
        x = x.replace("{time}", stats.mtime)
        x = x.replace("{replayname}", backup[i].replace(".replay", ""))
        returnable.push(x)
    }
    fs.writeFileSync("./rendered.txt", returnable.join(""))
})