# Generated by Django 3.1.4 on 2021-07-14 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pms_index', '0012_auto_20210713_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listcard',
            name='status',
            field=models.CharField(default='1', max_length=10),
        ),
        migrations.AlterField(
            model_name='workspacelist',
            name='status',
            field=models.CharField(default='1', max_length=10),
        ),
    ]