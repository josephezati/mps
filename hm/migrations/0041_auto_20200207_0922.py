# Generated by Django 2.2.6 on 2020-02-07 06:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hm', '0040_auto_20200207_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='unit_measure',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='hm.UnitMeasure'),
        ),
    ]