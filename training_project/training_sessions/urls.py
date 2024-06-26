# training_session/urls.py
from django.urls import path
from .views import StartTrainingSessionView

urlpatterns = [
    path('start/<int:template_id>/', StartTrainingSessionView.as_view(), name='start_training_session'),
]

