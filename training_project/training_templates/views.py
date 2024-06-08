from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import TrainingTemplate
from .forms import TrainingTemplateForm, AddExerciseForm
from exercises.models import Exercise


def create_training_template(request):
    if request.method == 'POST':
        form = TrainingTemplateForm(request.POST)
        if form.is_valid():
            training_template = form.save()
            request.session['training_template_id'] = training_template.id
            return redirect('create_training_template')  # Redirect to the same page to add exercises
    else:
        form = TrainingTemplateForm()

    exercises = Exercise.objects.all()
    return render(request, 'training_templates/create_training_template.html', {'form': form, 'exercises': exercises})


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
            if 'finish' in request.POST:
                del request.session['training_template_id']
                return redirect('training_template_list')
            return JsonResponse({'success': True, 'exercise_name': exercise.name})

    return JsonResponse({'success': False, 'error': 'Invalid data'})


def training_template_list(request):
    templates = TrainingTemplate.objects.all()
    return render(request, 'training_templates/training_template_list.html', {'templates': templates})
