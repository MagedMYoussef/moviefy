from django.shortcuts import render
from django.http import HttpResponse, Http404


def index(request):
    """
    View function for the Home of Moviefy site.
    """
    return render(request, 'index.html')