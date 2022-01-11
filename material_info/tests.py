from django.test import TestCase

# Create your tests here.
#from .models import Unit
import requests
import pprint

# 构建添加材料信息的消息体，是json格式
payload = {
    "action": "add_material",
    "data":{
        "name": "测试关联成品",
        "code": 6,
        "standards": "这是一种标准",
        "exe_standard": "执行标准",
        "is_product": False,
        "unit": 4,
        "pro":9,
        "remarks": "备注在这里写"
    }
}
# #

   # 构建修改材料信息的消息体，是json格式
# payload = {
#      "action": "modify_material",
#      "id": 14,
#      "newdata":{
#          "remarks": "修改信息2",
#          "code": "43",
#          "standards": "这是修改标准2",
#          "exe_standard": "修改执行标准2",
#          "unit": 2,
#           "pro":8,
#
#      }
#  }

  ##构建删除材料信息的消息体，是json格式
# payload = {
#     "action": "del_material",
#     "id": 5,
# }
#
# # # # 发送请求给web服务
response = requests.post('http://127.0.0.1:80/material/mater_mg/', json=payload)
# # #
# #
pprint.pprint(response.json())
#
# # 构建查看产品信息的消息体
# response = requests.get('http://127.0.0.1/material/mater_mg?action=list_material_filter')
# #
# # 查看unit数据
# response = requests.get('http://127.0.0.1/material/mater_mg?action=list_material_name')
# # # # # 发送请求给web服务
# pprint.pprint(response.json())

#过滤测试
# 再发送列出请求，注意多了 keywords
# payload = {
#     'action': 'list_material_filter',
#     'pagenum': 1,
#     'pagesize': 6,
#     'keywords': '5'
# }
#
# response = requests.get('http://localhost/material/mater_mg/',
#               params=payload)
#
# pprint.pprint(response.json())


#分页测试


# 再发送列出请求，注意多了 pagenum 和 pagesize
# payload = {
#     'action': 'list_material_filter',
#     'pagenum': 1,
#     'pagesize' : 16
# }
#
# response = requests.get('http://localhost/material/mater_mg/',
#               params=payload)
#
# pprint.pprint(response.json())


# payload = {
#     'action': 'list_material_code',
#     'name': '机器'
# }
# response = requests.get('http://127.0.0.1/material/mater_mg', params=payload)
# # # # # 发送请求给web服务
# # response = requests.get('http://127.0.0.1/purchase/contract?action=list_material_name')
# pprint.pprint(response.json())