from django.views import generic


class TopView(generic.TemplateView):
    template_name = 'user_auth/top.html'
