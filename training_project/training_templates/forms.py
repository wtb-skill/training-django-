from django import forms
from .models import TrainingTemplate
from exercises.models import Exercise, Set


class TrainingTemplateForm(forms.ModelForm):
    class Meta:
        model = TrainingTemplate
        fields = ['name']


class AddExerciseForm(forms.Form):
    def __init__(self, *args, available_exercises=None, **kwargs):
        super(AddExerciseForm, self).__init__(*args, **kwargs)
        if available_exercises is not None:
            self.fields['exercise'].queryset = available_exercises

    exercise = forms.ModelChoiceField(queryset=Exercise.objects.none())


class SetForm(forms.ModelForm):
    class Meta:
        model = Set
        fields = ['set_type', 'weight', 'reps']

