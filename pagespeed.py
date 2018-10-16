import requests
import json
import unittest

class pagetest(object):
    def __init__(self, title, desktop_score, mobile_score, desktop_load, mobile_load, desktop_result, mobile_result):
        self.title = title
        self.desktop_score = desktop_score
        self.desktop_load = desktop_load
        self.desktop_result = desktop_result

        self.mobile_score = mobile_score
        self.mobile_load = mobile_load
        self.mobile_result = mobile_result
    pass


def pagespeedapi(page_url):
    api_key = 'AIzaSyDplKio3HHteEPFPN-fkDquFeHKVodlJBw'
    
    desktop_url = 'https://www.googleapis.com/pagespeedonline/v4/runPagespeed?url=' + page_url + '&filter_third_party_resources=true&screenshot=false&strategy=desktop&key=' + api_key
    desktop_req = requests.get(desktop_url)
    mobile_url = 'https://www.googleapis.com/pagespeedonline/v4/runPagespeed?url=' + page_url + '&filter_third_party_resources=true&screenshot=false&strategy=mobile&key=' + api_key
    mobile_req = requests.get(mobile_url)
    
    desktop_res_content = desktop_req.text
    mobile_res_content = mobile_req.text
    desktop_json_content = json.loads(desktop_res_content)
    mobile_json_content = json.loads(mobile_res_content)
    
    return pagetest(desktop_json_content["title"],
        desktop_json_content["ruleGroups"]["SPEED"]["score"],
        mobile_json_content["ruleGroups"]["SPEED"]["score"],
        desktop_json_content["loadingExperience"]["metrics"]["FIRST_CONTENTFUL_PAINT_MS"]["median"],
        mobile_json_content["loadingExperience"]["metrics"]["FIRST_CONTENTFUL_PAINT_MS"]["median"],
        desktop_json_content["formattedResults"],
        mobile_json_content["formattedResults"])
