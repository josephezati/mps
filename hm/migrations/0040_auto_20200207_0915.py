# Generated by Django 2.2.6 on 2020-02-07 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hm', '0039_auto_20200207_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='unit_measure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hm.UnitMeasure'),
        ),
    ]