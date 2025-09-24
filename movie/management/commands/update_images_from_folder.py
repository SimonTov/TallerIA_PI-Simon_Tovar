import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from movie.models import Movie

class Command(BaseCommand):
    help = "Asigna imágenes desde media/movie/images a las películas en la BD"

    def handle(self, *args, **kwargs):
        folder = os.path.join(settings.MEDIA_ROOT, "movie", "images")
        if not os.path.isdir(folder):
            self.stdout.write(self.style.ERROR(f"No existe la carpeta: {folder}"))
            return

        exts = ['jpg', 'jpeg', 'png', 'webp', 'JPG', 'JPEG', 'PNG', 'WEBP']
        updated = 0

        for movie in Movie.objects.all():
            if movie.poster:  # Ya tiene poster asignado
                continue

            # generar posibles nombres de archivo
            candidates = [
                movie.title,
                movie.title.replace(" ", "_"),
                movie.title.replace(" ", "")
            ]
            safe = ''.join(c for c in movie.title if c.isalnum() or c in " -_").strip()
            if safe and safe not in candidates:
                candidates.append(safe)

            # buscar archivo
            found = None
            for name in candidates:
                for ext in exts:
                    filename = f"{name}.{ext}"
                    path = os.path.join(folder, filename)
                    if os.path.exists(path):
                        found = (filename, path)
                        break
                if found:
                    break

            if found:
                filename, path = found
                with open(path, "rb") as f:
                    movie.poster.save(filename, File(f), save=True)  # 👈 ahora usa `poster`
                updated += 1
                self.stdout.write(self.style.SUCCESS(f"Asignada imagen a: {movie.title}"))

        self.stdout.write(self.style.SUCCESS(f"Proceso terminado. {updated} imágenes asignadas."))
