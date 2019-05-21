# -*- coding: utf-8 -*-

# <a href="http://www.jobbole.com/members/dai745726163">@Time</a>   : 2017/3/28 8:46

# @Author : Lyrichu

# <a href="http://www.jobbole.com/members/Email">@Email</a>  : 919987476@qq.com

# @File   : NetCloud_spider3.py

'''

@Description:

网易云音乐评论爬虫，可以完整爬取整个评论

部分参考了@平胸小仙女的文章(地址:https://www.zhihu.com/question/36081767)

post加密部分也给出了，可以参考原帖：

作者：平胸小仙女

链接：https://www.zhihu.com/question/36081767/answer/140287795

来源：知乎

'''

from Crypto.Cipher import AES
import base64
import requests
import json
import codecs
import time

headers = {
    'Host':"music.163.com",
    'Accept-Language':"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    'Accept-Encoding':"gzip, deflate",
    'Content-Type':"application/x-www-form-urlencoded",
    'Cookie':"_ntes_nnid=754361b04b121e078dee797cdb30e0fd,1486026808627; _ntes_nuid=754361b04b121e078dee797cdb30e0fd; JSESSIONID-WYYY=yfqt9ofhY%5CIYNkXW71TqY5OtSZyjE%2FoswGgtl4dMv3Oa7%5CQ50T%2FVaee%2FMSsCifHE0TGtRMYhSPpr20i%5CRO%2BO%2B9pbbJnrUvGzkibhNqw3Tlgn%5Coil%2FrW7zFZZWSA3K9gD77MPSVH6fnv5hIT8ms70MNB3CxK5r3ecj3tFMlWFbFOZmGw%5C%3A1490677541180; _iuqxldmzr_=32; vjuids=c8ca7976.15a029d006a.0.51373751e63af8; vjlast=1486102528.1490172479.21; __gads=ID=a9eed5e3cae4d252:T=1486102537:S=ALNI_Mb5XX2vlkjsiU5cIy91-ToUDoFxIw; vinfo_n_f_l_n3=411a2def7f75a62e.1.1.1486349441669.1486349607905.1490173828142; P_INFO=m15527594439@163.com|1489375076|1|study|00&99|null&null&null#hub&420100#10#0#0|155439&1|study_client|15527594439@163.com; NTES_CMT_USER_INFO=84794134%7Cm155****4439%7Chttps%3A%2F%2Fsimg.ws.126.net%2Fe%2Fimg5.cache.netease.com%2Ftie%2Fimages%2Fyun%2Fphoto_default_62.png.39x39.100.jpg%7Cfalse%7CbTE1NTI3NTk0NDM5QDE2My5jb20%3D; usertrack=c+5+hljHgU0T1FDmA66MAg==; Province=027; City=027; _ga=GA1.2.1549851014.1489469781; __utma=94650624.1549851014.1489469781.1490664577.1490672820.8; __utmc=94650624; __utmz=94650624.1490661822.6.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; playerid=81568911; __utmb=94650624.23.10.1490672820",
    'Connection':"keep-alive",
    'Referer':'http://music.163.com/'
}

proxies= {
    'http:':'http://121.232.146.184',
    'https:':'https://144.255.48.197'
}

# offset的取值为:(评论页数-1)*20,total第一页为true，其余页为false
first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
second_param = "010001"
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
forth_param = "0CoJUm6Qyw8W8jud"

def get_params(page):    # iterate this page number to get all comments
    iv = "0102030405060708"
    first_key = forth_param
    second_key = 16 * 'F'
    if(page == 1):
        first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
        h_encText = AES_encrypt(first_param, first_key, iv)
    else:
        offset = str((page-1)*20)
        first_param = '{rid:"", offset:"%s", total:"%s", limit:"20", csrf_token:""}' %(offset,'false')
        h_encText = AES_encrypt(first_param, first_key, iv)

    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText

def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey

def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)

    return encrypt_text

def get_json(url, params, encSecKey):
    data = {
        "params": params,
        "encSecKey": encSecKey
    }

    response = requests.post(url, headers=headers, data=data,proxies = proxies)
    return response.content

def get_hot_comments(url):
    hot_comments_list = []
    hot_comments_list.append(u"User-ID User-Nickname User-Portrait Comment-Time Likes Content\n")
    params = get_params(1)    # first page
    encSecKey = get_encSecKey()

    json_text = get_json(url,params,encSecKey)
    json_dict = json.loads(json_text)
    hot_comments = json_dict['hotComments']

    print("[INFO] %d hot-comments in total." % len(hot_comments))

    for item in hot_comments:
            comment = item['content']
            likedCount = item['likedCount']
            comment_time = item['time']
            userID = item['user']['userID']    # commenter's id
            nickname = item['user']['nickname']
            avatarUrl = item['user']['avatarUrl']
            comment_info = userID + " " + nickname + " " + avatarUrl + " " + comment_time + " " + likedCount + " " + comment + u"\n"
            hot_comments_list.append(comment_info)

    return hot_comments_list

def get_all_comments(url):
    all_comments_list = []
    all_comments_list.append(u"User-ID User-Nickname User-Portrait Comment-Time Likes Content\n") # header's content 用户ID 用户昵称 用户头像地址 评论时间 点赞总数 评论内容
    params = get_params(1)
    encSecKey = get_encSecKey()
    json_text = get_json(url,params,encSecKey)
    json_dict = json.loads(json_text)
    comments_num = int(json_dict['total'])

    if(comments_num % 20 == 0):
        page = comments_num / 20
    else:
        page = int(comments_num / 20) + 1

    print("[INFO] %d pages of comment in total." % page)

    for i in range(page):
        params = get_params(i+1)
        encSecKey = get_encSecKey()
        json_text = get_json(url,params,encSecKey)
        json_dict = json.loads(json_text)
        if i == 0:
            print("[INFO] %d comments in total." % comments_num)
        for item in json_dict['comments']:
            comment = item['content']
            likedCount = item['likedCount']
            comment_time = item['time']
            userID = item['user']['userId']
            nickname = item['user']['nickname']
            avatarUrl = item['user']['avatarUrl']
            comment_info = unicode(userID) + u" " + nickname + u" " + avatarUrl + u" " + unicode(comment_time) + u" " + unicode(likedCount) + u" " + comment + u"\n"
            all_comments_list.append(comment_info)

        print("[INFO] %d pages have been processed sucessfully." % (i+1))

    return all_comments_list

def save_to_file(list,filename):
    with codecs.open(filename,'a',encoding='utf-8') as f:
        f.writelines(list)
    print("[INFO] Successfully writen to {}!".format(filename))

if __name__ == "__main__":
    start_time = time.time()
    url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_186016/?csrf_token="
    filename = u"晴天.txt"
    all_comments_list = get_all_comments(url)

    save_to_file(all_comments_list,filename)

    print("[INFO] Time consumed: {} seconds.".format(time.time() - start_time))

