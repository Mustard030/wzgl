# Generated by Django 3.1.2 on 2021-12-19 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material_info', '0010_auto_20211218_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='code',
            field=models.CharField(blank=True, default='', max_length=32, null=True, verbose_name='代号'),
        ),
        migrations.AlterField(
            model_name='material',
            name='exe_standard',
            field=models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='执行标准'),
        ),
        migrations.AlterField(
            model_name='material',
            name='remarks',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='material',
            name='standards',
            field=models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='规格'),
        ),
    ]
