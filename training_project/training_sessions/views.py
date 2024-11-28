# training_session/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils import timezone
from django.urls import reverse
from .models import TrainingSession, SessionExercise, SessionSet
from training_templates.models import TrainingTemplate, ExerciseOrder, Set
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


class StartTrainingSessionView(View):
    def get(self, request, *args, **kwargs):
        training_template_id = kwargs.get('template_id')
        training_template = get_object_or_404(TrainingTemplate, pk=training_template_id)

        # Create a new TrainingSession
        training_session = TrainingSession.objects.create(template=training_template)

        # Create session exercises and sets
        exercise_orders = ExerciseOrder.objects.filter(training_template=training_template).select_related('exercise')
        for exercise_order in exercise_orders:
            session_exercise = SessionExercise.objects.create(session=training_session,
                                                              exercise=exercise_order.exercise)
            sets = Set.objects.filter(exercise_order=exercise_order)
            for set in sets:
                SessionSet.objects.create(session_exercise=session_exercise, set_type=set.set_type, reps=set.reps,
                                          weight=set.weight)

        # Pass the newly created session ID to the context
        context = {
            'training_template': training_template,
            'exercises_with_sets': [
                {
                    'exercise_order': eo,
                    'sets': SessionSet.objects.filter(session_exercise__exercise=eo.exercise,
                                                      session_exercise__session=training_session)
                } for eo in exercise_orders
            ],
            'session_id': training_session.id,
        }

        return render(request, 'training_sessions/start.html', context)


class ProcessTrainingSessionView(View):
    def post(self, request, *args, **kwargs):
        session_id = kwargs.get('session_id')
        training_session = get_object_or_404(TrainingSession, pk=session_id)

        # for key, value in request.POST.items():
        #     if key.startswith('set_') and key.endswith('_reps'):
        #         set_id = key.split('_')[1]
        #         session_set = get_object_or_404(SessionSet, pk=set_id)
        #         session_set.reps = int(value)
        #         session_set.save()
        #     elif key.startswith('set_') and key.endswith('_weight'):
        #         set_id = key.split('_')[1]
        #         session_set = get_object_or_404(SessionSet, pk=set_id)
        #         session_set.weight = float(value)
        #         session_set.save()

        # # Mark the session as completed and set the end time
        # training_session.is_completed = True
        # training_session.end_time = timezone.now()
        # training_session.save()

        return redirect('/')


class FinishTrainingSessionView(View):
    def post(self, request, *args, **kwargs):
        session_id = kwargs.get('session_id')
        training_session = get_object_or_404(TrainingSession, pk=session_id)

        for key, value in request.POST.items():
            if key.startswith('set_') and key.endswith('_reps'):
                set_id = key.split('_')[1]
                session_set = get_object_or_404(SessionSet, pk=set_id)
                session_set.reps = int(value)
                session_set.save()
            elif key.startswith('set_') and key.endswith('_weight'):
                set_id = key.split('_')[1]
                session_set = get_object_or_404(SessionSet, pk=set_id)
                session_set.weight = float(value)
                session_set.save()

        # Mark the session as completed and set the end time
        training_session.is_completed = True
        training_session.end_time = timezone.now()
        training_session.save()

        return redirect('/')


@csrf_exempt
def mark_set_completed(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)  # Debug incoming data
            set_id = data.get('set_id')
            is_completed = data.get('is_completed')

            session_set = SessionSet.objects.get(id=set_id)
            session_set.is_completed = is_completed
            session_set.save()

            print(session_set)  # Debug the saved instance

            return JsonResponse({'success': True})
        except (SessionSet.DoesNotExist, KeyError, ValueError) as e:
            print(e)  # Debug error
            return JsonResponse({'success': False, 'error': 'Invalid data.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)


