# exercises/admin.py

from django.contrib import admin
from .models import Exercise, BodyPart


class ExerciseAdmin(admin.ModelAdmin):
    filter_vertical = ['additional_body_parts']

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'additional_body_parts':
            # Get the exercise object being edited/added
            obj = kwargs.get('obj')

            # Exclude the main body part from the queryset
            if obj and obj.main_body_part:
                kwargs['queryset'] = BodyPart.objects.exclude(id=obj.main_body_part.id)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(BodyPart)
