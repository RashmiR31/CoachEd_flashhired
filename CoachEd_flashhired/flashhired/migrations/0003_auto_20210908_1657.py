# Generated by Django 3.1.3 on 2021-09-08 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flashhired', '0002_user_phone_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_student',
            new_name='is_candidate',
        ),
    ]