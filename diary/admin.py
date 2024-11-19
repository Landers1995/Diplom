from django.contrib import admin
from diary.models import Diary


@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'body', 'create_date', 'user',)
    list_filter = ('user', 'title', 'create_date',)
    search_fields = ('user',)
