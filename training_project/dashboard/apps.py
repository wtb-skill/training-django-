from django.apps import AppConfig


# Responsibilities: Provide an overview of user activities and quick access to different parts of the application.
# Features: Main menu with options like starting a new training session, viewing training history, accessing templates, etc.

class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'
