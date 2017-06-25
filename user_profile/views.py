from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views import generic


def profile(request, username):
    return render(request, "profile.html")