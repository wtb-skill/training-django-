from django.http import HttpResponse
from django.db.models import F
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic


class DashboardView(generic.TemplateView):
    template_name = "dashboard/dashboard.html"

