from django.apps import AppConfig


# Responsibilities: Manage the creation, updating, and deletion of training templates.
# Features: CRUD operations for training templates, list of available templates, details of each template.

class TrainingTemplatesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'training_templates'
