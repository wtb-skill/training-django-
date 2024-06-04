from django.apps import AppConfig


# Responsibilities: Manage the actual training sessions where users perform their exercises based on selected templates.
# Features: Start a training session, list of exercises for the session, marking exercises as complete, recording weights/reps/sets.

class TrainingSessionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'training_sessions'
