from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from django.contrib.auth.views import logout

urlpatterns = [
    # Examples:
    # url(r'^$', 'moviefy.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/', include('apps.homepage.urls')),

    # Redirect the base URL to our home application
    url(r'^$', RedirectView.as_view(url='/home/', permanent=True)),

    # Try it out page
    url(r'^try/', include('apps.tryitout.urls')),

    # Recommendation
    url(r'^recommend/', include('apps.recommend.urls')),

    # Model API
    url(r'^modelapi/', include('apps.moviefy_lstm.urls')),

    # User Profile
    # \w will match any word characters and digits
    # url(r'^user/(?P<username>\w+)/', include('user_profile.urls')),
    url(r'^profile/', include('apps.user_profile.urls')),

    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/logout/$', logout,
     {'next_page': '/accounts/login'}),

    # About
    url(r'^about/', include('apps.about.urls')),

    # Contact
    url(r'^contact/', include('apps.contact.urls')),

    # How it works
    url(r'^howitworks/', include('apps.howitworks.urls')),
]
