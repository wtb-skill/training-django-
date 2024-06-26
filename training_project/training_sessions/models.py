# training_session/models.py

from django.db import models
from django.contrib.auth.models import User
from training_templates.models import TrainingTemplate
from exercises.models import Exercise


class TrainingSession(models.Model):
    template = models.ForeignKey(TrainingTemplate, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.template.name} - {self.start_time}"


class SessionExercise(models.Model):
    session = models.ForeignKey(TrainingSession, related_name='session_exercises', on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.session} - {self.exercise.name}"


class SessionSet(models.Model):
    session_exercise = models.ForeignKey(SessionExercise, related_name='session_sets', on_delete=models.CASCADE)
    set_type = models.CharField(max_length=50)  # E.g., Warmup, Working
    reps = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.session_exercise} - {self.set_type} - {self.reps} reps - {self.weight} kg"
