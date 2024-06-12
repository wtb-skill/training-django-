from django import forms
from .models import TrainingTemplate
from exercises.models import Exercise


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


# class AddExerciseForm(forms.Form):
#     exercise = forms.ModelChoiceField(queryset=Exercise.objects.all())