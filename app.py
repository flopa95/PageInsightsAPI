from flask import Flask, render_template, url_for, request
import requests
import json
#------------------------------------------------------------------------------------#
app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/testresults",methods = ['POST'])
def hello_world():

    #testurl = "https://cdnetworks.com"
    testurl = request.form['text']
    request_url = "https://www.googleapis.com/pagespeedonline/v4/runPagespeed?url=" + testurl + "&strategy=mobile&key=yourkeyhere"

    url = requests.get(request_url)
    jsons = json.loads(url.text)

    return render_template ("result.html",
    name=testurl,
    title=jsons["title"],
    speed_score=str(jsons["ruleGroups"]["SPEED"]["score"]) + "/100",
    loading_dist=jsons["loadingExperience"]["metrics"]["FIRST_CONTENTFUL_PAINT_MS"]["median"],
    file_size_savings=jsons["formattedResults"]["ruleResults"]["OptimizeImages"]["urlBlocks"][0]["header"]["args"][1]["value"],
    img_opt=jsons["formattedResults"]["ruleResults"]["OptimizeImages"]["urlBlocks"][0]["header"]["args"][2]["value"])
    


if __name__ == "__main__":
    app.run()

