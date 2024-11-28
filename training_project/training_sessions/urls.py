# training_session/urls.py
from django.urls import path
from .views import StartTrainingSessionView, ProcessTrainingSessionView, FinishTrainingSessionView, mark_set_completed

urlpatterns = [
    path('start/<int:template_id>/', StartTrainingSessionView.as_view(), name='start_training_session'),
    path('process/<int:session_id>/', ProcessTrainingSessionView.as_view(), name='process_training_session'),
    path('finish/<int:session_id>/', FinishTrainingSessionView.as_view(), name='finish_training_session'),
    path('mark-set-completed/', mark_set_completed, name='mark_set_completed'),
]

