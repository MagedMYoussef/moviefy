from django.views import generic


class IndexView(generic.ListView):
    template_name = 'howitworks.html'

    def get_queryset(self):
        return
