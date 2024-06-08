# Generated by Django 5.0.6 on 2024-06-06 07:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BodyPart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('additional_body_parts', models.ManyToManyField(blank=True, related_name='additional_body_exercises', to='exercises.bodypart')),
                ('main_body_part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_body_exercises', to='exercises.bodypart')),
            ],
        ),
    ]