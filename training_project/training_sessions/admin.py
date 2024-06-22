# training_session/admin.py

from django.contrib import admin
from .models import TrainingSession, SessionExercise, SessionSet

admin.site.register(TrainingSession)
admin.site.register(SessionExercise)
admin.site.register(SessionSet)
