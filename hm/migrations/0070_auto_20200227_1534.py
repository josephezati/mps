# Generated by Django 2.2.6 on 2020-02-27 12:34

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import hm.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hm', '0069_auto_20200227_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hm.Message'),
        ),
        migrations.CreateModel(
            name='SetFees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('year', models.IntegerField(default=hm.models.current_year, validators=[django.core.validators.MinValueValidator(2020), hm.models.max_value_current_year])),
                ('amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(500)])),
                ('fees_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hm.Classe')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hm.Term')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]