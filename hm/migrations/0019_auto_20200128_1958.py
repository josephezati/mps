# Generated by Django 2.2.6 on 2020-01-28 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hm', '0018_auto_20200128_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='reg_no',
            field=models.CharField(max_length=200, unique=True, verbose_name='Registration Number'),
        ),
    ]
