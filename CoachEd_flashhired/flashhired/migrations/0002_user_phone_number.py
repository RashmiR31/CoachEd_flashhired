# Generated by Django 3.1.3 on 2021-09-08 10:39

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('flashhired', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(default=0, max_length=128, region=None),
            preserve_default=False,
        ),
    ]