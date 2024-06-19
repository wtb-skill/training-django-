# training_templates/models.py

from django.db import models
from exercises.models import Exercise


class TrainingTemplate(models.Model):
    name = models.CharField(max_length=100)
    exercises = models.ManyToManyField(Exercise, through='ExerciseOrder')

    def __str__(self):
        exercises_list = self.exercises.all()
        exercises_str = "\n".join([f"Exercise {idx + 1}: {exercise.name}" for idx, exercise in enumerate(exercises_list)])
        return f"Name: {self.name}\n{exercises_str}"


class ExerciseOrder(models.Model):
    training_template = models.ForeignKey(TrainingTemplate, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']


class SetType(models.TextChoices):
    WARM_UP = 'W', 'Warm-up'  # Warm-up
    NUMBERED = 'N', 'Numbered'  # Numbered sets (1, 2, 3, ...)

    @classmethod
    def is_warm_up(cls, set_type):
        return set_type == cls.WARM_UP

    @classmethod
    def is_numbered(cls, set_type):
        return set_type == cls.NUMBERED


class Set(models.Model):
    exercise_order = models.ForeignKey(ExerciseOrder, related_name='sets', on_delete=models.CASCADE)
    set_type = models.CharField(max_length=2, choices=SetType.choices, default=SetType.NUMBERED)
    weight = models.FloatField()
    reps = models.IntegerField()

    def __str__(self):
        return f"Set for {self.exercise_order} - Type: {self.get_set_type_display()}, Reps: {self.reps}, Weight: {self.weight}"

    class Meta:
        ordering = [
            models.Case(
                models.When(set_type='W', then=models.Value(0)),
                models.When(set_type__regex=r'^\d+$', then=models.Value(1)),
                default=models.Value(2),
                output_field=models.IntegerField(),
            ),
            models.Case(
                models.When(set_type='W', then=models.Value(0)),
                default=models.F('set_type'),
                output_field=models.IntegerField(),
            )
        ]

    @classmethod
    def create_empty(cls, exercise_order):
        # Find the highest numbered set type for the exercise_order
        numbered_sets = cls.objects.filter(
            exercise_order=exercise_order,
            set_type__regex=r'^\d+$'  # Regex to match only numbered sets
        )
        if numbered_sets.exists():
            highest_numbered_set = max(int(set.set_type) for set in numbered_sets)
            next_set_number = highest_numbered_set + 1
        else:
            next_set_number = 1
        return cls.objects.create(exercise_order=exercise_order, set_type=str(next_set_number), weight=0.0, reps=0)

    @classmethod
    def create_warmup(cls, exercise_order):

        return cls.objects.create(exercise_order=exercise_order, set_type='W', weight=0.0, reps=0)

    


