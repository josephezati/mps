# Generated by Django 2.2.6 on 2020-01-29 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hm', '0021_schoolitem_schoolrequirement'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolrequirement',
            name='child',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='hm.Student'),
            preserve_default=False,
        ),
    ]
