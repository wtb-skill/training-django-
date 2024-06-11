from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import models
from .models import TrainingTemplate, ExerciseOrder
from .forms import TrainingTemplateForm, AddExerciseForm
from exercises.models import Exercise


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

    exercises = Exercise.objects.all()
    selected_exercises = ExerciseOrder.objects.filter(training_template=training_template).order_by('order') if training_template else []

    return render(request, 'training_templates/create_training_template.html', {
        'form': form,
        'exercises': exercises,
        'selected_exercises': selected_exercises,
        'template_id': template_id,
    })


def add_exercise(request, template_id):
    training_template = get_object_or_404(TrainingTemplate, id=template_id)
    print(f"[add_exercise] template_id = {template_id}")  # debug

    if request.method == 'POST':
        form = AddExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.cleaned_data['exercise']
            last_order = ExerciseOrder.objects.filter(training_template=training_template).aggregate(models.Max('order'))['order__max'] or 0
            ExerciseOrder.objects.create(training_template=training_template, exercise=exercise, order=last_order + 1)
            return redirect('edit_training_template', template_id=template_id)
    else:
        form = AddExerciseForm()

    return render(request, 'training_templates/create_training_template.html', {
        'form': form,
        'selected_exercises': training_template.exercises.all(),
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
