from django.conf.urls import url

from . import views

app_name = "moviefy_lstm"

urlpatterns = [
    url(r'^$', views.LSTMView.as_view(), name="index"),
]
