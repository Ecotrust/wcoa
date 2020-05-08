from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from  django.views.defaults import page_not_found as dj_page_not_found
from visualize.views import show_planner
from django.views.decorators.clickjacking import xframe_options_exempt

def index(request):
    return HttpResponse("Hello, world. You're at the wcoa index.")

def show_wcoa_planner(request, template='wcoa/visualize/planner.html'):
    return show_planner(request, template)

@xframe_options_exempt
def show_wcoa_embedded_map(request, template='wcoa/visualize/embedded.html'):
    return show_planner(request, template)

def page_not_found(request, exception=None, template='wcoa_404.html'):
    return dj_page_not_found(request, exception, template)
