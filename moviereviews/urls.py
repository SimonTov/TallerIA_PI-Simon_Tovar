"""
URL configuration for moviereviews project.
"""

from django.contrib import admin
from django.urls import path, include
from movie import views as movieViews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home y páginas principales
    path('', movieViews.home, name='home'),
    path('about/', movieViews.about, name='about'),
    path('statistics/', movieViews.statistics_view, name='statistics'),
    path('signup/', movieViews.signup, name='signup'),

    # Apps
    path('news/', include('news.urls')),
    path('movies/', include('movie.urls')),
]

# 👇 Esto permite servir archivos de media en modo desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
