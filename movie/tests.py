from django.test import TestCase
from .models import Movie

class MovieModelTest(TestCase):

    def test_create_movie(self):
        movie = Movie.objects.create(
            title="The Matrix",
            description="A computer hacker learns about the true nature of reality.",
            release_date="1999-03-31",
            director="Wachowskis",
            genre="Sci-Fi",
            rating=9.0
        )
        self.assertEqual(movie.title, "The Matrix")
        self.assertEqual(movie.rating, 9.0)
