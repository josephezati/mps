# Generated by Django 2.2.6 on 2020-02-13 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hm', '0042_book_lendbookchild_lendbookstaff'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='uploads',
            field=models.FileField(blank=True, null=True, upload_to='book_uploads'),
        ),
    ]