# training_history/views.py

from django.views.generic import ListView
from training_sessions.models import TrainingSession
from django.utils import timezone

class TrainingSessionHistoryView(ListView):
    model = TrainingSession
    template_name = 'training_history/history.html'
    context_object_name = 'training_sessions'
    ordering = ['-start_time']

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('session_exercises__session_sets')

        # Add duration details to the session
        for session in queryset:
            if session.start_time and session.end_time:
                session.duration = session.end_time - session.start_time
            elif session.start_time:
                # If the session is still ongoing, calculate the duration until now
                session.duration = timezone.now() - session.start_time
            else:
                session.duration = None

            # Precompute hours, minutes, seconds for easier template rendering
            if session.duration:
                total_seconds = session.duration.total_seconds()
                session.hours = int(total_seconds // 3600)
                session.minutes = int((total_seconds % 3600) // 60)
                session.seconds = int(total_seconds % 60)
            else:
                session.hours = session.minutes = session.seconds = 0

        return queryset

