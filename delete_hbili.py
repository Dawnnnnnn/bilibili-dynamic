#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/9/8 17:33
# @Author  : Dawn
# @Contact : 1050596704@qq.com
import requests
import time
import traceback
import datetime
import hashlib

#######################
#       账户设置       #
#######################
cookie = ""
uid = 0
access_key = ""
csrf = ""


# 格式化打印模块
def printer(info, *args):
    at_now = int(time.time())
    time_arr = time.localtime(at_now)
    format_time = time.strftime("%Y-%m-%d %H:%M:%S", time_arr)
    # flag = "," if len(args) else " "
    content = f'[{format_time}] {info} {" ".join(f"{str(arg)}" for arg in args)}'
    print(content)


# 计算sign
def calc_sign(str):
    str = str + "560c52ccd288fed045859ed18bffd973"
    hash = hashlib.md5()
    hash.update(str.encode('utf-8'))
    sign = hash.hexdigest()
    return sign


# 获取当前时间戳
def CurrentTime():
    currenttime = int(time.mktime(datetime.datetime.now().timetuple()))
    return str(currenttime)


# 删除动态
def del_dynamic_id(dy_id):
    printer(f'删除{dy_id}动态!')
    headers = {
        "User-Agent": "Mozilla/5.0 BiliDroid/5.31.3 (bbcallen@gmail.com)",
        "Cookie": "l=v; sid=6gpbr48u",
        "Device-ID": "SX1NL0wuHCsaKRt4BHhIfRguTXxOfj5WN1BkBTdLfhstTn9NfUouFiUV",
        "Buvid": "32E49244-E168-4A0F-8361-EC61D73973DC20798infoc",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Display-ID": "48766812-1536402060"
    }
    temp_data = f"_device=android&_hwid=SX1NL0wuHCsaKRt4BHhIfRguTXxOfj5WN1BkBTdLfhstTn9NfUouFiUV&access_key={access_key}&appkey=1d8b6e7d45233436&build=5310300&dynamic_id={dy_id}&mobi_app=android&platform=android&src=meizu&trace_id=20180909020900047&ts={CurrentTime()*1000}&uid={uid}&version=5.31.3.5310300"
    data = f"{temp_data}&sign={calc_sign(temp_data)}"
    url = 'https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/rm_rp_dyn'
    response = requests.post(url, data=data, headers=headers)
    printer(response.json())


# 获取所有动态id
def get_dynamic_list():
    dy_id = 0
    dy_uid_list = []
    start = 1
    while 1:
        printer(f"当前进行到第{start}页")
        temp_params = f"_device=android&_hwid=SX1NL0wuHCsaKRt4BHhIfRguTXxOfj5WN1BkBTdLfhstTn9NfUouFiUV&access_key={access_key}&appkey=1d8b6e7d45233436&build=5310300&host_uid={uid}&mobi_app=android&offset_dynamic_id={dy_id}&page={start}&platform=android&qn=32&src=meizu&trace_id=20180908182200005&ts={CurrentTime()}&version=5.31.3.5310300&visitor_uid={uid}"
        url = f"https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?{temp_params}&sign={calc_sign(temp_params)}"
        headers = {
            "User-Agent": "Mozilla/5.0 BiliDroid/5.31.3 (bbcallen@gmail.com)",
            "Device-ID": "SX1NL0wuHCsaKRt4BHhIfRguTXxOfj5WN1BkBTdLfhstTn9NfUouFiUV",
            "Buvid": "32E49244-E168-4A0F-8361-EC61D73973DC20798infoc"
        }

        response = requests.get(url, headers=headers)
        exist = (response.json()['data']['has_more'])
        if exist == 0:
            break
        _len = len(response.json()['data']['cards'])
        for i in range(0, _len):
            dyid = response.json()['data']['cards'][i]['desc']['dynamic_id']
            tmp = (response.json()['data']['cards'][i]['card']).replace("true", "True").replace("false", "False")
            tmp = eval(tmp)
            if 'origin' in tmp.keys():
                tmp = eval(tmp['origin'])
                if 'id' in tmp['item'].keys():
                    printer(f"该条动态id:{dyid},对应的up主uid为{tmp['user']['uid']},对应的原始动态id为{tmp['item']['id']}")
                    dy_uid_list.append([dyid, tmp['user']['uid'], tmp['item']['id']])
                else:
                    printer(f"出现了一个旧版动态{response.json()}")
            else:
                printer(f"该条动态id:{dyid}已被原up主删除或者不是抽奖动态,将尝试删除")
                del_dynamic_id(dyid)
        dy_id = response.json()['data']['cards'][_len - 1]['desc']['dynamic_id']
        start = start + 1

        continue
    return dy_uid_list


# 取消关注
def unfollow(uid):
    printer(f'取消{uid}关注状态!')
    url = "https://api.live.bilibili.com/liveact/attention"
    headers = {
        "Referer": "https://link.bilibili.com/p/center/index",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
        "Origin": "https://link.bilibili.com",
        "Cookie": cookie,
    }
    data = {
        "type": 0,
        "uid": uid,
        "token": "",
        "csrf_token": csrf
    }
    response = requests.post(url, data=data, headers=headers)
    printer(response.json())


# 检查抽奖是否过期
def check_lottery_time(dy_id):
    url = f"https://api.vc.bilibili.com/lottery_svr/v1/lottery_svr/lottery_notice?business_type=2&business_id={dy_id}"
    headers = {
        "Referer": "https://t.bilibili.com/lottery/h5/index/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
        "Cookie": cookie,
        "Host": "api.vc.bilibili.com"
    }
    response = requests.get(url, headers=headers)
    if 'lottery_time' in (response.json()['data']).keys():
        unix_time = response.json()['data']['lottery_time']
        printer(unix_time)
        printer(time.time())
        if unix_time < time.time():
            return True
        else:
            return False
    else:
        return True


if __name__ == "__main__":
    all_list = get_dynamic_list()
    for i in range(0, len(all_list)):
        try:
            printer(all_list[i])
            statu = check_lottery_time(all_list[i][2])
            if statu:
                unfollow(all_list[i][1])
                del_dynamic_id(all_list[i][0])
        except:
            traceback.print_exc()
