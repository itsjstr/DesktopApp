import carball

import os
from flask import Flask, flash, request, redirect, url_for, request
from werkzeug.utils import secure_filename
from google.protobuf.json_format import MessageToJson
import json

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['replay', 'replay'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

app = Flask(__name__)

@app.route("/")
def load():
    return open("./html/home.html", "r").read()
@app.route("/end")
def end():
    shutdown_server()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

	
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        template = """
        <table class="table">
            <thead>
                <tr>
                    <th scope="col">Player</th>
                    <th scope="col">Score</th>
                    <th scope="col">Goals</th>
                    <th scope="col">Assists</th>
                    <th scope="col">Saves</th>
                    <th scope="col">Shots</th>
                </tr>
            </thead>
            <tbody>
                {add-here}
            </tbody>
        </table>
        """
        addable = """
        <tr>
            <th scope="row">{name}</th>
            <td>{score}</td>
            <td>{goals}</td>
            <td>{assists}</td>
            <td>{saves}</td>
            <td>{shots}</td>
        </tr>
        """

        o_created = []
        b_created = []

        f = request.files['file']
        f.save(secure_filename(f.filename))
        manager = carball.analyze_replay_file("./"+f.filename, 
                                      output_path="./replays/"+f.filename.replace(".replay", ".json"), 
                                      overwrite=True)
        proto_game = manager.get_protobuf_data()
        jsonObj = MessageToJson(proto_game)
        file = open("./replays/out-"+f.filename.replace(".replay", ".json"), "w")
        file.write(jsonObj)
        file.close()

        raw_json_file = open("./replays/out-"+f.filename.replace(".replay", ".json"), "r")
        raw_json = raw_json_file.read()
        raw_json_file.close()

        html_file = open("./html/stats.html", "r");
        html_unparsed = html_file.read()
        html_file.close()

        json_loaded = json.loads(raw_json)

        for i in range(0, len(json_loaded["players"])):
            arr = json_loaded["players"]
            x = addable.replace("{name}", arr[i]["name"])
            x = x.replace("{score}", str(arr[i]["score"]))
            x = x.replace("{goals}", str(arr[i]["goals"]))
            x = x.replace("{assists}", str(arr[i]["assists"]))
            x = x.replace("{saves}", str(arr[i]["saves"]))
            x = x.replace("{shots}", str(arr[i]["shots"]))

            if arr[i]["isOrange"] == 0:
                b_created.append(x)
            else:
                o_created.append(x)
            x = ""

        o_joined = " ".join(o_created)
        b_joined = " ".join(b_created)

        holder1 = template.replace("{add-here}", o_joined)
        holder2 = template.replace("{add-here}", b_joined)

        y = html_unparsed.replace("{orange}", holder1)
        y = y.replace("{blue}", holder2)

        return y
    elif request.method == 'GET':
        return open("./html/choose.html", "r").read().replace("{replaceme}", open("./rendered.txt", "r").read())

