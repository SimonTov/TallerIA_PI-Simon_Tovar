from django.db import models
from django.conf import settings
import os

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    director = models.CharField(max_length=100, blank=True, null=True)
    genre = models.CharField(max_length=50, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    poster = models.ImageField(upload_to="movie/images/", blank=True, null=True)  # 👈 campo para la imagen

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        """
        Si tiene un poster guardado en BD, devuelve su URL.
        Si no, busca en media/movie/images con varias extensiones basadas en el título.
        """
        if self.poster:  # usa el campo de Django si existe
            return self.poster.url

        folder = os.path.join(settings.MEDIA_ROOT, 'movie', 'images')
        if not os.path.isdir(folder):
            return None

        exts = ['jpg', 'jpeg', 'png', 'webp', 'JPG', 'JPEG', 'PNG', 'WEBP']

        candidates = [
            self.title,
            self.title.replace(' ', '_'),
            self.title.replace(' ', '')
        ]
        safe = ''.join(c for c in self.title if c.isalnum() or c in " -_").strip()
        if safe and safe not in candidates:
            candidates.append(safe)

        for name in candidates:
            for ext in exts:
                filename = f"{name}.{ext}"
                full = os.path.join(folder, filename)
                if os.path.exists(full):
                    return os.path.join(
                        settings.MEDIA_URL.rstrip('/'),
                        'movie', 'images', filename
                    )
        return None
