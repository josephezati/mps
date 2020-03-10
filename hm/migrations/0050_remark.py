# Generated by Django 2.2.6 on 2020-02-17 19:26

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import hm.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hm', '0049_examset_short_form'),
    ]

    operations = [
        migrations.CreateModel(
            name='Remark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remark', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('year', models.IntegerField(default=hm.models.current_year, validators=[django.core.validators.MinValueValidator(2020), hm.models.max_value_current_year])),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hm.Student')),
                ('marks_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hm.Classe')),
                ('stream', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hm.Stream')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hm.Term')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('child', 'term', 'year', 'marks_class')},
            },
        ),
    ]