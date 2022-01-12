import traceback
from django.db.models import F
import numpy as np
from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse, JsonResponse
from .models import Material, Unit
import json
import pandas as pd
from purchase.models import ContractDetail


# Create your views here.

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
    if action == 'list_unit':
        return list_unit(request)
    if action == 'list_pro':
        return list_pro(request)
    if action == 'list_product':
        return list_product(request)
    if action == 'list_material':
        return list_material(request)
    elif action == 'add_material':
        return add_material(request)
    elif action == 'list_material_filter':
        return list_material_filter(request)
    elif action == 'edit_material':
        return edit_material(request)
    elif action == 'del_material':
        return del_material(request)
    elif action == 'list_material_name':
        return list_material_name(request)
    elif action == 'list_material_code':
        return list_material_code(request)
    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})


# 查询单位
def list_unit(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = Unit.objects.values()

    # 将 QuerySet 对象 转化为 list 类型
    # 否则不能 被 转化为 JSON 字符串
    retlist = list(qs)

    return JsonResponse({'ret': 0, 'retlist': retlist})


# 查询成品中没有被关联原材料的成品
def list_pro(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    # qs=Material.objects.filter(pro__isnull=False).values_list('pro')
    qs = Material.objects.filter(is_product=True).exclude(
        id__in=Material.objects.filter(pro__isnull=False).values_list('pro')).values('id', 'name', 'code')
    # 将 QuerySet 对象 转化为 list 类型
    #  Material.objects.filter(pro__isnull=False).values_list('pro')找出成品中已经关联了材料的成品
    # 否则不能 被 转化为 JSON 字符串
    retlist = list(qs)
    return JsonResponse({'ret': 0, 'retlist': retlist})


# 查询所有的成品
def list_product(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    # qs=Material.objects.filter(pro__isnull=False).values_list('pro')
    qs = Material.objects.filter(is_product=True).values('id', 'name')
    # 将 QuerySet 对象 转化为 list 类型
    # 否则不能 被 转化为 JSON 字符串
    retlist = list(qs)
    return JsonResponse({'ret': 0, 'retlist': retlist})


# 查询原材料名称
def list_material_name(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = Material.objects.filter(is_product=False).values('name')
    # 将 QuerySet 对象 转化为 list 类型
    # 否则不能 被 转化为 JSON 字符串
    retlist = list(qs)
    return JsonResponse({'ret': 0, 'retlist': retlist})


# 查询根据原材料名称获的代号、规格型号、执行标准、单位等信息
def list_material_code(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    query = request.params.get('name', None)
    qs = Material.objects.annotate(unit_name=F('unit__name')).filter(is_product=False, name=query).values('code',
                                                                                                          'standards',
                                                                                                          'exe_standard',
                                                                                                          'unit__name')
    # 将 QuerySet 对象 转化为 list 类型
    # 否则不能 被 转化为 JSON 字符串
    retlist = list(qs)
    return JsonResponse({'ret': 0, 'retlist': retlist})


# 过滤查询
def list_material_filter(request):
    try:
        # .order_by('-id') 表示按照 id字段的值 倒序排列
        # 这样可以保证最新的记录显示在最前面
        filter_dict = {'is_product': False}
        if request.params.get('isProduct', None) == 'true':
            filter_dict['pro__isnull'] = False
        qs = Material.objects.filter(**filter_dict).values('id', 'name', 'code', 'standards', 'exe_standard',
                                                           'remarks', 'unit__id', 'pro__id', 'unit__name',
                                                           'pro__name').order_by('-id')

        # 查看是否有 关键字 搜索 参数
        conditions = dict()
        name = request.params.get('name', None)
        code = request.params.get('code', None)
        if name:
            conditions['name__icontains'] = name.strip()
        if code:
            conditions['code__icontains'] = code.strip()
        qs = qs.filter(**conditions)
        # 要获取的第几页
        pagenum = request.params['pagenum']

        # 每页要显示多少条记录
        pagesize = request.params['pagesize']

        # 使用分页对象，设定每页多少条记录
        pgnt = Paginator(qs, pagesize)

        # 从数据库中读取数据，指定读取其中第几页
        page = pgnt.page(pagenum)

        # 将 QuerySet 对象 转化为 list 类型
        retlist = list(page)

        # 把原来的list转化成dataframe对象
        df = pd.DataFrame(retlist).fillna("")
        # 讲不符合命名规则的列名重命名（以字典格式），inplace代表在原dataframe对象上修改
        df.rename(columns={'unit__id': 'unitID',
                           'pro__id': 'proID',
                           'unit__name': 'unitName',
                           'pro__name': 'proName'}, inplace=True)
        # 将dataframe转换为字典格式数据
        retlist = df.to_dict("records")
        # total指定了 一共有多少数据
        return JsonResponse({'ret': 0, 'retlist': retlist, 'total': pgnt.count})

    except EmptyPage:
        return JsonResponse({'ret': 1, 'retlist': [], 'total': 0})

    except Exception as e:
        return JsonResponse({'ret': 2, 'msg': f'未知错误\n{e}'})
        # return JsonResponse({'ret': 2, 'msg': f'未知错误\n{traceback.format_exc()}'})


# def list_material(request):
#     # 返回一个 QuerySet 对象 ，包含所有的表记录
#     qs = Material.objects.filter(is_product=False).values('id', 'name', 'code', 'standards', 'exe_standard',
#                           'remarks', 'unit__name', 'pro__name')
#
#     # 将 QuerySet 对象 转化为 list 类型
#     # 否则不能 被 转化为 JSON 字符串
#     retlist = list(qs)
#
#     return JsonResponse({'ret': 0, 'retlist': retlist})

# 这个方法不需要了
def list_material(request):
    try:
        # 返回一个 QuerySet 对象 ，包含所有的表记录
        qs = Material.objects.filter(is_product=False).values('id', 'name', 'code', 'standards', 'exe_standard',
                                                              'remarks', 'unit__name', 'pro__name')

        # 要获取的第几页
        pagenum = request.params['pagenum']

        # 每页要显示多少条记录
        pagesize = request.params['pagesize']

        # 使用分页对象，设定每页多少条记录
        pgnt = Paginator(qs, pagesize)

        # 从数据库中读取数据，指定读取其中第几页
        page = pgnt.page(pagenum)

        # 将 QuerySet 对象 转化为 list 类型
        retlist = list(page)

        # total指定了 一共有多少数据
        return JsonResponse({'ret': 0, 'retlist': retlist, 'total': pgnt.count})

    except EmptyPage:
        return JsonResponse({'ret': 0, 'retlist': [], 'total': 0})

    except:
        return JsonResponse({'ret': 2, 'msg': f'未知错误\n{traceback.format_exc()}'})


def add_material(request):
    # 从请求消息中 获取要添加材料的信息
    # 并且插入到数据库中
    # 返回值 就是对应插入记录的对象
    info = request.params['data']
    conditions = dict()
    # 判断前端传来的name\code，如果不为空则去掉字符前后的空格，并保存在查询字典里面
    if info['name']:
        conditions['name'] = info['name'].strip()
    if info['code']:
        conditions['code'] = info['code'].strip()
    # 查找用户添加的名称和代号在数据表中存在的话则提示不能添加（精确查找）
    if Material.objects.filter(**conditions).exists():
        return JsonResponse({'ret': 1, 'msg': '原材料重复，不能添加'})
    # 判断前端数据是否带有成品，有的话将其对象化为pro
    if info["pro"]:
        pro = Material.objects.get(id=info["pro"])
    else:
        pro = None
    # 判断单位是否存在与数据库中，有的话将其对象化为unit
    try:
        unit = Unit.objects.get(id=info["unit"])
    except Unit.DoesNotExist:
        unit = None
    # 将添加的原材料的参数保存在字典conditions,判断前端数据用get(参数,None)，为空时则为None,不为空时删除空格。
    conditions = dict()
    name = info.get('name', None)
    if name:
        conditions['name'] = name.strip()
    code = info.get('code', None)
    if code:
        conditions['code'] = code.strip()
    standards = info.get('standards', None)
    if standards:
        conditions['standards'] = standards.strip()
    exe_standard = info.get('exe_standard', None)
    if exe_standard:
        conditions['exe_standard'] = exe_standard.strip()
    remarks = info.get('remarks', None)
    if remarks:
        conditions['remarks'] = remarks.strip()
    conditions['unit'] = unit
    conditions['pro'] = pro
    record=Material.objects.create(**conditions)
    # record = Material.objects.create(name=info.get('name', None).strip(),
    #                                  code=info.get('code', None).strip(),
    #                                  standards=info.get('standards', None).strip(),
    #                                  exe_standard=info.get('exe_standard', None).strip(),
    #                                  unit=unit,
    #                                  is_product=info['is_product'],
    #                                  remarks=info.get('remarks', None).strip(),
    #                                  pro=pro
    #                                  )

    return JsonResponse({'ret': 0, 'id': record.id})


def edit_material(request):
    # 从请求消息中 获取修改材料的信息
    # 找到该材料，并且进行修改操作

    materid = request.params['id']
    newdata = request.params['newdata']

    try:
        # 根据 id 从数据库中找到相应的客户记录
        material = Material.objects.get(id=materid)
    except Material.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'id 为`{materid}`的材料信息不存在或已经关联合同，不能修改'
        }

    if 'remarks' in newdata:
        material.remarks = newdata['remarks']
    if 'unit' in newdata:
        try:
            unit = Unit.objects.get(id=newdata["unit"])
        except Unit.DoesNotExist:
            unit = None
        material.unit = unit
    if 'code' in newdata:
        material.code = newdata['code']
    if 'standards' in newdata:
        material.standards = newdata['standards']
    if 'exe_standard' in newdata:
        material.exe_standard = newdata['exe_standard']
    if 'pro' in newdata:
        if newdata['pro'] != "":
            try:
                pro = Material.objects.get(id=newdata["pro"])
            except Material.DoesNotExist:
                pro = None
            material.pro = pro
        else:
            material.pro = None

    # 注意，一定要执行save才能将修改信息保存到数据库
    material.save()
    #
    return JsonResponse({'ret': 0,
                         'msg': '修改成功'})


def del_material(request):
    materid = request.params['id']

    try:
        # 根据 id 从数据库中找到相应的原材料记录
        material = Material.objects.get(id=materid)
    except Material.DoesNotExist:
        return JsonResponse({
            'ret': 1,
            'msg': f'id 为`{materid}`的客户不存在'
        })
    # 判断该原材料是否关联了成品
    if material.pro_id:
        return JsonResponse({
            'ret': 1,
            'msg': '该原材料已经关联成品，不能删除'})
    # 判断该原材料是否关联了合同
    elif ContractDetail.objects.filter(material=material).exists():
        return JsonResponse({
            'ret': 1,
            'msg': '该原材料已经关联合同或者发货信息，不能删除'})
    else:
        material.delete()
        # delete 方法就将该记录从数据库中删除了
        return JsonResponse({'ret': 0})
