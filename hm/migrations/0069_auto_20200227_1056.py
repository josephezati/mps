# Generated by Django 2.2.6 on 2020-02-27 07:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hm', '0068_auto_20200226_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message_body',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='hm.MessageStatus'),
        ),
        migrations.AlterField(
            model_name='message',
            name='uploads',
            field=models.FileField(blank=True, null=True, upload_to='email_uploads'),
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('reply_body', models.TextField(blank=True, null=True)),
                ('uploads', models.FileField(blank=True, null=True, upload_to='email_uploads')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hm.Message')),
                ('replyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replyer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
