# Generated by Django 5.0.6 on 2024-06-20 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_item'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Item',
        ),
    ]
