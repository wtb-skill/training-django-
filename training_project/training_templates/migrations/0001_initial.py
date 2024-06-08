# Generated by Django 5.0.6 on 2024-06-06 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('exercises', '0004_alter_exercise_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('exercises', models.ManyToManyField(to='exercises.exercise')),
            ],
        ),
    ]