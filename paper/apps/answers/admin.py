from django.contrib import admin
from .models import Participate, Answer, Select
# Register your models here.

class AnswerAdmin(admin.ModelAdmin):
    list_per_page = 15

    list_display = (
        'id', 'participate', 'content',
    )
    search_fields = ('content',)
class SelectAdmin(admin.ModelAdmin):
    list_per_page = 15

    list_display = (
        'id', 'answer', 'choice',
    )


admin.site.register(Participate)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Select, SelectAdmin)
