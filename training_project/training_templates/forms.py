from django import forms
from .models import TrainingTemplate
from exercises.models import Exercise


class TrainingTemplateForm(forms.ModelForm):
    class Meta:
        model = TrainingTemplate
        fields = ['name']


class AddExerciseForm(forms.Form):
    exercise = forms.ModelChoiceField(queryset=Exercise.objects.all())
