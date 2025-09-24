import os
import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from movie.models import Movie


class Command(BaseCommand):
    help = "Create or update movie info in the database from a CSV file"

    def handle(self, *args, **kwargs):
        # 📥 Archivo CSV con las actualizaciones
        csv_file = 'updated_movie_descriptions.csv'

        if not os.path.exists(csv_file):
            self.stderr.write(f"CSV file '{csv_file}' not found.")
            return

        created_count = 0
        updated_count = 0

        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                title = row.get("Title")
                if not title:
                    continue

                # ✅ Crear o actualizar la película
                movie, created = Movie.objects.get_or_create(title=title)

                # Descripción
                if row.get("Updated Description"):
                    movie.description = row["Updated Description"]
                elif row.get("Description"):
                    movie.description = row["Description"]

                # Director
                if row.get("Director"):
                    movie.director = row["Director"]

                # Rating
                if row.get("Rating"):
                    try:
                        movie.rating = float(row["Rating"])
                    except ValueError:
                        pass

                # Release Date (convertir formato DD/MM/YYYY → YYYY-MM-DD)
                if row.get("Release Date"):
                    try:
                        movie.release_date = datetime.strptime(
                            row["Release Date"], "%d/%m/%Y"
                        ).date()
                    except ValueError:
                        self.stderr.write(
                            f"⚠️ Invalid date format for {title}: {row['Release Date']}"
                        )

                # Género
                if row.get("Genre"):
                    movie.genre = row["Genre"]

                movie.save()

                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f"Created: {title}"))
                else:
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f"Updated: {title}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"Finished processing movies. Created: {created_count}, Updated: {updated_count}"
            )
        )
