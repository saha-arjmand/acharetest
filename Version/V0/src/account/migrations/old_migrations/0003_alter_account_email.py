# Generated by Django 4.2 on 2023-04-15 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_account_ip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(max_length=60, verbose_name='email'),
        ),
    ]
