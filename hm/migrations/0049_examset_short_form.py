# Generated by Django 2.2.6 on 2020-02-17 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hm', '0048_auto_20200217_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='examset',
            name='short_form',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
