from django.contrib import admin

# Register your models here.
from .models import Unit, Material


class MaterialManager(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'code', 'standards', 'exe_standard', 'remarks',  'unit', 'guid_price','is_product', 'pro' ]

admin.site.register(Material, MaterialManager)

class UnitManager(admin.ModelAdmin):
    list_display = ['id', 'name']

admin.site.register(Unit, UnitManager)

