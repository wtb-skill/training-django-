from django.apps import AppConfig


# Responsibilities: Track and display the history of user training sessions.
# Features: List of past training sessions, details of each session, progress tracking over time.


class TrainingHistoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'training_history'
