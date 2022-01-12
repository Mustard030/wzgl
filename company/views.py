import json

from django.http import JsonResponse
from django.shortcuts import render


# Create your views here.
from company.models import Supplier


def dispatcher(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理

    # GET请求 参数在url中，同过request 对象的 GET属性获取
    if request.method in ['GET', 'DELETE']:
        request.params = request.GET

    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
    elif request.method in ['POST', 'PUT']:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        request.params = json.loads(request.body)

    # 根据不同的action分派给不同的函数进行处理

    action = request.params['action']
    if action == 'list_supplier':
        return list_supplier(request)


def list_supplier(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = Supplier.objects.values('name')
    # 将 QuerySet 对象 转化为 list 类型
    # 否则不能 被 转化为 JSON 字符串
    retlist = list(qs)
    return JsonResponse({'ret': 0, 'retlist': retlist})
