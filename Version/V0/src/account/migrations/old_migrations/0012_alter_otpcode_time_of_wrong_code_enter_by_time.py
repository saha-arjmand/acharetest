# Generated by Django 4.2 on 2023-04-16 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_alter_otpcode_time_of_wrong_code_enter_by_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpcode',
            name='time_of_wrong_code_enter_by_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
