# Generated by Django 3.1.4 on 2021-06-09 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pms_index', '0004_visibilityattribute'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='visibility',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.PROTECT, to='pms_index.visibilityattribute'),
        ),
    ]
