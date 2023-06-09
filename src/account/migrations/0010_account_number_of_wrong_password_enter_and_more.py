# Generated by Django 4.2 on 2023-04-26 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_otpcode_block_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='number_of_wrong_password_enter',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='account',
            name='user_block',
            field=models.BooleanField(default=False),
        ),
    ]
