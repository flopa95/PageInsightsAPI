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
    request_url_mobile = "https://www.googleapis.com/pagespeedonline/v4/runPagespeed?url=" + testurl + "&strategy=mobile&key=AIzaSyDplKio3HHteEPFPN-fkDquFeHKVodlJBw"
    request_url_desktop = "https://www.googleapis.com/pagespeedonline/v4/runPagespeed?url=" + testurl + "&strategy=desktop&key=AIzaSyDplKio3HHteEPFPN-fkDquFeHKVodlJBw"

    url = requests.get(request_url_mobile)
    url2 = requests.get(request_url_desktop)
    
    mobiledata = json.loads(url.text)
    desktopdata = json.loads(url2.text)

#Checking the main details
    try:
        title = mobiledata["title"]
        mobile_speed_score = str(mobiledata["ruleGroups"]["SPEED"]["score"]) + "/100"
        loading_dist = mobiledata["loadingExperience"]["metrics"]["FIRST_CONTENTFUL_PAINT_MS"]["median"]
        
    except KeyError:
        title = "N/A"
        mobile_speed_score = "N/A"
        loading_dist = "N/A"

#Checking specific for image optimization      
    try:
        file_size_savings = "You can reduce your website's images by " + mobiledata["formattedResults"]["ruleResults"]["OptimizeImages"]["urlBlocks"][0]["header"]["args"][1]["value"]
        img_opt = "(" + mobiledata["formattedResults"]["ruleResults"]["OptimizeImages"]["urlBlocks"][0]["header"]["args"][2]["value"] + " reduction)."
    except KeyError:
         file_size_savings = "Your images are fully optimized."
         img_opt = ""
    


    return render_template ("result.html",
    name=testurl, title=title, mobile_speed_score=mobile_speed_score, loading_dist=loading_dist, file_size_savings=file_size_savings, img_opt=img_opt)
    


if __name__ == "__main__":
    app.run()

