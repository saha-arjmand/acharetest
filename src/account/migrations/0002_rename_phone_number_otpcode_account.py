# Generated by Django 4.2 on 2023-04-24 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='otpcode',
            old_name='phone_number',
            new_name='account',
        ),
    ]
