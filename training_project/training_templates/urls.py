from django.urls import path
from .views import create_training_template, add_exercise, finish_template, training_template_list

urlpatterns = [
    path('create/', create_training_template, name='create_training_template'),
    path('add-exercise/', add_exercise, name='add_exercise'),
    path('finish/', finish_template, name='finish_template'),
    path('', training_template_list, name='training_template_list'),
]
