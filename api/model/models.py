"""
models.py
- for defining classes that will serve as data objects for the server

Created by Xiong Kaijie on 2022-08-01.
Contributed by: Xiong Kaijie
Copyright © 2022 team Root of ByteDance Youth Camp. All rights reserved.
"""

from flask_mongoengine import MongoEngine
from mongoengine import *
from datetime import datetime



class User(DynamicDocument):
    """用户数据结构

    用户 ID: _id
    设备 (device)
    操作系统 (os)
    浏览器 (browser)
    网络制式 (network)
    IP (ip)
    地区 (location)

    """

    device = StringField()
    os = StringField()
    browser = StringField()
    ip = StringField()
    tag = StringField()
    page = StringField()

    meta = {
        'collection': 'user',
        'ordering': ['-id']
    }


class PageLoad(DynamicDocument):
    user = ReferenceField(User)
    pageUrl = StringField(required=True)
    timestamp = DateTimeField(required=True)
    FP = FloatField(required=True)
    FCP = FloatField(required=True)
    DOMReady = FloatField(required=True)
    stayDuration = FloatField(required=True)

    meta = {
        'collection': 'pageLoad',
        'ordering': ['-id']
    }


class RequestData(DynamicDocument):
    """请求数据结构

    请求 ID (requestID): _id
    用户 ID (userID {用户}['_id'])
    请求目标 URL 地址 (targetURL)
    状态码 (statusCode)
    时间戳 (timestamp 请求触发时间)
    事件类型 (eventType load/error/abort)
    HTTP持续时间 (httpDuration)
    DNS持续时间 (dnsDuration)
    请求参数 (params URL Body/URL Parameters)
    响应内容 (responseData return value)
    """

    user = ReferenceField(User)
    targetURL = StringField(required=True)
    statusCode = StringField(required=True)
    timestamp = DateTimeField(required=True)
    eventType = StringField()
    httpDuration = FloatField()
    dnsDuration = FloatField()
    params = StringField()
    responseData = StringField()
    is_error = BooleanField(required=True, default=False)

    meta = {
        'collection': 'requestData',
        'ordering': ['-timestamp']
    }


class ErrorData(DynamicDocument):
    """Error data structure
    Requirements:「异常监控, 包括: JS异常、接口异常、白屏异常、资源异常等」

    [基本信息]
        错误 ID: _id
        错误分类 (category JS/Promise/Request/Resource/BlankScreen)
        错误来源 URL 地址 (originURL)
        时间戳 (timestamp 错误的产生时间)

        用户
        请求

        {用户}
            用户 ID (触发该错误的当前用户): _id
            设备 (device)
            操作系统 (os)
            浏览器 (browser)
            网络制式 (network)
            IP (ip)
            地区 (location)

        #JS异常 JS执行异常
        if categroy == 'JS'
            错误类型 (errorType): 'jsError'
            报错信息 (errorMsg): event.message
            报错文件名 (filename 报错链接): event.filename
            行列号 (position): (event.lineNo || 0) + ":" + (event.columnNo || 0)
            堆栈信息 (stack 包含源文件, 报错位置等): event.error.stack
            选择器信息 (selector CSS选择器): getLastEvent()? getSelector(getLastEvent().path || getLastEvent().target): ""

        #JS异常 Promise异常
        if categroy == 'Promise'
            错误类型 (errorType): 'promiseError'
            报错信息 (errorMsg): event.reason || event.reason.message
            报错文件名 (filename): event.reason.stack.match(/at\s+(.+):(\d+):(\d+)/)[1]
            行列号 (position): event.reason.stack.match(/at\s+(.+):(\d+):(\d+)/)[2] + ':' + event.reason.stack.match(/at\s+(.+):(\d+):(\d+)/)[3]
            堆栈信息 (stack 包含源文件, 报错位置等): getLines(event.reason.stack)
            选择器信息 (selector CSS选择器): getLastEvent()? getSelector(getLastEvent().path || getLastEvent().target): ""

        #资源异常
        if categroy == 'Resource'
            错误类型 (errorType): 'resourceError'
            报错文件名 (filename 加载失败的文件位置): event.target.src || event.target.href
            标签名 (tagName): event.target.tagName
            时间 (rsrcTimestamp): formatTime(event.timeStamp)
            选择器信息 (selector CSS选择器): getSelector(event.path || event.target)

        #接口异常
        if categroy == 'Request'
            错误类型 (errorType): 'requestError'
            {请求} > 如果Request监控出现异常, 则向error表里面添加此request
                请求 ID (requestID): _id
                用户 ID (userID {用户}['_id'])
                请求目标 URL 地址 (targetURL)
                状态码 (statusCode)
                时间戳 (timestamp 请求触发时间)
                事件类型 (eventType load/error/abort)
                HTTP持续时间 (httpDuration)
                DNS持续时间 (dnsDuration)
                请求参数 (params URL Body/URL Parameters)
                响应内容 (response return value)

        #白屏异常
        if categroy == 'BlankScreen'
            错误类型 (errorType): 'blankscreenError'
            空白点 (emptyPoints)
            分辨率 (screen)
            视口 (viewPoint)
            选择器 (selector)

    [用户行为回溯信息]
        行为名称
        行为对应项目
        行为时间戳

    [数据统计概况]
        发生总次数
        影响用户数
        发生数时间维度统计

    deviceName = StringField()
    deviceOS = StringField()
    deviceBrowser = StringField()
    ip = StringField(required=True, max_length=128)
    """

    category = StringField(required=True)
    originURL = StringField(required=True)
    timestamp = DateTimeField(required=True, default=datetime.utcnow)
    user = ReferenceField(User)
    requestData = ReferenceField(RequestData)
    errorType = StringField()
    errorMsg = StringField()
    filename = StringField()
    position = StringField()
    stack = StringField()
    selector = StringField()
    tagName = StringField()
    rsrcTimestamp = StringField()
    emptyPoints = StringField()
    screen = StringField()
    viewPoint = StringField()

    meta = {
        'collection': 'errorData',
        'ordering': ['-timestamp'],
        'allow_inheritance': True,
    }
