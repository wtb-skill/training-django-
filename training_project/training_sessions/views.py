# training_session/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import TrainingSession, SessionExercise, SessionSet
from training_templates.models import TrainingTemplate, ExerciseOrder, Set


class StartTrainingSessionView(View):
    def get(self, request, *args, **kwargs):
        training_template_id = kwargs.get('template_id')
        training_template = get_object_or_404(TrainingTemplate, pk=training_template_id)

        # Get exercise orders with related exercises
        exercise_orders = ExerciseOrder.objects.filter(training_template=training_template).select_related('exercise')

        # Prepare a dictionary to hold exercises and their sets
        exercises_with_sets = []
        for exercise_order in exercise_orders:
            sets = Set.objects.filter(exercise_order=exercise_order)
            exercises_with_sets.append({
                'exercise_order': exercise_order,
                'sets': sets
            })

        context = {
            'training_template': training_template,
            'exercises_with_sets': exercises_with_sets,
        }

        return render(request, 'training_sessions/start.html', context)


# class ProcessTrainingSessionView(View):
#     def get(self, request, session_id):
#         session = TrainingSession.objects.get(id=session_id)
#         return render(request, 'training_session/start.html', {'session': session})
#
#     def post(self, request, session_id):
#         session = TrainingSession.objects.get(id=session_id)
#         for exercise in session.session_exercises.all():
#             exercise.is_completed = request.POST.get(f'exercise_{exercise.id}_completed') == 'on'
#             exercise.save()
#             for set in exercise.session_sets.all():
#                 set.is_completed = request.POST.get(f'set_{set.id}_completed') == 'on'
#                 set.save()
#
#         session.is_completed = all(ex.is_completed for ex in session.session_exercises.all())
#         if session.is_completed:
#             session.end_time = timezone.now()
#         session.save()
#
#         return redirect('some_finish_view')

