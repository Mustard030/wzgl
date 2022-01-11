import requests as requests
from django.test import TestCase
import requests
import pprint
# Create your tests here.
# payload = {
#     'action': 'list_contract_filter',
#     'pagenum': 1,
#     'pagesize': 6,
#     'supplier': "",
#     'code': "",
#     'name': "",
#     'dateRange[]':["2022-1-1","2022-1-10"],
#     'executing':1
#
#     # ‘date’:("2022-1-1","2022-1-10")
#
# }
# response = requests.get('http://127.0.0.1/purchase/contract', params=payload)
# # # # 发送请求给web服务
# response = requests.get('http://127.0.0.1/purchase/contract?action=list_material_name')
# pprint.pprint(response.json())

payload = {
    "action": "add_contract",
    "data":{
        "contract_id": "2022-1-5",
        "supplier": "西南石油大学",
        "name":"123",
        "date":"2022-1-1",
        "place":"xindu",
        "money":50,
        "state":1,
        "remarks":"dsafaf"
        }
    }


# # # 发送请求给web服务
response = requests.post('http://127.0.0.1:80/purchase/contract/', json=payload)
# # #
# #
pprint.pprint(response.json())