from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import models
from django.db.models import F
from .models import TrainingTemplate, ExerciseOrder
from .forms import TrainingTemplateForm, AddExerciseForm
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
        print(f"template_id = {template_id}")  # debug
    else:
        training_template = None
        print("No template_id.")  # debug

    if request.method == 'POST':
        form = TrainingTemplateForm(request.POST, instance=training_template)
        if form.is_valid():
            training_template = form.save()
            request.session['template_id'] = training_template.id
            return redirect('edit_training_template', template_id=training_template.id)
    else:
        form = TrainingTemplateForm(instance=training_template)

    available_exercises, selected_exercises = get_exercises(training_template)

    return render(request, 'training_templates/create_training_template.html', {
        'form': form,
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


def move_up_exercise(request, template_id, exercise_id):
    training_template = get_object_or_404(TrainingTemplate, id=template_id)
    current_exercise_order = get_object_or_404(ExerciseOrder, training_template=training_template, exercise_id=exercise_id)

    # Get the exercise order above the current exercise
    exercise_above = ExerciseOrder.objects.filter(training_template=training_template, order=current_exercise_order.order - 1).first()

    if exercise_above:
        # Swap the orders using F expressions to update the database atomically
        current_exercise_order.order, exercise_above.order = exercise_above.order, current_exercise_order.order
        current_exercise_order.save()
        exercise_above.save()

    return redirect('edit_training_template', template_id=template_id)


def move_down_exercise(request, template_id, exercise_id):
    training_template = get_object_or_404(TrainingTemplate, id=template_id)
    current_exercise_order = get_object_or_404(ExerciseOrder, training_template=training_template, exercise_id=exercise_id)

    # Get the exercise order below the current exercise
    exercise_below = ExerciseOrder.objects.filter(training_template=training_template, order=current_exercise_order.order + 1).first()

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
    template_exercises = [(template, ExerciseOrder.objects.filter(training_template=template).order_by('order')) for template in templates]
    return render(request, 'training_templates/training_template_list.html', {'template_exercises': template_exercises})


def delete_template(request, template_id):
    template = get_object_or_404(TrainingTemplate, id=template_id)
    template.delete()
    return redirect('training_template_list')
