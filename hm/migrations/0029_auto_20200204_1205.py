# Generated by Django 2.2.6 on 2020-02-04 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hm', '0028_auto_20200204_1159'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='teachersubject',
            unique_together={('subject', 'subject_class', 'term', 'stream', 'year')},
        ),
    ]