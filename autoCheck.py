#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/20 10:42
# @Author  : Derek.S
# @Site    : 
# @File    : autoCheck.py

import requests
import res
import time
import argparse

USAGE = "autoCheck.py -u [Username] -p [Password]"

parser = argparse.ArgumentParser(prog="autocheck.py", usage=USAGE)
parser.add_argument("-u", "-username", nargs="+", type=str, required=True, dest="username", help="username")
parser.add_argument("-p", "-password", nargs="+", type=str, required=True, dest="password", help="password")
args = parser.parse_args()

s = requests.session()

headers = {
    "Accept": "*",
    "Accept-APIVersion": "1.0",
    "appVersionNo": "73",
    "mobileBrand": "Honor",
    "mobileStandard": "WIFI",
    "platformType": "android",
    "platformVersion": "6.0",
    "User-Agent": "okhttp/3.4.1",
    "Accept-Encoding": "gzip",
    "Content-Type": "application/x-www-form-urlencoded"
}


def login(username, password):
    login_url = "http://webapp.cocc.cdmetro.cn:10080/api/login"

    pnId = res.randompnId()
    callTime = res.localtime()
    userId = str(username)
    userPwd = res.pwdMD5(str(password))

    sign_data = {
        "callTime": callTime,
        "pnId": pnId,
        "userId": userId,
        "userPwd": userPwd,
        "tokenId": ""
    }

    sign_str = res.getSign(**sign_data)

    formdata = {
        "pnId": pnId,
        "userPwd": userPwd
    }

    headers['callTime'] = callTime
    headers['sign'] = sign_str
    headers['tokenId'] = ""
    headers['userId'] = userId

    try:
        loginPost = s.post(login_url, data=formdata, headers=headers)
        if loginPost.status_code == 200:
            if loginPost.text:
                loginReturnData = loginPost.json()
                code = loginReturnData['code']
                if(code == 0):
                    print("登录成功")
                    tokenId = loginReturnData['returnData'][0]
                    queryTotalPoints(tokenId, userId)
                    autoCheckin(tokenId, userId)
                else:
                    print("登录异常\n" + loginReturnData['message'])
            else:
                print("Post返回异常")
        else:
            print("请求失败")
    except Exception as e:
        print("登录失败\n" + e)


def autoCheckin(tokenid, userid):
    query_url = "http://webapp.cocc.cdmetro.cn:10080/api/checkin"

    callTime = res.localtime()
    userId = userid

    sign_data = {
        "callTime": callTime,
        "userId": userId,
        "tokenId": tokenid
    }

    sign_str = res.getSign(**sign_data)

    headers['callTime'] = callTime
    headers['sign'] = sign_str
    headers['tokenId'] = tokenid
    headers['userId'] = userId

    try:
        checkinPost = s.post(query_url, headers=headers)
        if checkinPost.status_code == 200:
            if not checkinPost.content:
                queryCheckinStatus(tokenid, userId)
            else:
                checkinJson = checkinPost.json()
                code = checkinJson['code']
                mes = checkinJson['message']
                if code == 0:
                    print(mes)
                    getSurplusTimes(tokenid, userid)
                else:
                    print(mes)
    except Exception as e:
        print("签到失败\n".join(e))


def queryCheckinStatus(tokenid, userid):
    query_url = "http://webapp.cocc.cdmetro.cn:10080/api/QuerySignInRecord"

    callTime = res.localtime()
    userId = userid

    sign_data = {
        "callTime": callTime,
        "userId": userId,
        "tokenId": tokenid
    }

    sign_str = res.getSign(**sign_data)

    headers['callTime'] = callTime
    headers['sign'] = sign_str
    headers['tokenId'] = tokenid
    headers['userId'] = userId

    try:
        querySignInRecordPost = s.post(query_url, headers=headers)
        if querySignInRecordPost.status_code == 200:
            if querySignInRecordPost.text:
                signInRecordJson = querySignInRecordPost.json()
                signInRecodeData = signInRecordJson['returnData']
                signInDate = signInRecodeData[0]['checkin_date']
                todayDate = str(time.strftime("%Y-%m-%d", time.localtime()))
                if str(signInDate).split(" ")[0] == todayDate:
                    print("已签到")
                    getSurplusTimes(tokenid, userid)
            else:
                print("查询签到详情失败")
        else:
            print("请求失败")
    except Exception as e:
        print(e)


def autoGoLottery(tokenid, userid):
    query_url = "http://webapp.cocc.cdmetro.cn:10080/api/prizes/lottery"

    callTime = res.localtime()
    userId = userid

    sign_data = {
        "callTime": callTime,
        "userId": userId,
        "tokenId": tokenid
    }

    sign_str = res.getSign(**sign_data)

    headers['callTime'] = callTime
    headers['sign'] = sign_str
    headers['tokenId'] = tokenid
    headers['userId'] = userId

    try:
        goLotteryPost = s.post(query_url, headers=headers)
        if goLotteryPost.status_code == 200:
            if goLotteryPost.text:
                lotteryResultJson = goLotteryPost.json()
                lotteryResultCode = lotteryResultJson['code']
                if lotteryResultCode == 0:
                    print(lotteryResultJson['message'])
                    for i in lotteryResultJson['returnData']:
                        print(i["prize"]["name"])
                else:
                    print(lotteryResultJson['message'])
    except Exception as e:
        print(e)


def getSurplusTimes(tokenid, userid):
    query_url = "http://webapp.cocc.cdmetro.cn:10080/api/prizes/getSurplusTimes"

    callTime = res.localtime()
    userId = userid

    sign_data = {
        "callTime": callTime,
        "userId": userId,
        "tokenId": tokenid
    }

    sign_str = res.getSign(**sign_data)

    headers['callTime'] = callTime
    headers['sign'] = sign_str
    headers['tokenId'] = tokenid
    headers['userId'] = userId

    try:
        getSurplusTimePost = s.post(query_url, headers=headers)
        if getSurplusTimePost.status_code == 200:
            if getSurplusTimePost.text:
                surplusTimeJson = getSurplusTimePost.json()
                surplusTimeData = surplusTimeJson['returnData'][0]
                if surplusTimeData != 0:
                    print("抽奖次数：" + str(surplusTimeData) + " 开始抽奖")
                    for i in range(surplusTimeData):
                        autoGoLottery(tokenid, userId)
                else:
                    print("已无抽奖次数")
                    queryTotalPoints(tokenid, userId)
            else:
                print("查询抽奖次数失败")
        else:
            print("请求失败")
    except Exception as e:
        print(e)


def queryTotalPoints(tokenid, userid):
    query_url = "http://webapp.cocc.cdmetro.cn:10080/api/QuerytotalPoints"

    callTime = res.localtime()
    userId = userid

    sign_data = {
        "callTime": callTime,
        "userId": userId,
        "tokenId": tokenid
    }

    sign_str = res.getSign(**sign_data)

    headers['callTime'] = callTime
    headers['sign'] = sign_str
    headers['tokenId'] = tokenid
    headers['userId'] = userId

    try:
        queryTotalPointsPost = s.post(query_url, headers=headers)
        if queryTotalPointsPost.status_code == 200:
            if queryTotalPointsPost.text:
                totalPointsJson = queryTotalPointsPost.json()
                totalPoints = totalPointsJson['returnData'][0]['totalPoints']
                print("当前积分：" + str(totalPoints))
            else:
                print("获取积分失败")
        else:
            print("请求失败")
    except Exception as e:
        print("发生异常")


if __name__ == "__main__":
    print(time.strftime("%Y-%m-%d".format(time.localtime())))
    login(args.username[0], args.password[0])
