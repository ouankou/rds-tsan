from flask import Flask, request, render_template, redirect, Response
from subprocess import PIPE, run
import flask
import os
import json
import subprocess
import time
from werkzeug import secure_filename
import logjson
UPLOAD_FOLDER = '/tmp/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def api_root():
    return render_template('index.html', val="")


# benchmark API for TSan
@app.route('/benchmark', methods=['POST'])
def benchmark():
    print("request received")

    # Running first command
    cmd = "sh /home/rds/dataracebench/check-data-races.sh"
    tstart = time.time()
    result = run(cmd.split(),
                 stdout=PIPE,
                 stderr=subprocess.STDOUT,
                 universal_newlines=True)
    tend = time.time()
    benchmarkTime = tend - tstart
    print(benchmarkTime)
    if (result.returncode == 1):
        str = result.stderr
    else:
        str = result.stdout
    print(str)

    with open(os.path.join(app.config['UPLOAD_FOLDER'], "tsanbenchmark.txt"),
              "w") as tsanfile:
        print("Benchmark time: ", benchmarkTime, file=tsanfile)
    return flask.make_response(flask.jsonify({'tsan': json.loads(str)}), 200)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    name = ""
    if request.method == "POST":
        if 'file' in request.files:
            f = request.files['file']
            if not f:
                print("file is empty")
                name = ""
            else:
                # f.save(secure_filename(f.filename))
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                name = f.filename
        else:
            name = ""
        print(name)
        cmd_list = [
            "cp " + os.path.join(app.config['UPLOAD_FOLDER'], name) + " /home/rds/dataracebench/micro-benchmarks/.",
            "/home/rds/dataracebench/scripts/test-harness.sh -d 32 -x tsan-clang"
         ]
        '''
        cmd_list = [
            "clang " + os.path.join(app.config['UPLOAD_FOLDER'], name) +
            " -fopenmp -fsanitize=thread -fPIE -pie -g -o " +
            os.path.join(app.config['UPLOAD_FOLDER'], "myApp"),
            os.path.join(app.config['UPLOAD_FOLDER'], "myApp")
        ]
        '''
        for cmd in cmd_list:
            result = run(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        if result.returncode == 1:
            output = result.stderr
        else:
            output = result.stdout
        #print(output)
        if not output:
            output = '{}'
        jsonResult = logjson.jsonify("/home/rds/dataracebench/result/log/" + name + "parser.log")
        if request.args.get('type') == 'json':
            return flask.make_response(jsonResult, 200)
        else:
            return render_template('index.html', val=str.split('\n'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
