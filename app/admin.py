from django.contrib import admin
from . models import User, Poll, Question, PollAnswer, PollResponse
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, UserAdmin)
admin.site.register(Poll)
admin.site.register(PollAnswer)
admin.site.register(PollResponse)
admin.site.register(Question)