# Generated by Django 2.2.6 on 2020-01-08 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hm', '0007_classroomreport_healthinformation_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroomreport',
            name='child',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='hm.Student'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='healthinformation',
            name='child',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='hm.Student'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parent',
            name='child',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='hm.Student'),
            preserve_default=False,
        ),
    ]