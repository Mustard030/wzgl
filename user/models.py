from django.db import models

# Create your models here.
# 临时用户表
class user(models.Model):
    id = models.CharField("用户id", primary_key=True, max_length=16)
    name = models.CharField("用户姓名", max_length=8, unique=True)