# Generated by Django 3.0.6 on 2020-06-14 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mazeData', '0004_remove_users_salt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
