# Generated by Django 3.1.3 on 2021-12-12 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashhired', '0011_auto_20211210_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobposting',
            name='vacancies',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jobposting',
            name='required_cgpa',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
        migrations.AlterField(
            model_name='languages',
            name='proficiency',
            field=models.CharField(choices=[('native/bilingualproficiency', 'Native/Bilingual Proficiency'), ('fullprofessionalproficiency', 'Full Professional Proficiency'), ('elementaryproficiency', 'Elementary Proficiency'), ('professionalworkingproficiency', 'Professional Working Proficiency'), ('limitedworkingproficiency', 'Limited Working Proficiency')], max_length=100),
        ),
    ]
