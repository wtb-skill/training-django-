# training_templates/models.py

from django.db import models
from exercises.models import Exercise


class TrainingTemplate(models.Model):
    name = models.CharField(max_length=100)
    exercises = models.ManyToManyField(Exercise)

    def __str__(self):
        exercises_list = self.exercises.all()
        exercises_str = "\n".join([f"Exercise {idx + 1}: {exercise.name}" for idx, exercise in enumerate(exercises_list)])
        return f"Name: {self.name}\n{exercises_str}"

