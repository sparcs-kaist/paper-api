from django.core.mail import send_mail
from .models import PaperMail

class MailHelpers():

    def __init__(self, paperMail):
        self.paperMail = paperMail

    def sendMail(self):
        send_mail(
            self.paperMail.subject,
            self.paperMail.message,
            self.paperMail.sender_address,
            self.paperMail.get_receivers_addresss(),
            fail_silently=False,
        )