# Generated by Django 3.1.4 on 2023-10-22 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20231022_0624'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='usr_comment',
        ),
    ]
