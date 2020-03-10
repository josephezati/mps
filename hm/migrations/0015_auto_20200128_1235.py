# Generated by Django 2.2.6 on 2020-01-28 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hm', '0014_income_received_from'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='uploads',
            field=models.FileField(blank=True, null=True, upload_to='expense_docs'),
        ),
        migrations.AddField(
            model_name='income',
            name='uploads',
            field=models.FileField(blank=True, null=True, upload_to='income_docs'),
        ),
    ]
