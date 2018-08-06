from django.core import mail
from django.views.generic import View
from braces.views import LoginRequiredMixin

class MailView(View, LoginRequiredMixin):
    def post(self, request):
        pass


