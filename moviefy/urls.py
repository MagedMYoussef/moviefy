from django.conf.urls import  include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    # Examples:
    # url(r'^$', 'moviefy.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/', include('homepage.urls')),

    # Redirect the base URL to our home application
    url(r'^$', RedirectView.as_view(url='/home/', permanent=True)),

    # Try it out page
    url(r'^try/', include('tryitout.urls')),

    # Recommendation
    url(r'^recommend/', include('recommend.urls')),

    # Model API
    url(r'^modelapi/', include('moviefy_lstm.urls')),

    # User Profile
    # \w will match any word characters and digits
    url(r'^user/(?P<username>\w+)/', include('user_profile.urls')),

]