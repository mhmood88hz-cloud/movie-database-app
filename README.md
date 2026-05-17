# My Movie Database App

A professional, modular Python command-line application that allows users to manage their personal movie collection. The app connects to the **OMDb API** to fetch real-world movie details (including posters) and stores everything safely in a local **SQLite database** using **SQLAlchemy**.

## Features
- **Live API Integration**: Add movies simply by entering their title. Ratings, release years, and poster URLs are fetched automatically.
- **SQL Storage**: Fully persistent database storage using SQLAlchemy. No data loss on restart!
- **Duplication & Error Handling**: Fully protected against network drops, missing API data, or adding the same movie twice.
- **Statistics**: Instantly calculate average ratings, median values, and find the best/worst movies in your collection.
- **Website Generator**: Export your entire database into a beautiful, responsive HTML grid layout to view movie posters in your browser.

## Project Structure
- `movies_APP.py` (Main Application & Menu Control Flow)
- `movie_storage_sql_API.py` (Database Layer & SQL Queries)
- `_static/` (Folder containing `index_template.html` and `style.css`)
- `.env` (Secure file for configuration & API keys)
- `requirements.txt` (List of external Python modules)
- `.gitignore` (Files to be ignored by Git)

## Setup Instructions

1. **Clone or download** this project repository.
2. **Install dependencies** using pip:
   ```bash
   pip install -r requirements.txt
   ```
3. **Get a free OMDb API Key** from [omdbapi.com](https://omdbapi.com).
4. Create a `.env` file in the root directory and add your key:
   ```text
   OMDB_API_KEY=your_secret_key_here
   ```

## How to Use
Run the application from your terminal:
```bash
python movies_APP.py
```
Follow the interactive on-screen menu (Options 0-10) to manage your movies and select **Option 9** to generate your visual web showcase (`index.html`).
