from django.shortcuts import render
from django.views.generic.base import TemplateView


class MainMenuView(TemplateView):
    template_name = 'mini_app/index.html'
