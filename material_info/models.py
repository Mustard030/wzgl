from django.db import models


# Create your models here.


class Unit(models.Model):
    name = models.CharField("计量单位", max_length=8, unique=True)


class Material(models.Model):
    name = models.CharField("名称", max_length=64, default="")
    code = models.CharField("代号", max_length=32, blank=True, null=True)
    standards = models.CharField("规格", max_length=64, blank=True, null=True)
    exe_standard = models.CharField("执行标准", max_length=64, blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, blank=True, null=True)
    guid_price = models.DecimalField("指导价", max_digits=12, decimal_places=2, blank=True, null=True)
    is_product = models.BooleanField("是否成品", default=False)
    pro = models.OneToOneField('self', verbose_name='成品ID', on_delete=models.SET_NULL, blank=True, null=True,)
    remarks = models.CharField("备注", max_length=255, blank=True, null=True)