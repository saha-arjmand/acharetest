# Generated by Django 4.2 on 2023-04-25 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_otpcode_wrong_code_enter_by_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpcode',
            name='wrong_code_enter_by_time',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
