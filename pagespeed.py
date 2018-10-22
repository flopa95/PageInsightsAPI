import requests
import json
import re

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
        desktop_json_content["loadingExperience"]["metrics"],
        mobile_json_content["loadingExperience"]["metrics"],
        desktop_json_content["formattedResults"],
        mobile_json_content["formattedResults"])

def format_string(json_obj):
    formatted_string = json_obj['format']
    for arg in json_obj['args']:
        if arg['type'] == "HYPERLINK":
            formatted_string = re.sub(r'\{\{BEGIN_LINK\}\}', '<a href="' + arg['value'] + '">', formatted_string)
            formatted_string = re.sub(r'\{\{END_LINK\}\}', '</a>', formatted_string)
        elif arg['key'] in formatted_string:
            formatted_string=re.sub(r'\{\{'+ arg['key'] + r'\}\}', "<b>" + arg['value'] + "</b>", formatted_string)
    return formatted_string

# TEST format_string()
#format_string(content['formattedResults'] \
#['ruleResults']['EnableGzipCompression'] \
#['urlBlocks'][0]['header'])

def list_urls(json_obj):
    url_list = []
    for result in json_obj:
        item_string = result['result']['format']
        for arg in result['result']['args']:
            if arg['key'] in item_string:
                item_string=re.sub(r'\{\{'+ arg['key'] + r'\}\}', arg['value'], item_string)
        url_list.append(item_string)    
    return (url_list)

# TEST list_urls()
#list_urls(content['formattedResults'] \
#['ruleResults']['EnableGzipCompression'] \
#['urlBlocks'][0]['urls'])
