# training_history/views.py

from django.views.generic import ListView
from training_sessions.models import TrainingSession

class TrainingSessionHistoryView(ListView):
    model = TrainingSession
    template_name = 'training_history/history.html'
    context_object_name = 'training_sessions'
    ordering = ['-start_time']

    def get_queryset(self):
        # Optionally add some filtering or prefetching of related data
        return super().get_queryset().prefetch_related('session_exercises__session_sets')
