# exercises/models.py

from django.db import models


class BodyPart(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']  # Specify ordering by the 'name' field


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    main_body_part = models.ForeignKey(BodyPart, on_delete=models.CASCADE, related_name='main_body_exercises')
    additional_body_parts = models.ManyToManyField(BodyPart, related_name='additional_body_exercises', blank=True)

    def __str__(self):
        return self.name

    def get_main_body_part_name(self):
        return self.main_body_part.name

    class Meta:
        ordering = ['main_body_part', 'name']  # Specify ordering by the main body part and then by name
