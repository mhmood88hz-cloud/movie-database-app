from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

DB_URL = "sqlite:///movies.db"
engine = create_engine(DB_URL, echo=False)

# DATENBANK-RESET: Löscht die alte Struktur ohne 'note'-Spalte einmalig beim Start
with engine.connect() as connection:
    #connection.execute(text("DROP TABLE IF EXISTS movies"))
    connection.commit()

    # Erstellt die Tabelle frisch mit allen benötigten Spalten
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster TEXT,
            note TEXT DEFAULT ''
        )
    """))
    connection.commit()


def list_movies():
    """Retrieve all movies from the database including notes."""
    with engine.connect() as connection:
        # NEU: note wird mit abgefragt
        result = connection.execute(text("SELECT title, year, rating, poster, note FROM movies"))
        movies = result.fetchall()

    # NEU: row[4] übergibt die Notiz an das Python-Dictionary
    return {row[0]: {"year": row[1], "rating": row[2], "poster": row[3], "note": row[4]} for row in movies}


def add_movie(title, year, rating, poster_url):
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text("""
                    INSERT INTO movies (title, year, rating, poster) 
                    VALUES (:title, :year, :rating, :poster)
                """),
                {"title": title, "year": year, "rating": rating, "poster": poster_url}
            )
            connection.commit()
            print(f"Success: Movie '{title}' added successfully to your database.")
            return True
        except IntegrityError:
            print(f"Information: '{title}' is already in your database.")
            return False


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        result = connection.execute(
            text("DELETE FROM movies WHERE title = :title"),
            {"title": title}
        )
        connection.commit()
        if result.rowcount > 0:
            print(f"Movie '{title}' successfully deleted.")
        else:
            print("Movie not found in database.")


def update_movie(title, note):
    """NEU: Aktualisiert die Notiz eines Films in der Datenbank."""
    with engine.connect() as connection:
        connection.execute(
            text("UPDATE movies SET note = :note WHERE title = :title"),
            {"title": title, "note": note}
        )
        connection.commit()
        print(f"Movie {title} successfully updated")
