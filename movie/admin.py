from django.contrib import admin
from .models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'director', 'genre', 'rating')
    search_fields = ('title', 'director', 'genre')
    list_filter = ('genre', 'release_date')
