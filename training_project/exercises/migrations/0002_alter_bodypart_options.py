# Generated by Django 5.0.6 on 2024-06-06 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bodypart',
            options={'ordering': ['name']},
        ),
    ]