# Generated by Django 5.1.1 on 2025-05-09 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('decor', '0015_remove_contactmessage_subject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactmessage',
            name='phone_number',
        ),
    ]
