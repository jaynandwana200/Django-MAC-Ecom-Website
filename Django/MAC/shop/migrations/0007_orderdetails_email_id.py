# Generated by Django 3.2.1 on 2024-09-23 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20210120_0852'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetails',
            name='Email_id',
            field=models.EmailField(default='', max_length=100),
        ),
    ]
