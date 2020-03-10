# Generated by Django 2.2.6 on 2020-02-26 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hm', '0066_messagestatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='sender', to='hm.MessageStatus'),
        ),
    ]
