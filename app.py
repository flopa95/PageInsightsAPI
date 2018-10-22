from flask import Flask, render_template, url_for, request, Response, session
import io
import requests
import json
import pagespeed
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)
app.secret_key = 'a3MhfHH4UBhz0FI45dSM'

@app.route("/")
def main():
    if session.get('dist', None):
        session.pop('dist', None)
    return render_template("index.html")

# Later you should rearrange and split according to desktop and mobile

@app.route("/testresults", methods = ['POST'])
def test_results():

    # Test URL for https
    testurl = request.form['testurl']
    try:
        if testurl.startswith("http://") | testurl.startswith("https://"):
            testurl = testurl
        else:
            testhttps = requests.get("https://" + testurl)
            if testhttps.status_code == 200:   
                testurl = "https://" + testurl
            else:
                testurl = "http://" + testurl
    except requests.exceptions.RequestException:
        return render_template ("error.html")

    # Pagespeed API
    pagespeed_obj = pagespeed.pagespeedapi(testurl)

    # Gzip Compression
    gzip_enabled = ""
    try:
        if "You have compression enabled" in pagespeed_obj.desktop_result["ruleResults"]["EnableGzipCompression"]["summary"]["format"]:
            gzip_enabled = "You have gzip compression enabled."
        else:
            gzip_enabled = pagespeed.format_string(pagespeed_obj.desktop_result["ruleResults"]["EnableGzipCompression"]["urlBlocks"][0]["header"]) \
            + "<br><details style='font-size:14px;max-width:480px;overflow-wrap:break-word;word-wrap:break-word;'><summary>Show/Hide</summary><div class='scrollable'><ul>"
            for item in pagespeed.list_urls(pagespeed_obj.desktop_result["ruleResults"]["EnableGzipCompression"]["urlBlocks"][0]["urls"]):
                gzip_enabled += "<li>" + item + "</li>"
            gzip_enabled += "</ul></div></details>"
    except KeyError:
        gzip_enabled = "No gzip compression found."

    # Server Response Speed
    server_response = ""
    try:
        if  "Your server responded quickly" in pagespeed_obj.desktop_result["ruleResults"]["MainResourceServerResponseTime"]["summary"]["format"]:
            server_response = "Your server responded quickly."
        else:
            server_response = pagespeed.format_string(pagespeed_obj.desktop_result["ruleResults"]["MainResourceServerResponseTime"]["summary"])
    except KeyError:
        server_response = "Some error occurred. Server response not recorded."
        
    #Checking specific for image optimization  
    optimize_image = ""
    try:
        if pagespeed_obj.desktop_result["ruleResults"]["OptimizeImages"]["urlBlocks"]:
            optimize_image = pagespeed.format_string(pagespeed_obj.desktop_result["ruleResults"]["OptimizeImages"]["urlBlocks"][0]["header"]) \
            + "<br><details style='font-size:14px;max-width:480px;overflow-wrap:break-word;word-wrap:break-word;'><summary>Show/Hide</summary><div class='scrollable'><ul>"
            for item in pagespeed.list_urls(pagespeed_obj.desktop_result["ruleResults"]["OptimizeImages"]["urlBlocks"][0]["urls"]):
                optimize_image += "<li>" + item + "</li>"
            optimize_image += "</ul></div></details>"
    except KeyError:
        optimize_image = "Your images are fully optimized."

    # Checking specific for Leverage Browser Caching
    browser_caching = "<p><b>"
    try:
        if pagespeed_obj.desktop_result["ruleResults"]["LeverageBrowserCaching"]["urlBlocks"]:
            browser_caching += pagespeed.format_string(pagespeed_obj.desktop_result["ruleResults"]["LeverageBrowserCaching"]["urlBlocks"][0]["header"]) \
            + "</b></p><details style='font-size:14px;max-width:640px;overflow-wrap:break-word;word-wrap:break-word;'><summary>Show/Hide</summary><div class='scrollable'><ul>"
            for item in pagespeed.list_urls(pagespeed_obj.desktop_result["ruleResults"]["LeverageBrowserCaching"]["urlBlocks"][0]["urls"]):
                browser_caching += "<li>" + item + "</li>"
            browser_caching += "</ul></div></details>"
    except KeyError:
        browser_caching ="<p><b>You are already fully leveraging on browser caching.</b></p>"

    distribution = []
    for i in range(3):
        inner_dist = []
        inner_dist.append(pagespeed_obj.desktop_load["FIRST_CONTENTFUL_PAINT_MS"]
        ["distributions"][i]["proportion"])
        inner_dist.append(pagespeed_obj.desktop_load["DOM_CONTENT_LOADED_EVENT_FIRED_MS"]
        ["distributions"][i]["proportion"])
        distribution.append(inner_dist)

    session['dist'] = distribution

    return render_template ("result.html",
        name=testurl, 
        title=pagespeed_obj.title, 
        desktop_opt_score=pagespeed_obj.desktop_score, 
        mobile_opt_score=pagespeed_obj.mobile_score, 
        loading_dist_desktop=round(pagespeed_obj.desktop_load["FIRST_CONTENTFUL_PAINT_MS"]["median"]/1000, 1), 
        loading_dist_mobile=round(pagespeed_obj.mobile_load["FIRST_CONTENTFUL_PAINT_MS"]["median"]/1000, 1),
        gzip_compression=gzip_enabled,
        server_response=server_response,
        file_size_savings=optimize_image,
        browser_caching=browser_caching
    )

@app.route('/plot.png')
def create_figure():
    #plt.style.use('fivethirtyeight')
    fig = plt.figure(figsize=(5,5))
    ax = plt.subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.25))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.05))
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0,symbol=None))
    distribution = session.get('dist', None)

    n = 2
    Fast = np.array(distribution[0])
    Normal = np.array(distribution[1])
    Slow = np.array(distribution[2])
    ind = np.arange(n)
    width = 0.35

    p1 = plt.bar(ind, Fast, width, color='#AAC210')
    p2 = plt.bar(ind, Normal, width, color='#FDA100', bottom=Fast)
    p3 = plt.bar(ind, Slow, width, color='#E10000', bottom=Fast+Normal)

    plt.xticks(ind,('FCP','DCL'))
    plt.ylabel('Proportion categorised by loading time', fontsize=12)
    plt.legend((p3, p2, p1), ('Slow', 'Average', 'Fast'))

    for r1, r2, r3 in zip(p1, p2, p3):
        h1 = r1.get_height()
        h2 = r2.get_height()
        h3 = r3.get_height()
        plt.text(r1.get_x() + r1.get_width() / 2., h1 / 2., "%d" % (h1*100) + "%", ha="center", va="center", color="white", fontsize=14, fontweight="bold")
        plt.text(r2.get_x() + r2.get_width() / 2., h1 + h2 / 2., "%d" % (h2*100) + "%", ha="center", va="center", color="white", fontsize=14, fontweight="bold")
        plt.text(r3.get_x() + r3.get_width() / 2., h1 + h2 + h3 / 2., "%d" % (h3*100) + "%", ha="center", va="center", color="white", fontsize=14, fontweight="bold")

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    plt.close('all')
    return Response(output.getvalue(), mimetype='image/png')

if __name__ == "__main__":
    app.run()