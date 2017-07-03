from django.conf.urls import url

from . import views

# a namespace to specify which app
app_name = 'recommend'


urlpatterns = [
    url(r'^$', views.recommend, name='recommendation'),
]

