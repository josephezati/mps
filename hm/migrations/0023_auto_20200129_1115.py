# Generated by Django 2.2.6 on 2020-01-29 08:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hm', '0022_schoolrequirement_child'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolrequirement',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hm.SchoolItem'),
        ),
        migrations.CreateModel(
            name='GatePass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.IntegerField(verbose_name='Duration in Days')),
                ('reason', models.CharField(max_length=200)),
                ('picked_by', models.CharField(max_length=200)),
                ('authorized_by', models.CharField(max_length=200)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('return_date', models.DateField(default=django.utils.timezone.now)),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hm.Student')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
