from django.conf.urls import url

from . import views

# a namespace to specify which app
app_name = 'contact'


urlpatterns = [
        url(r'^$', views.IndexView.as_view(), name='index'),
]

