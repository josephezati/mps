# Generated by Django 2.2.6 on 2020-01-28 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hm', '0015_auto_20200128_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='total_cost',
            field=models.IntegerField(default=10000000),
            preserve_default=False,
        ),
    ]