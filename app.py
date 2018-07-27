from flask import Flask, render_template, url_for, request
import requests
import json
#------------------------------------------------------------------------------------#
app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

# Later you should rearrange and split according to desktop and mobile

@app.route("/testresults", methods = ['POST'])
def hello_world():

    #testurl = "https://cdnetworks.com"
    testurl = request.form['testurl']

    request_url_mobile = "https://www.googleapis.com/pagespeedonline/v4/runPagespeed?url=" + testurl + "&strategy=mobile&key=AIzaSyDplKio3HHteEPFPN-fkDquFeHKVodlJBw"
    request_url_desktop = "https://www.googleapis.com/pagespeedonline/v4/runPagespeed?url=" + testurl + "&strategy=desktop&key=AIzaSyDplKio3HHteEPFPN-fkDquFeHKVodlJBw"

    url = requests.get(request_url_mobile)
    url2 = requests.get(request_url_desktop)
    
    mobiledata = json.loads(url.text)
    desktopdata = json.loads(url2.text)

    browser_caching = []

#Checking the main details
    try:
        title = mobiledata["title"]
        mobile_opt_score = str(mobiledata["ruleGroups"]["SPEED"]["score"]) + "/100"
        desktop_opt_score = str(desktopdata["ruleGroups"]["SPEED"]["score"]) + "/100"
        loading_dist_mobile = mobiledata["loadingExperience"]["metrics"]["FIRST_CONTENTFUL_PAINT_MS"]["median"]
        loading_dist_desktop = desktopdata["loadingExperience"]["metrics"]["FIRST_CONTENTFUL_PAINT_MS"]["median"]
        
    except KeyError:
        title = "N/A"
        mobile_opt_score = "N/A"
        desktop_opt_score = "N/A"
        loading_dist_mobile = "N/A"
        loading_dist_desktop = "N/A"

#Checking specific for image optimization  
    try:
        file_size_savings = "You can reduce your website's images by " + mobiledata["formattedResults"]["ruleResults"]["OptimizeImages"]["urlBlocks"][0]["header"]["args"][1]["value"]
        img_opt = "(" + mobiledata["formattedResults"]["ruleResults"]["OptimizeImages"]["urlBlocks"][0]["header"]["args"][2]["value"] + " reduction)."
    except KeyError:
         file_size_savings = "Your images are fully optimized."
         img_opt = ""
    
#Checking specific for Leverage Browser Caching
    try:
        for key in mobiledata["formattedResults"]["LeverageBrowserCaching"]["urlBlocks"][0]["urls"]:
            browser_caching.append(mobiledata["formattedResults"]["LeverageBrowserCaching"]["urlBlocks"][0]["urls"][key]["result"]["args"][0]["value"])
    except KeyError:
         browser_caching = "You are already fully leveraging on browser caching."


    return render_template ("result.html",
    name=testurl, title=title, desktop_opt_score=desktop_opt_score, mobile_opt_score=mobile_opt_score, loading_dist_desktop=loading_dist_desktop, loading_dist_mobile=loading_dist_mobile, file_size_savings=file_size_savings, img_opt=img_opt,browser_caching=browser_caching)
    


if __name__ == "__main__":
    app.run()