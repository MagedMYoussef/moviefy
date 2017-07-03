from django.views import generic


class IndexView(generic.ListView):
    template_name = 'about.html'

    def get_queryset(self):
        return
