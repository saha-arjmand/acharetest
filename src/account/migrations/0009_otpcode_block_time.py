# Generated by Django 4.2 on 2023-04-26 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_remove_otpcode_code_remove_otpcode_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='otpcode',
            name='block_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
