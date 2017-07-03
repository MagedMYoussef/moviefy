from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'tryitout.html'

    def get_queryset(self):
        return
