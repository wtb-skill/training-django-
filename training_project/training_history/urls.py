# training_history/urls.py

from django.urls import path
from .views import TrainingSessionHistoryView

urlpatterns = [
    path('', TrainingSessionHistoryView.as_view(), name='training_session_history'),
]
