import os
import random
import statistics
import requests
from dotenv import load_dotenv
import movie_storage_sql_API as movie_db  # Importiert Ihr SQL-Modul

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

if not OMDB_API_KEY:
    print("WARNING: OMDB_API_KEY not found in .env file! API features will not work.")



def get_valid_number(prompt, min_val, max_val, is_float=False):
    while True:
        try:
            value = float(input(prompt)) if is_float else int(input(prompt))
            if min_val <= value <= max_val:
                return value
            print(f"Please enter a value between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_optional_input(prompt, default_val, is_float=False):
    user_input = input(prompt).strip()
    if not user_input:
        return default_val
    try:
        return float(user_input) if is_float else int(user_input)
    except ValueError:
        print(f"Invalid format. Using default value: {default_val}")
        return default_val


def fetch_movie_from_api(title):
    if not OMDB_API_KEY:
        print("Error: Cannot search. API Key is missing. Check your .env file.")
        return None

    url = f"https://omdbapi.com/?apikey={OMDB_API_KEY}&t={title}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("Response") == "False":
            print(f"Error from API: {data.get('Error', 'Movie not found.')}")
            return None

        return data
    except requests.exceptions.RequestException as e:
        print(f"Network Error: Could not connect to OMDb API. Detail: {e}")
        return None


def wait_for_user():
    input("\nPress enter to continue...")



def list_movies():
    movies = movie_db.list_movies()
    if not movies:
        print("Your database is empty.")
        return
    print(f"\n{len(movies)} movies in total:")
    for movie, data in movies.items():
        print(f"- {movie} ({data['year']}) - Rating: {data['rating']}/10")
        #print(f"  Poster-URL: {data['poster']}")


def add_movie():
    title_input = input("Enter movie title to search and add: ").strip()
    if not title_input:
        print("Movie title cannot be empty.")
        return

    current_movies = movie_db.list_movies()
    if title_input.lower() in [t.lower() for t in current_movies.keys()]:
        print(f"Information: '{title_input}' already exists in your database.")
        return

    print("Searching on OMDb...")
    movie_data = fetch_movie_from_api(title_input)

    if movie_data:
        title = movie_data.get("Title")
        year_str = movie_data.get("Year", "0")[:4]
        year = int(year_str) if year_str.isdigit() else 0

        try:
            rating = float(movie_data.get("imdbRating", 0.0))
        except ValueError:
            rating = 0.0

        poster_url = movie_data.get("Poster", "N/A")

        print(f"\nFound: {title} ({year}) - IMDb: {rating}/10")
        movie_db.add_movie(title, year, rating, poster_url)


def delete_movie():
    name = input("Enter movie name to delete: ").strip()
    movie_db.delete_movie(name)


def update_movie():
    """Task 4: Aktualisiert die persönliche Notiz zu einem Film."""
    name = input("Enter movie name: ").strip()
    movies = movie_db.list_movies()

    if name in movies:
        movie_note = input("Enter movie note: ").strip()
        movie_db.update_movie(name, movie_note)
    else:
        print("Movie not found.")


def show_stats():
    movies = movie_db.list_movies()
    if not movies:
        print("No movies found to calculate stats.")
        return
    ratings = [film["rating"] for film in movies.values()]

    best_movie = max(movies, key=lambda k: movies[k]["rating"])
    worst_movie = min(movies, key=lambda k: movies[k]["rating"])

    print(f"Average rating: {statistics.mean(ratings):.2f}")
    print(f"Median rating:  {statistics.median(ratings):.2f}")
    print(f"Best movie:     {best_movie} ({movies[best_movie]['rating']}/10)")
    print(f"Worst movie:    {worst_movie} ({movies[worst_movie]['rating']}/10)")


def random_movie():
    movies = movie_db.list_movies()
    if not movies:
        print("No movies available.")
        return
    title = random.choice(list(movies.keys()))
    print(f"Your movie for tonight: {title}, it's rated {movies[title]['rating']}/10")


def search_movie():
    movies = movie_db.list_movies()
    query = input("Enter part of movie name: ").strip().lower()
    found = False
    for title, data in movies.items():
        if query in title.lower():
            print(f"- {title} ({data['year']}) - Rating: {data['rating']}/10")
            found = True
    if not found:
        print("No matching movies found.")


def sort_movies(by_key):
    """Task 8 & 9: Sortiert fehlerfrei nach 'rating' oder 'year'."""
    movies = movie_db.list_movies()
    if not movies:
        print("No movies to sort.")
        return

    # KORREKTUR: x[1][by_key] greift zuerst auf das Info-Dict an Index 1
    # des Tupels zu und holt dann den Wert für 'rating' oder 'year'
    sorted_list = sorted(movies.items(), key=lambda x: x[1][by_key], reverse=True)

    for title, data in sorted_list:
        print(f"- {title}: {data[by_key]}")


def generate_website():
    """Task 9: Generiert die Website und baut den Hover-Effekt (title-Attribut) ein."""
    movies = movie_db.list_movies()

    template_path = "_static/index_template.html"
    output_path = "index.html"

    try:
        with open(template_path, "r", encoding="utf-8") as file:
            template_content = file.read()
    except FileNotFoundError:
        print(f"Error: Template file '{template_path}' not found.")
        return

    # Das HTML-Film-Raster dynamisch zusammenbauen
    movie_grid_html = ""
    for title, data in movies.items():
        poster_src = data['poster'] if data['poster'] != "N/A" else "https://placeholder.com"

        # Holt die Notiz aus den Daten. Falls keine da ist, bleibt der Tooltip leer oder zeigt nichts an.
        note_text = data.get('note', '')

        movie_grid_html += "<li>\n"
        # KORREKTUR: title="{note_text}" sorgt für das kleine Hover-Fenster aus deinem Screenshot!
        movie_grid_html += f"    <div class=\"movie\" title=\"{note_text}\">\n"
        movie_grid_html += f"        <img class=\"movie-poster\" src=\"{poster_src}\" alt=\"{title} Poster\">\n"
        movie_grid_html += f"        <div class=\"movie-title\">{title}</div>\n"
        movie_grid_html += f"        <div class=\"movie-year\">{data['year']}</div>\n"
        movie_grid_html += "    </div>\n"
        movie_grid_html += "</li>\n"

    app_title = "My Movie App"
    updated_content = template_content.replace("__TEMPLATE_TITLE__", app_title)
    updated_content = updated_content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid_html)
    updated_content = updated_content.replace('href="style.css"', 'href="_static/style.css"')

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(updated_content)

    print("Website was generated successfully.")


