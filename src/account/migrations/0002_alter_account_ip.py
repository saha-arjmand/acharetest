# Generated by Django 4.1.7 on 2023-04-12 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='ip',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
