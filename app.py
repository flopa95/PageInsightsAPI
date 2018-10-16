from flask import Flask, render_template, url_for, request
import requests
import json
import pagespeed
#import plotly
#plotly.tools.set_credentials_file(username='cweitay93', api_key='Cim7dHbWiCO8p7xatCRD')
#------------------------------------------------------------------------------------#
app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

# Later you should rearrange and split according to desktop and mobile

@app.route("/testresults", methods = ['POST'])
def test_results():

    #testurl = "https://cdnetworks.com"
    testurl = request.form['testurl'] 

    if testurl.startswith("http://") | testurl.startswith("https://"):
        testurl = testurl
    else:
        testhttps = requests.get("https://" + testurl)
        if testhttps.status_code == 200:   
            testurl = "https://" + testurl
        else:
            testurl = "http://" + testurl

    pagespeed_obj = pagespeed.pagespeedapi(testurl)

    gzip_enabled = ""
    if "You have compression enabled" in pagespeed_obj.desktop_result["ruleResults"]["EnableGzipCompression"]["summary"]["format"]:
        gzip_enabled = "You have gzip compression enabled."
    else:
        gzip_enabled = "Gzip compression not enabled. " + pagespeed_obj.desktop_result["ruleResults"]["EnableGzipCompression"]["summary"]["format"] + " " + \
        pagespeed_obj.desktop_result["ruleResults"]["EnableGzipCompression"]["urlBlocks"][0]["header"]["format"]

    server_response = ""
    if "Your server responded quickly" in pagespeed_obj.desktop_result["ruleResults"]["MainResourceServerResponseTime"]["summary"]["format"]:
        server_response = "Your server responded quickly."
    else:
        server_response = pagespeed_obj.desktop_result["ruleResults"]["MainResourceServerResponseTime"]["summary"]["format"]

    #Checking specific for Leverage Browser Caching
    browser_caching = []
    try:
        for result in pagespeed_obj.desktop_result["LeverageBrowserCaching"]["urlBlocks"][0]["urls"]:
            browser_caching.append(result["result"]["args"][0]["value"])
    except KeyError:
         browser_caching = "You are already fully leveraging on browser caching."

    #Checking specific for image optimization  
    try:
        file_size_savings = "You can reduce your website's images by " + pagespeed_obj.mobile_result["ruleResults"]["OptimizeImages"]["urlBlocks"][0]["header"]["args"][1]["value"]
        img_opt = "(" + pagespeed_obj.mobile_result["ruleResults"]["OptimizeImages"]["urlBlocks"][0]["header"]["args"][2]["value"] + " reduction)."
    except KeyError:
         file_size_savings = "Your images are fully optimized."
         img_opt = ""
    
    return render_template ("result.html",
        name=testurl, 
        title=pagespeed_obj.title, 
        desktop_opt_score=pagespeed_obj.desktop_score, 
        mobile_opt_score=pagespeed_obj.mobile_score, 
        loading_dist_desktop=pagespeed_obj.desktop_load, 
        loading_dist_mobile=pagespeed_obj.mobile_load,
        gzip_compression=gzip_enabled,
        server_response=server_response,
        file_size_savings=file_size_savings, 
        img_opt=img_opt,
        browser_caching=browser_caching,
        results=pagespeed_obj.desktop_result["ruleResults"]
    )

if __name__ == "__main__":
    app.run()