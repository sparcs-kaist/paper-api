from django.contrib import admin
from .models import Paper, Question, Choice

# Register your models here.
admin.site.register(Paper)
admin.site.register(Question)
admin.site.register(Choice)