def filter_movies():
    """Task 10: Filtert die Live-Daten mit optionalen Feldern."""
    movies = movie_db.list_movies()
    min_rate = get_optional_input("Enter minimum rating (0-10, leave blank for 0): ", 0.0, is_float=True)
    start_year = get_optional_input("Enter start year (leave blank for 1888): ", 1888)
    end_year = get_optional_input("Enter end year (leave blank for 2100): ", 2100)

    found = False
    for title, data in movies.items():
        if data["rating"] >= min_rate and start_year <= data["year"] <= end_year:
            print(f"- {title} ({data['year']}): {data['rating']}/10")
            found = True
    if not found:
        print("No movies match your filter criteria.")



def main():
    print("\n********** My Movies Database (SQLAlchemy + OMDb API) **********")

    while True:
        print("\nMenu:")
        print("0. Exit\n1. List movies\n2. Add movie (via API)\n3. Delete movie\n4. Update movie")
        print("5. Stats\n6. Random movie\n7. Search movie\n8. Movies sorted by rating")
        print("9. Generate website\n10. Filter movies")  # Neu strukturiertes Menü

        choice = get_valid_number("\nEnter choice (0-10): ", 0, 10)

        if choice == 0:
            print("Bye!")
            break
        elif choice == 1:
            list_movies()
        elif choice == 2:
            add_movie()
        elif choice == 3:
            delete_movie()
        elif choice == 4:
            update_movie()
        elif choice == 5:
            show_stats()
        elif choice == 6:
            random_movie()
        elif choice == 7:
            search_movie()
        elif choice == 8:
            sort_movies("rating")
        elif choice == 9:
            generate_website()
        elif choice == 10:
            filter_movies()

        wait_for_user()


if __name__ == "__main__":
    main()
