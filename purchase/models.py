from django.db import models

# Create your models here.
from django.db.models import DateField
from django.utils import timezone

from material_info.models import Material
from company.models import Supplier
from user.models import user


# 合同表
class Contract(models.Model):
    state_choice = (
        (0, u'执行中'),
        (1, u'完成'),
        (2, u'终止')
    )
    id = models.CharField("合同编号", max_length=32, primary_key=True, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, default="")
    name = models.CharField("合同名称", max_length=32, blank=True)
    date = models.DateField("签订日期", blank=True, null=True, default=timezone.now)
    place = models.CharField("签订地点", max_length=64, blank=True, null=True)
    money = models.DecimalField("合同价格", max_digits=12, decimal_places=2, blank=True, null=True)
    state = models.IntegerField("合同状态", default=0, choices=state_choice)
    terminator = models.ForeignKey(user, on_delete=models.PROTECT, blank=True, null=True)
    terminal_date = models.DateField("终止日期", blank=True, null=True)
    terminal_reason = models.CharField("终止原因", max_length=128, blank=True, null=True)
    # raw_id = models.OneToOneField('self', verbose_name='原材料ID', on_delete=models.SET_NULL, blank=True, null=True)
    remarks = models.CharField("备注", max_length=128, blank=True, null=True)


# 合同文件表
class Doc(models.Model):
    name = models.CharField("文件名", max_length=16)
    url = models.FileField("文件路径", upload_to='../static/contract/')
    date = models.DateField("上传时间")
    contract = models.ForeignKey(Contract, on_delete=models.PROTECT)


# 合同详情表
class ContractDetail(models.Model):
    # id = models.IntegerField("物资明细id", primary_key=True, unique=True,=True)
    contract_id = models.ForeignKey(Contract, on_delete=models.PROTECT, blank=True, null=True)
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    amount = models.DecimalField("采购总数", max_digits=12, decimal_places=2)
    remarks = models.CharField("备注", max_length=128, blank=True, null=True)


# 详细价格表
class Price(models.Model):
    id = models.AutoField("物资明细id", primary_key=True, unique=True)
    contract_detail = models.ForeignKey(ContractDetail, on_delete=models.PROTECT)
    date = models.DateField("价格生效时间", default=timezone.now)
    unit_price = models.DecimalField("单价", max_digits=12, decimal_places=2)
    amount = models.DecimalField("此价格对应数量", max_digits=12, decimal_places=2)
    change_date = models.DateField("变更日期", default="")
    change_reason = models.CharField("变更原因", max_length=128, blank=True, default="")
    change_person = models.ForeignKey(user, on_delete=models.PROTECT, blank=True, null=True)
    state = models.BooleanField("更改确认", default=False)


# 送货通知单表
class DeliveryNotice(models.Model):
    id = models.IntegerField("送货通知单号", primary_key=True, unique=True)
    contacts = models.CharField("联系人", max_length=8)
    phone = models.CharField("联系电话", max_length=8)
    address = models.CharField("收货地址", max_length=64, blank=True, null=True)
    filled = models.ForeignKey(user, on_delete=models.PROTECT, related_name="filled")
    handler = models.ForeignKey(user, on_delete=models.PROTECT, related_name="handler")
    reviewer = models.ForeignKey(user, on_delete=models.PROTECT, related_name="reviewer")
    date = models.DateField("填报日期")
    revocator = models.ForeignKey(user, on_delete=models.PROTECT, related_name="revocator")
    canceldate = models.DateField("撤销日期")
    cancelreason = models.CharField("撤销原因", max_length=128, blank=True, default="")
    remarks = models.CharField("备注", max_length=128, blank=True, default="")
    state = models.IntegerField("状态")
    # 状态包含：如已审批（待通知供应商）、已通知供应商（待供应商回执）、供应商已回执（待供应商送货）。其余状态则根据功能操作自动形成。


# 送货详情表
class DeliveryDetailed(models.Model):
    notice = models.ForeignKey(DeliveryNotice, on_delete=models.PROTECT)
    contract_detail = models.ForeignKey(ContractDetail, on_delete=models.PROTECT)
    amount = models.DecimalField("计划数量", max_digits=12, decimal_places=2)
    remarks = models.CharField("备注", max_length=128, blank=True, default="")
    indate = models.DateField("要求日期")
    pack = models.CharField("包装要求", max_length=8)


# 发票表
class Invoice(models.Model):
    contract_detail = models.ManyToManyField(ContractDetail, blank=True)
    count = models.DecimalField("开票包含数量", max_digits=12, decimal_places=2)
    number = models.CharField("发票号码", max_length=8)
    code = models.CharField("发票代码", max_length=8)
    date = models.DateField("开票日期")
    money = models.DecimalField("开票该材料数量", max_digits=12, decimal_places=2)
    state = models.IntegerField("状态")
    remarks = models.CharField("发票状态", max_length=128, blank=True, default="")
    url = models.CharField("发票路径", max_length=100)
