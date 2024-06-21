from django.urls import path

from . import views

app_name = "dashboard"
urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path('api/training-templates/', views.training_templates, name='training_templates'),
]

