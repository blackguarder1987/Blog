from django.contrib import admin
from .models import Subscriber



class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'city', 'country', 'birthday']
    # list_filter = ['username', 'email']
    list_editable = ['city', 'country', 'birthday']

    def username(self, obj):
        return obj.user.username

    def email(self, obj):
        return obj.user.email


admin.site.register(Subscriber, SubscriberAdmin)