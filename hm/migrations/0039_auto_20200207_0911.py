# Generated by Django 2.2.6 on 2020-02-07 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hm', '0038_unitmeasure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='unit_measure',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
