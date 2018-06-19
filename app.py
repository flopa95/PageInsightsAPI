from flask import Flask, render_template, url_for, request
import requests
import json
#------------------------------------------------------------------------------------#
app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/login/<string:name>",methods = ['POST', 'GET'])
def hello_world(name):
    #x = name+"x"
    testurl = "https://cdnetworks.com"
    request_url = "https://www.googleapis.com/pagespeedonline/v4/runPagespeed?url=" + testurl + "&strategy=mobile&key=AIzaSyAsuAfkLwf8_qnzEMET8bH2BNLNhhntat4"

    url = requests.get(request_url)
    jsons = json.loads(url.text)
    #return jsons["title"]
    return render_template ("result.html", name=name, title=jsons["title"])















@app.route("/login",methods = ['POST', 'GET'])
def error_message():
    return "Please enter a domain that you would like to test!"


if __name__ == "__main__":
    app.run()

