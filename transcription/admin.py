from django.contrib import admin
from transcription.models import Commands, UsersTexts, AudioFile

# Register your models here.
@admin.register(Commands)
class CommandsAdmin(admin.ModelAdmin):
    list_display = ('commands', 'confirmation', 'slug',)
    list_filter = ('commands',)
    search_fields = ('commands', 'confirmation',)
    prepopulated_fields = {'slug': ('commands',)} # автозаполнение слага в админке по команде

@admin.register(UsersTexts)
class UsersTextsAdmin(admin.ModelAdmin):
    list_display = ('usertext', 'created',)
    list_filter = ('created',)
    search_fields = ('usertext', 'created',)

# @admin.register(AudioFile)
# class AudioFileAdmin(admin.ModelAdmin):
#     list_display = ('audio_file',)
