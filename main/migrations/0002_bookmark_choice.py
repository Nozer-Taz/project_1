# Generated by Django 3.1 on 2021-08-23 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmark',
            name='choice',
            field=models.BooleanField(default=False),
        ),
    ]
