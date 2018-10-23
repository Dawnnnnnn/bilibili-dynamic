import requests
import hashlib
import time
import datetime
# keywords = ['抽奖','盖楼','抢楼','转发并评论','参与抽奖','参与活动','就有机会','本动态','此动态',"这条动态","开奖","'评论并转发'"]
# keywords = ['​动态互动抽奖','互动抽奖']
cookie = ""
access_key = ""
csrf = ""
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
    "Cookie": cookie
}
# def check(des):
#     for i in keywords:
#         if des.find(i) != -1:
#             return True


def modify(uid):
    url = "https://api.bilibili.com/x/relation/modify"
    data = {
        "fid":uid,
        "act":"1",
        "re_src":"11",
        "jsonp":"jsonp",
        "csrf":csrf
    }
    response = requests.post(url,data=data,headers=headers)
    print("关注状态:",response.json())

def repost(dynamic_id):
    temp_params = "access_key="+access_key+"&appkey=1d8b6e7d45233436&build=5260003&mobi_app=android&platform=android&src=meizu&trace_id=20180531235400023&ts=1527782063000&version=5.26.3.5260003"

    url = "https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/repost?access_key="+access_key+"&appkey=1d8b6e7d45233436&build=5260003&mobi_app=android&platform=android&src=meizu&trace_id=20180531235400023&ts=1527782063000&version=5.26.3.5260003&sign="+calc_sign(temp_params)
    headers={
        "User-Agent":"Mozilla/5.0 BiliDroid/5.26.3 (bbcallen@gmail.com)",
        "Host":"api.vc.bilibili.com"
    }
    data = {
        "uid":"48766812",
        "dynamic_id":"0",
        "type":"2",
        "rid":dynamic_id,
        "content":"@大姬八云紫@゚大鹏不想飞",
        "ctrl":'[{"data":"3453410","length":4,"location":0,"type":1},{"data":"240834777","length":5,"location":4,"type":1}]',
        "at_uids":"3453410,240834777",
        "spec_type":"0",
        "repost_code":"10000",
        "extension":"{}"
    }
    response = requests.post(url,headers=headers,data=data)
    print("转发状态：",response.json())

def calc_sign(str):
    str = str + "560c52ccd288fed045859ed18bffd973"
    hash = hashlib.md5()
    hash.update(str.encode('utf-8'))
    sign = hash.hexdigest()
    return sign

# //暂时废弃
# def doc2id(id):
#     temp_params = "_device=android&_hwid=SX1NL0wuHCsaKRt4BHhIfRguTXxOfj5WN1BkBTdLfhstTn9NfUouFiUV&access_key="+access_key+"&appkey=1d8b6e7d45233436&build=5260003&doc_id="+str(id)+"&mobi_app=android&platform=android&src=meizu&trace_id=20180531234300045&ts=1527781425&version=5.26.3.5260003"
#     url = "http://api.vc.bilibili.com/link_draw/v2/doc/dynamic_id?_device=android&_hwid=SX1NL0wuHCsaKRt4BHhIfRguTXxOfj5WN1BkBTdLfhstTn9NfUouFiUV&access_key="+access_key+"&appkey=1d8b6e7d45233436&build=5260003&doc_id="+str(id)+"&mobi_app=android&platform=android&src=meizu&trace_id=20180531234300045&ts=1527781425&version=5.26.3.5260003&sign="+calc_sign(temp_params)
#     headers={
#         "User-Agent":"Mozilla/5.0 BiliDroid/5.26.3 (bbcallen@gmail.com)",
#         "Host":"api.vc.bilibili.com"
#     }
#     response = requests.get(url,headers=headers)
#     dynamic_id = response.json()['data']['dynamic_id']
#     print(dynamic_id)
#     return dynamic_id

def helper(i):
    url = "https://api.vc.bilibili.com/link_draw/v1/doc/detail?doc_id=" + str(i)
    response = requests.get(url)
    if response.json()['code'] == 0:
        lottery = (response.json()['data']['item']['extension'])
        des = (response.json()['data']['item']['description'])
        format_lottery = eval(lottery)
        if len(format_lottery) >= 1:
            tmp = eval(format_lottery['lott_cfg'])
            title = tmp['title']
            uid = response.json()['data']['user']['uid']
            return title, des, uid
        else:
            title = "不符合规则的动态"
            des = "不符合规则的动态"
            uid = "不符合规则的动态"
            return title, des, uid
    elif response.json()['msg'] == "doc not found":
        title = "未找到id"
        des = "未找到id"
        uid = "未找到id"
        return title, des, uid
    else:
        title = "error"
        des = "error"
        uid = "error"
        return title,des,uid

def monitor():
    for i in range(5857780, 9000000):
        print(i)
        try:
            # url = "https://api.vc.bilibili.com/link_draw/v1/doc/detail?doc_id="+str(i)
            #             # response = requests.get(url)
            #             # lottery = (response.json()['data']['item']['extension'])
            #             # des = (response.json()['data']['item']['description'])
            #             # format_lottery = eval(lottery)
            #             # if len(format_lottery) >= 1:
            #             #     tmp = eval(format_lottery['lott_cfg'])
            #             #     title = tmp['title']
            data = helper(i)
            flag = 5
            while data[0] == "未找到id":
                if flag < 10:
                    print("休眠一下")
                    time.sleep(5)
                    print("休眠完成")
                    data = helper(i)
                    flag = flag + 1
                    print(flag)
                else:
                    i = i + 1
                    data = helper(i)
            if data[0] == "不符合规则的动态":
                print("不符合规则的动态")
            if data[0] == "error":
                print("出现了异常情况")
            if data[0] == "互动抽奖":
                # print(url)
                print(data[1])
                print("https://h.bilibili.com/"+str(i))
                modify(data[2])
                # tmp = doc2id(i)
                # print(tmp)
                repost(i)

        except:
            pass

monitor()
