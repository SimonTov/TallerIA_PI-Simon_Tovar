from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Actualiza las descripciones de las películas sin usar API"

    def handle(self, *args, **kwargs):
        movies = Movie.objects.all()
        for movie in movies:
            nueva_desc = f"{movie.title} es una película destacada con una trama envolvente y gran dirección."
            movie.description = nueva_desc
            movie.save()
            self.stdout.write(self.style.SUCCESS(f"Descripción actualizada para: {movie.title}"))
