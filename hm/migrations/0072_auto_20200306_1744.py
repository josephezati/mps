# Generated by Django 2.2.6 on 2020-03-06 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hm', '0071_auto_20200306_1739'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='reg_no',
        ),
        migrations.AlterField(
            model_name='reply',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hm.Message'),
        ),
    ]
