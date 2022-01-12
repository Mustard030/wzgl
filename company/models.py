from django.db import models


# Create your models here.
# 供应商表
class Supplier(models.Model):
    name = models.CharField("供应商名称", max_length=64, unique=True, primary_key=True)
    corporation = models.CharField("法人", max_length=8, blank=True, null=True)
    code = models.CharField("机构代码", max_length=32, blank=True, null=True)
    address = models.CharField("地址", max_length=64, blank=True, null=True)
    bank = models.CharField("开户行", max_length=32, blank=True, null=True)
    account = models.CharField("银行账号", max_length=32, blank=True, null=True)
    postadd = models.CharField("通讯地址", max_length=64, blank=True, null=True)
    contacts = models.CharField("联系人", max_length=8, blank=True, null=True)
    phone = models.CharField("联系电话", max_length=8, blank=True, null=True)
    email = models.EmailField("电子邮箱", max_length=8, blank=True, null=True)
    remarks = models.CharField("备注", max_length=128, blank=True, null=True)



# 客户表
class Customer(models.Model):
    name = models.CharField("客户名称", max_length=64, unique=True, primary_key=True)
    corporation = models.CharField("法人", max_length=8, blank=True, null=True)
    code = models.CharField("机构代码", max_length=32, blank=True, null=True)
    address = models.CharField("地址", max_length=64, blank=True, null=True)
    bank = models.CharField("开户行", max_length=32, blank=True, null=True)
    account = models.CharField("银行账号", max_length=32, blank=True, null=True)
    postadd = models.CharField("通讯地址", max_length=64, blank=True, null=True)
    contacts = models.CharField("联系人", max_length=8, blank=True, null=True)
    phone = models.CharField("联系电话", max_length=8, blank=True, null=True)
    email = models.EmailField("电子邮箱", max_length=8, blank=True, null=True)
    remarks = models.CharField("备注", max_length=128, blank=True, null=True)
    external = models.BooleanField("外部客户", default=False)
