# Generated by Django 2.2.6 on 2020-02-05 10:20

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import hm.models


class Migration(migrations.Migration):

    dependencies = [
        ('hm', '0032_auto_20200205_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='mark',
            name='stream',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='hm.Stream'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mark',
            name='year',
            field=models.IntegerField(default=hm.models.current_year, validators=[django.core.validators.MinValueValidator(2020), hm.models.max_value_current_year]),
        ),
        migrations.AlterField(
            model_name='mark',
            name='marks_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hm.Classe'),
        ),
    ]
