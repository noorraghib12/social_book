# Generated by Django 4.2.2 on 2023-10-22 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_followedcount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followedcount',
            name='following',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='followedcount',
            name='user',
            field=models.CharField(max_length=200),
        ),
    ]
