# training_session/urls.py
from django.urls import path
from .views import StartTrainingSessionView, ProcessTrainingSessionView

urlpatterns = [
    path('start/<int:template_id>/', StartTrainingSessionView.as_view(), name='start_training_session'),
    path('process/<int:session_id>/', ProcessTrainingSessionView.as_view(), name='process_training_session'),
]

