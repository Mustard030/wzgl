import datetime
import json
import traceback
import pandas as pd
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from company.models import supplier as supply
from material_info.models import Material
from .models import Contract, ContractDetail, Price


# Create your views here

def dispatcher(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理d

    # GET请求 参数在url中，同过request 对象的 GET属性获取
    if request.method in ['GET', 'DELETE']:
        request.params = request.GET

    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
    elif request.method in ['POST', 'PUT']:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        request.params = json.loads(request.body)

    # 根据不同的action分派给不同的函数进行处理

    action = request.params['action']
    if action == 'contractID_check':
        return contractID_check(request)
    # if action == 'list_product':
    #     return list_product(request)
    # if action == 'list_material':
    #     return list_material(request)
    if action == 'list_contract_filter':
        return list_contract_filter(request)
    elif action == 'add_contract':
        return add_contract(request)
    # elif action == 'modify_material':
    #     return modify_material(request)
    # elif action == 'del_material':
    #     return del_material(request)

    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})


# 过滤查询合同
def list_contract_filter(request):
    try:
        # .order_by('-date') 表示按照 合同时间 倒序排列
        # 这样可以保证最新的记录显示在最前面
        qs = Contract.objects.values('id', 'name', 'date', 'place', 'money',
                                     'remarks', 'supplier__name').order_by('-date')
        # 查看是否有 关键字 搜索 参数
        # 获取页面查询时间范围
        conditions = dict()
        # 获取页面其他参数
        supplier = request.params.get('supplier', None)
        code = request.params.get('code', None)
        name = request.params.get('name', None)
        executing = request.params.get('executing', None)
        if executing == 'true':
            conditions['state'] = 0

        conditions['supplier__name__icontains'] = supplier
        conditions['id__icontains'] = code.strip()
        conditions['name__icontains'] = name.strip()

        if "dateRange[]" in request.params:
            start, end = request.params.getlist('dateRange[]')
            start = datetime.datetime.strptime(start, '%Y-%m-%d')
            end = datetime.datetime.strptime(end, '%Y-%m-%d')
            conditions['date__range'] = (start, end)

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
        df.rename(columns={'supplier__name': 'supplier'}, inplace=True)
        # 将dataframe转换为字典格式数据
        retlist = df.to_dict("records")
        # total指定了 一共有多少数据
        return JsonResponse({'ret': 0, 'retlist': retlist, 'total': pgnt.count})

    except EmptyPage:
        return JsonResponse({'ret': 1, 'retlist': [], 'total': 0})

    except Exception as e:
        return JsonResponse({'ret': 2, 'msg': f'未知错误\n{traceback.format_exc()}'})


def contractID_check(request):
    # 注意将传入字符串前后的空格去掉
    contract_id = request.params.get('contract_id', None).strip()
    if contract_id:
        if Contract.objects.filter(id=contract_id).exists():
            return JsonResponse({'ret': 0, 'msg': '此合同单号已经存在'})
        else:
            return JsonResponse({'ret': 1})
    else:
        return JsonResponse({'msg': '合同单号不能为空'})


def add_contract(request):
    # 从请求消息中 获取要添加合同的信息
    # 并且插入到数据库中，插入到合同表、合同详情表、价格表
    # 返回值 就是对应插入记录的对象
    # 将获得数据放入info,合同物资列表放如detail
    info = request.params['data']
    detail = info['rawdetail']
    # supplier是将获取的供应商转换为supply对象
    try:
        supplier = supply.objects.get(name=info["supplier"])
    except supplier.DoesNotExist:
        supplier = None
    # 将合同基本信息写入到合同表
    record1 = Contract.objects.create(id=info['contract_id'],
                                      supplier=supplier,
                                      name=info['name'].strip(),
                                      date=info['date'],
                                      place=info['place'].strip(),
                                      money=info['money'],
                                      state=info['state'],
                                      remarks=info['remarks'].strip()
                                      )
    # 遍历前端传过来的合同详情数据项，添加到合同详细表、价格表
    if record1:
        if detail:
            for raw in detail:
                # 获取物资id
                try:
                    material = Material.objects.get(id=int(raw['id']))
                except Material.DoesNotExist:
                    material = None
                # 插入数据到合同详细表record2,合同价格表record3
                record2 = ContractDetail.objects.create(contract_id=record1,
                                                        material=material,
                                                        amount=raw['amount'],
                                                        remarks=raw['remarks'].strip()
                                                        )
                record3 = Price.objects.create(contract_detail=record2,
                                               unit_price=raw['unit_price'],
                                               amount=raw['amount'],
                                               change_date=info['date'])
            return JsonResponse({'ret': 0,
                                 'contract': record1.id,
                                 'contract_detail': record2.id,
                                 'price': record3.id
                                 })
        else:
            return JsonResponse({'ret': 0,
                                 'contract': record1.id})

    else:
        return JsonResponse({'ret': 1,
                             'msg': '合同不存在'})
