from django.urls import path
from .views import create_or_edit_training_template, add_exercise, delete_exercise, finish_template, \
    training_template_list, delete_template, move_up_exercise, move_down_exercise

urlpatterns = [
    path('create/', create_or_edit_training_template, name='create_training_template'),
    path('edit/<int:template_id>/', create_or_edit_training_template, name='edit_training_template'),
    path('add-exercise/<int:template_id>/', add_exercise, name='add_exercise'),
    path('delete-exercise/<int:template_id>/<int:exercise_id>/', delete_exercise, name='delete_exercise'),
    path('move-up-exercise/<int:template_id>/<int:exercise_id>/', move_up_exercise, name='move_up_exercise'),
    path('move-down-exercise/<int:template_id>/<int:exercise_id>/', move_down_exercise, name='move_down_exercise'),
    path('finish/', finish_template, name='finish_template'),
    path('', training_template_list, name='training_template_list'),
    path('delete/<int:template_id>/', delete_template, name='delete_template'),
]
