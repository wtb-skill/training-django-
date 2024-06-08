# training_templates/models.py

from django.db import models
from exercises.models import Exercise


class TrainingTemplate(models.Model):
    name = models.CharField(max_length=100)
    exercises = models.ManyToManyField(Exercise)

    def __str__(self):
        return self.name
