# Generated by Django 3.0.6 on 2020-06-14 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mazeData', '0002_auto_20200614_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='userName',
            field=models.CharField(max_length=35, unique=True),
        ),
    ]
