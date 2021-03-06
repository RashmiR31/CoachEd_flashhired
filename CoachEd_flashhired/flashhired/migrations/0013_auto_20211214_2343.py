# Generated by Django 3.1.3 on 2021-12-14 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashhired', '0012_auto_20211212_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='duration',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='languages',
            name='proficiency',
            field=models.CharField(choices=[('fullprofessionalproficiency', 'Full Professional Proficiency'), ('elementaryproficiency', 'Elementary Proficiency'), ('native/bilingualproficiency', 'Native/Bilingual Proficiency'), ('limitedworkingproficiency', 'Limited Working Proficiency'), ('professionalworkingproficiency', 'Professional Working Proficiency')], max_length=100),
        ),
    ]
