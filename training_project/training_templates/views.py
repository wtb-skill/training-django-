from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import TrainingTemplate
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
    selected_exercises = training_template.exercises.all() if training_template else []

    return render(request, 'training_templates/create_training_template.html', {
        'form': form,
        'exercises': exercises,
        'selected_exercises': selected_exercises,
        'template_id': template_id,
    })


def add_exercise(request):
    template_id = request.session.get('template_id')
    training_template = get_object_or_404(TrainingTemplate, id=template_id)

    if request.method == 'POST':
        form = AddExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.cleaned_data['exercise']
            training_template.exercises.add(exercise)
            training_template.save()
            return redirect('edit_training_template', template_id=template_id)
    else:
        # If it's not a POST request, create a new form instance
        form = AddExerciseForm()

    return redirect('edit_training_template', template_id=template_id)


def finish_template(request):
    if 'training_template_id' in request.session:
        del request.session['training_template_id']
    return redirect('training_template_list')


def training_template_list(request):
    templates = TrainingTemplate.objects.all()
    return render(request, 'training_templates/training_template_list.html', {'templates': templates})


def delete_template(request, template_id):
    template = get_object_or_404(TrainingTemplate, id=template_id)
    template.delete()
    return redirect('training_template_list')
