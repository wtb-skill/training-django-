from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import models
from django.db.models import F
from .models import TrainingTemplate, ExerciseOrder, Set, SetType
from .forms import TrainingTemplateForm, AddExerciseForm, SetForm
from exercises.models import Exercise


def get_exercises(training_template):
    selected_exercise_ids = ExerciseOrder.objects.filter(training_template=training_template).\
        values_list('exercise_id', flat=True)
    available_exercises = Exercise.objects.exclude(id__in=selected_exercise_ids)
    selected_exercises = ExerciseOrder.objects.filter(training_template=training_template).order_by('order') \
        if training_template else []
    return available_exercises, selected_exercises


def create_or_edit_training_template(request, template_id=None):
    if template_id:
        training_template = get_object_or_404(TrainingTemplate, id=template_id)
    else:
        training_template = None

    form = TrainingTemplateForm(instance=training_template)
    set_form = SetForm()

    if request.method == 'POST':
        if 'add-set-form' in request.POST:
            exercise_order_id = request.POST.get('exercise_order_id')
            exercise_order = ExerciseOrder.objects.get(pk=exercise_order_id)

            # Debug print
            print(f"[DEBUG] Adding new set to exercise_order_id: {exercise_order_id}")

            # Use create_empty method to create a new set
            new_set = Set.create_empty(exercise_order)

            # Debug print
            print(f"[DEBUG] New set created: {new_set}")

            return redirect('edit_training_template', template_id=template_id)
        elif 'add-warmup-set-form' in request.POST:
            exercise_order_id = request.POST.get('exercise_order_id')
            exercise_order = ExerciseOrder.objects.get(pk=exercise_order_id)

            new_warmup_set = Set.create_warmup(exercise_order)

            # Debug print
            print(f"[DEBUG] New set created: {new_warmup_set}")
            return redirect('edit_training_template', template_id=template_id)
        elif 'edit-set-form' in request.POST:
            set_id = request.POST.get('set_id')
            set_instance = get_object_or_404(Set, pk=set_id)

            # Debug print
            print(f"[DEBUG] Editing set id: {set_id}")

            # set_instance.set_type = request.POST.get('set_type')
            set_instance.reps = request.POST.get('reps')
            set_instance.weight = request.POST.get('weight')
            set_instance.save()
            return redirect('edit_training_template', template_id=template_id)

        elif 'name-form' in request.POST:
            form = TrainingTemplateForm(request.POST, instance=training_template)
            if form.is_valid():
                training_template = form.save()
                return redirect('edit_training_template', template_id=training_template.id)

    available_exercises, selected_exercises = get_exercises(training_template)

    return render(request, 'training_templates/create_training_template.html', {
        'form': form,
        'set_form': set_form,
        'exercises': available_exercises,
        'selected_exercises': selected_exercises,
        'template_id': template_id,
    })


def add_exercise(request, template_id):
    training_template = get_object_or_404(TrainingTemplate, id=template_id)
    print(f"[add_exercise] template_id = {template_id}")  # debug

    available_exercises, selected_exercises = get_exercises(training_template)
    print("Number of available exercises:", available_exercises.count())  # debug

    if request.method == 'POST':
        form = AddExerciseForm(request.POST, available_exercises=available_exercises)
        if form.is_valid():
            exercise = form.cleaned_data['exercise']

            last_order = \
            ExerciseOrder.objects.filter(training_template=training_template).aggregate(models.Max('order'))[
                'order__max'] or 0
            ExerciseOrder.objects.create(training_template=training_template, exercise=exercise, order=last_order + 1)
            return redirect('edit_training_template', template_id=template_id)
    else:
        form = AddExerciseForm(available_exercises=available_exercises)

    return render(request, 'training_templates/create_training_template.html', {
        'form': form,
        'selected_exercises': selected_exercises,
        'exercises': available_exercises,  # Pass available_exercises to the template
        'template_id': template_id,
    })


def delete_exercise(request, template_id, exercise_id):
    training_template = get_object_or_404(TrainingTemplate, id=template_id)
    exercise_order = get_object_or_404(ExerciseOrder, training_template=training_template, exercise_id=exercise_id)
    exercise_order.delete()

    # Reorder the remaining exercises
    remaining_exercises = ExerciseOrder.objects.filter(training_template=training_template).order_by('order')
    for index, exercise_order in enumerate(remaining_exercises):
        exercise_order.order = index + 1
        exercise_order.save()

    return redirect('edit_training_template', template_id=template_id)


def delete_set(request, template_id, set_id):
    set_instance = get_object_or_404(Set, pk=set_id)
    exercise_order = set_instance.exercise_order
    set_instance.delete()

    # Reorder the remaining sets
    remaining_sets = Set.objects.filter(exercise_order=exercise_order).order_by('set_type')
    if SetType.is_warm_up(set_instance.set_type):
        # If the deleted set was a warm-up, reorder only the warm-ups
        warm_up_sets = remaining_sets.filter(set_type=SetType.WARM_UP)
        for index, warmup_set in enumerate(warm_up_sets):
            warmup_set.set_type = SetType.WARM_UP
            warmup_set.save()
    else:
        # If the deleted set was numbered, reorder the numbered sets
        numbered_sets = remaining_sets.filter(set_type__regex=r'^\d+$')
        for index, numbered_set in enumerate(numbered_sets):
            numbered_set.set_type = str(index + 1)
            numbered_set.save()

    return redirect('edit_training_template', template_id=template_id)


def move_up_exercise(request, template_id, exercise_id):
    training_template = get_object_or_404(TrainingTemplate, id=template_id)
    current_exercise_order = get_object_or_404(ExerciseOrder, training_template=training_template,
                                               exercise_id=exercise_id)

    # Get the exercise order above the current exercise
    exercise_above = ExerciseOrder.objects.filter(training_template=training_template,
                                                  order=current_exercise_order.order - 1).first()

    if exercise_above:
        # Swap the orders using F expressions to update the database atomically
        current_exercise_order.order, exercise_above.order = exercise_above.order, current_exercise_order.order
        current_exercise_order.save()
        exercise_above.save()

    return redirect('edit_training_template', template_id=template_id)


def move_down_exercise(request, template_id, exercise_id):
    training_template = get_object_or_404(TrainingTemplate, id=template_id)
    current_exercise_order = get_object_or_404(ExerciseOrder, training_template=training_template,
                                               exercise_id=exercise_id)

    # Get the exercise order below the current exercise
    exercise_below = ExerciseOrder.objects.filter(training_template=training_template,
                                                  order=current_exercise_order.order + 1).first()

    if exercise_below:
        # Swap the orders using F expressions to update the database atomically
        current_exercise_order.order, exercise_below.order = exercise_below.order, current_exercise_order.order
        current_exercise_order.save()
        exercise_below.save()

    return redirect('edit_training_template', template_id=template_id)


def finish_template(request):
    return redirect('training_template_list')


def training_template_list(request):
    templates = TrainingTemplate.objects.all()
    template_exercises = [(template, ExerciseOrder.objects.filter(training_template=template).order_by('order'))
                          for template in templates]
    return render(request, 'training_templates/training_template_list.html', {'template_exercises': template_exercises})


def delete_template(request, template_id):
    template = get_object_or_404(TrainingTemplate, id=template_id)
    template.delete()
    return redirect('training_template_list')


