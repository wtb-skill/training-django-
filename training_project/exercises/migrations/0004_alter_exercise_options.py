# Generated by Django 5.0.6 on 2024-06-06 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0003_alter_exercise_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exercise',
            options={'ordering': ['main_body_part', 'name']},
        ),
    ]
