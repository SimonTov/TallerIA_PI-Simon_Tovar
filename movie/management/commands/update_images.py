import os
import re
from django.core.management.base import BaseCommand
from django.core.files import File
from movie.models import Movie

class Command(BaseCommand):
    help = "Actualiza las imágenes de todas las películas desde media/movie/images"

    def handle(self, *args, **kwargs):
        images_path = os.path.join("media", "movie", "images")

        if not os.path.exists(images_path):
            self.stdout.write(self.style.ERROR(f"❌ No se encontró la carpeta {images_path}"))
            return

        updated = 0
        total = Movie.objects.count()

        for movie in Movie.objects.all():
            # Normalizamos el nombre de la película para buscar el archivo
            safe_title = re.sub(r'[^a-z0-9]+', '_', movie.title.lower())
            filename = f"{safe_title}.jpg"
            file_path = os.path.join(images_path, filename)

            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    movie.poster.save(filename, File(f), save=True)
                updated += 1
                self.stdout.write(self.style.SUCCESS(f"✅ Imagen actualizada: {movie.title}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠ No se encontró imagen para: {movie.title} (buscado: {filename})"))

        self.stdout.write(self.style.SUCCESS(
            f"🎉 Proceso completado: {updated}/{total} imágenes actualizadas."
        ))
