from django.shortcuts import render
from django.http import HttpResponse
from visualize.views import show_planner

def index(request):
    return HttpResponse("Hello, world. You're at the wcoa index.")

def show_wcoa_planner(request, template='wcoa/visualize/planner.html'):
    return show_planner(request, template)
