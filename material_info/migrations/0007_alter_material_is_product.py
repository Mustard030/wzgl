# Generated by Django 3.2.9 on 2021-12-17 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material_info', '0006_auto_20211217_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='is_product',
            field=models.BooleanField(default=False, verbose_name='是否关联成品'),
        ),
    ]
