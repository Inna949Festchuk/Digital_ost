from django.contrib import admin
from picasso.models import UsersPromts

# Register your models here.
@admin.register(UsersPromts)
class UsersPromtsAdmin(admin.ModelAdmin):
    list_display = ('usertext', 'created',)
    list_filter = ('created',)
    search_fields = ('usertext', 'created',)