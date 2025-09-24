from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Movie

import matplotlib
import matplotlib.pyplot as plt
import io
import base64

# ======================
# Páginas principales
# ======================

def home(request):
    searchTerm = request.GET.get('searchMovie')  # Parámetro de búsqueda
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})


def about(request):
    return render(request, 'about.html')


def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})


# ======================
# Listado y detalle de películas
# ======================

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movie/movie_list.html', {'movies': movies})


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'movie/movie_detail.html', {'movie': movie})


# ======================
# Vistas estadísticas
# ======================

def statistics_view(request):
    matplotlib.use('Agg')
    all_movies = Movie.objects.all()

    # Gráfica: películas por año
    movie_counts_by_year = {}
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        movie_counts_by_year[year] = movie_counts_by_year.get(year, 0) + 1
    year_graphic = generate_bar_chart(movie_counts_by_year, 'Year', 'Number of movies')

    # Gráfica: películas por género
    movie_counts_by_genre = {}
    for movie in all_movies:
        genre = movie.genre.split(',')[0].strip() if movie.genre else "None"
        movie_counts_by_genre[genre] = movie_counts_by_genre.get(genre, 0) + 1
    genre_graphic = generate_bar_chart(movie_counts_by_genre, 'Genre', 'Number of movies')

    return render(request, 'statistics.html', {
        'year_graphic': year_graphic,
        'genre_graphic': genre_graphic
    })


# ======================
# Función auxiliar para gráficos
# ======================

def generate_bar_chart(data, xlabel, ylabel):
    keys = [str(key) for key in data.keys()]
    plt.bar(keys, data.values())
    plt.title('Movies Distribution')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=90)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')
    return graphic
