# dashboard\views.py
from django.views import generic
from django.http import JsonResponse
from training_templates.models import TrainingTemplate


class DashboardView(generic.TemplateView):
    template_name = "dashboard/dashboard.html"


def training_templates(request):
    templates = TrainingTemplate.objects.all().values('id', 'name')
    return JsonResponse({'templates': list(templates)})
