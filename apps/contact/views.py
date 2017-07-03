from django.views import generic


class IndexView(generic.ListView):
    template_name = 'contact.html'

    def get_queryset(self):
        return
