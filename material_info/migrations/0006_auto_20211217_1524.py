# Generated by Django 3.2.9 on 2021-12-17 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('material_info', '0005_alter_material_raw_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='material',
            name='raw_id',
        ),
        migrations.AddField(
            model_name='material',
            name='pro',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='material_info.material', verbose_name='成品ID'),
        ),
    ]