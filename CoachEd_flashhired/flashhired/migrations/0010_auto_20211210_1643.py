# Generated by Django 3.1.3 on 2021-12-10 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashhired', '0009_auto_20211210_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skills',
            name='supporting_doc',
            field=models.FileField(blank=True, default=0, upload_to='candidate/skills'),
            preserve_default=False,
        ),
    ]
