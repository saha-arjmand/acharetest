# Generated by Django 4.2 on 2023-04-25 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_otpcode_wrong_code_enter_by_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='otpcode',
            name='wrong_code_enter_by_time2',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]