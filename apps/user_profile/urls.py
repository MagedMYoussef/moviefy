from django.conf.urls import url

from . import views

# a namespace to specify which app
app_name = 'user_profile'


urlpatterns = [
    url(r'^$', views.profile, name='profile'),
    # If we get an API request
    url(r'^api/', views.UserProfileView.as_view(), name='user_api'),

]

