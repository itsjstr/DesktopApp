import carball

import os
from flask import Flask, flash, request, redirect, url_for, request
from werkzeug.utils import secure_filename
from google.protobuf.json_format import MessageToJson

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
        f = request.files['file']
        f.save(secure_filename(f.filename))
        manager = carball.analyze_replay_file("./"+f.filename, 
                                      output_path="./"+f.filename.replace(".replay", ".json"), 
                                      overwrite=True)
        proto_game = manager.get_protobuf_data()
        jsonObj = MessageToJson(proto_game)
        file = open("output.json", "w")
        file.write(jsonObj)
        file.close()
        return 'file uploaded successfully'
    elif request.method == 'GET':
        return """
        <html>
            <body>
                <form action = "http://localhost:5000/upload" method = "POST" 
                    enctype = "multipart/form-data">
                    <input type = "file" name = "file" />
                    <input type = "submit"/>
                </form>
            </body>
        </html>
        """

