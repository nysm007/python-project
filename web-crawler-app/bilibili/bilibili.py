#-*-coding:utf-8 -*-

import sys
import hashlib
import requests
import json
import re
import time
import datetime
import urllib

APP_SCERET = "ea85624dfcf12d7cc7b2b3a94fac1f2c"
RETRY_TIMES = 5
TIMEOUT = 2
VERIFY_STATUS = True

def sign(base_url):
    if base_url.find('?') == -1:
        print("Warning: cannot verify this request pattern. Check {0}.".format(base_url))
    else:
        seed = base_url[base_url.find('?') + 1 : ] + APP_SCERET
    
    m = hashlib.md5()
    m.update(seed)
    return m.hexdigest()

def get_video_stat(vid):
    url = "http://api.bilibili.com/archive_stat/stat?aid={0}".format(vid)
    try:
        json_response = json.loads(requests.get(url, timeout=TIMEOUT, verify=VERIFY_STATUS).text)
    except Exception as e:
        return None
    try:
        return json_response['data']    #dict
    except Exception as e:
        return None



def get_video_recommend(vid):
    keep_list = ["aid", "duration"]
    url = "http://comment.bilibili.com/recommendnew,{0}".format(vid)
    try:
        json_response = json.loads(requests.get(url, timeout=TIMEOUT, verify=VERIFY_STATUS).text)
    except Exception as e:
        pass
    try:
        if len(json_response['data']) < 2:
            return None
        else:
            rec_list = list()
        return rec_list
    except Exception as e:
        return None

def get_json_response(url_base, page_num):
    url = url_base + str(page_num)
    response = requests.get(url, timeout=10, verify=VERIFY_STATUS)
    json_response = json.loads(response.text)
    return json_response

def bilibili_search(keyword, duration):
    coll = {'video':[], 'uploader':[], 'bangumi':[], 'movie':[]}
    url_base = "https://app.bilibili.com/x/v2/search?&keyword={0}&duration={1}&ps=20&pn="
    url_base = url_base.format(keyword, duration)
    page_num = 1

    while(1):
        json_form = get_json_response(url_base, page_num)

        if len(json_form['data']['items']) == 0:
            break
        else:
            coll.get('video').extend(json_form['data']['items']['archive'])

        page_num += 1

    coll.get('uploader').extend(get_type_detail(keyword, 2))
    coll.get('bangumi').extend(get_type_detail(keyword, 1))
    coll.get('movie').extend(get_type_detail(keyword, 3))

    now = re.sub(r"[(:\ )]", '-', str(datetime.datetime.now())[0:16])
    file_name = "{0}-{1}-{2}".format(urllib.unquote(keyword), duration, now)
    with open ("./{0}.json".format(file_name), "w") as f:
        json.dump(coll, f)

    return coll

def get_type_detail(keyword, type_id):
    url_base = "https://app.bilibili.com/x/v2/search/type?keyword={0}&ps=20&type={1}&pn="
    url_base = url_base.format(keyword, type_id)
    page_num = 1
    type_detail = list()

    while(1):
        json_form = get_json_response(url_base, page_num)
        try:
            if len(json_form['data']['items']) == 0:
                break
            else:
                type_detail.extend(json_form['data']['items'])
            page_num += 1
        except KeyError as e:
            # print "Invalid entry to this page! Check the page at {0}{1}.".format(url_base, page_num)
            break
    return type_detail

if __name__ == "__main__":
    print("This Python file should be used as an import library.")
