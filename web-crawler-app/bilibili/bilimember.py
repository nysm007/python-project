#-*-coding:utf-8 -*-

import sys
import json
import requests
import re
import datetime
import hashlib
import bilibili

TIME_OUT = 4
VERIFY_STATUS = True
APP_KEY = "13956944702616074536"


def get_member_info(vmid):
    url = "https://app.bilibili.com/x/v2/space?build=5800&vmid={0}".format(vmid)
    try:
        response = requests.get(url, timeout=TIME_OUT, verify=VERIFY_STATUS)
        info = json.loads(response.text)
    except Exception as e:
        return None
    
    if info['code'] < 0:
        if info['code'] == -503:
            try:
                info = json.loads(requests.get(url, timeout=TIME_OUT, verify=VERIFY_STATUS).text)
            except Exception as e:
                return None
            if info['code'] < 0:
                return None
        else:
            # print "Code < 0 and != 503. " + url
            return None
    try:
        update_card(info, vmid)
        update_bangumi(info, vmid)
    except Exception as e:
        f = open("UpdateError.log", 'a')
        f.write("[Error] {0} {1} {2}\n".format(str(datetime.datetime.now()), str(e), url ))
        f.flush()
        f.close()
    
    if __name__ == "__main__":
        now = re.sub(r"[(:\ )]", '-', str(datetime.datetime.now())[0:16])
        file_name = "member-{0}.json".format(now)
        with open ("./{0}".format(file_name), "w") as f:
            json.dump(info, f)
     
    return info

def get_member_info_lite(vmid):
    # starttime = datetime.datetime.now()
    try:
        lite_info = get_member_info(vmid)['data']
    except TypeError as e:
        return None

    # print "Time consumed: {0} seconds.".format(str((datetime.datetime.now()-starttime).seconds))
    return lite_info


def get_json_response(base_url, page_num, mid):
    url = base_url.format(page_num, mid)
    url = url + "&sign={0}".format(bilibili.sign(url))
    try:
        return json.loads(requests.get(url, timeout=TIME_OUT, verify=VERIFY_STATUS).text)
    except Exception as e:
        return None

def update_bangumi(info, mid):
    info['data']['season'] = list()
    base_url = "http://bangumi.bilibili.com/api/get_concerned_season?_device=android&_hwid=a5ec35c7d2562a2d&appkey={}&build=408005&page={0}&pagesize=20&platform=android&taid={1}&ts=1498987277000"
    page_num = 1
    while(1):
        json_response = get_json_response(base_url, page_num, mid)
        if len(json_response['result']) != 0:
            info['data']['season'] += json_response['result']
            page_num += 1
        else:
            break
        
    return info['data']['season']


def update_card(info, mid):
    base_url = "https://account.bilibili.com/api/member/getCardByMid?_device=android&_hwid=a5ec35c7d2562a2d&appkey={}&build=408005&mid={0}&platform=android".format(mid)
    url = base_url + "&sign={0}".format(bilibili.sign(base_url))
    try:
        json_response = json.loads(requests.get(url, timeout=TIME_OUT, verify=VERIFY_STATUS).text)
        info['data']['card'] = json_response['card']
        update_fans(info, mid)
    except Exception as e:
        return None

    return info['data']['card']

def update_fans(info, mid):
    info['data']['card']['fans_detail'] = list()
    base_url = "https://account.bilibili.com/api/friend/fans?_device=android&_hwid=a5ec35c7d2562a2d&appkey={}&build=408005&mid={1}&page={0}&pagesize=100&platform=android"
    page_num = 1
    while(1):
        json_response = get_json_response(base_url, page_num, mid)
        try:
            info['data']['card']['fans_detail'] += json_response['list']
            page_num += 1
        except KeyError as e:
            break
    
    return info['data']['card']['fans_detail']


if __name__ == "__main__":
    print("Take user \"2554172\" as an example.")
    aa = get_member_info("2554172")

