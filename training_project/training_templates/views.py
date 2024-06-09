from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import TrainingTemplate
from .forms import TrainingTemplateForm, AddExerciseForm
from exercises.models import Exercise


def create_training_template(request):
    training_template = None
    if 'training_template_id' in request.session:
        training_template_id = request.session['training_template_id']
        training_template = TrainingTemplate.objects.get(id=training_template_id)

    if request.method == 'POST':
        form = TrainingTemplateForm(request.POST, instance=training_template)
        if form.is_valid():
            training_template = form.save()
            request.session['training_template_id'] = training_template.id
            return redirect('create_training_template')  # Redirect to the same page to add exercises
    else:
        form = TrainingTemplateForm(instance=training_template)

    exercises = Exercise.objects.all()
    selected_exercises = training_template.exercises.all() if training_template else []

    return render(request, 'training_templates/create_training_template.html', {
        'form': form,
        'exercises': exercises,
        'selected_exercises': selected_exercises
    })


def add_exercise(request):
    if 'training_template_id' not in request.session:
        return redirect('create_training_template')

    training_template_id = request.session['training_template_id']
    training_template = TrainingTemplate.objects.get(id=training_template_id)

    if request.method == 'POST':
        form = AddExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.cleaned_data['exercise']
            training_template.exercises.add(exercise)
            return redirect('create_training_template')  # Redirect to the same page to add more exercises

    return redirect('create_training_template')


def finish_template(request):
    if 'training_template_id' in request.session:
        del request.session['training_template_id']
    return redirect('training_template_list')


def training_template_list(request):
    templates = TrainingTemplate.objects.all()
    return render(request, 'training_templates/training_template_list.html', {'templates': templates})


def edit_template(request, template_id):
    template = get_object_or_404(TrainingTemplate, id=template_id)
    if request.method == 'POST':
        form = TrainingTemplateForm(request.POST, instance=template)
        if form.is_valid():
            form.save()
            return redirect('training_template_list')
    else:
        form = TrainingTemplateForm(instance=template)
    return render(request, 'training_templates/edit_template.html', {'form': form})


def delete_template(request, template_id):
    template = get_object_or_404(TrainingTemplate, id=template_id)
    template.delete()
    return redirect('training_template_list')
