from django.core import mail
from .models import PaperMail

class MailHelpers():

    def __init__(self, sender, receivers):
        self.sender = sender
        self.receivers = self.receivers

    def saveMail(self, subject, content):
        instance = PaperMail(sender_address=self.sender.email, subject=subject, content=content)
        receiver_address_list = []
        for receiver in self.receivers:
            receiver_address_list.append(receiver.email)
        instance.set_receivers_address(receiver_address_list)
        instance.save()