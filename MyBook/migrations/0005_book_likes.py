# Generated by Django 2.0 on 2017-12-21 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyBook', '0004_auto_20171220_2321'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
