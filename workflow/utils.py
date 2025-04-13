import json
from mutagen import File
import re

def clean_filename(file_name: str) -> str:
    """
    Cleans the filename while preserving important info like Remix or Mix names.
    """
    # 1. Remover contenido entre corchetes (suelen ser sellos, catálogos)
    file_name = re.sub(r'\[.*?\]', '', file_name)

    # 2. Reemplazar guiones bajos por espacios
    file_name = file_name.replace('_', ' ')

    # 3. Remover números de track al principio (e.g., "01.", "04 -", etc.)
    file_name = re.sub(r'^\s*\d+[a-zA-Z]?[\.\-\s]+', '', file_name)

    # 4. Normalizar espacios múltiples
    file_name = re.sub(r'\s+', ' ', file_name)

    # 5. Limpiar extremos
    file_name = file_name.strip()

    return file_name


def extract_metadata(file_path: str):
    """
    Extracts metadata (artist and title) from the audio file if available.
    """
    try:
        audio = File(file_path)
        artist = audio.get("artist", [None])[0]
        title = audio.get("title", [None])[0]
        
        return artist, title
    except Exception as e:
        print(f"Error extracting metadata for {file_path}: {e}")
        return None, None


def update_artist_database(state, artist, artist_db_file):
    """
    Updates the artist database by adding a new artist if it's not already present.
    """

    try:
        with open(artist_db_file, "r") as file:
            artist_database = json.load(file)
    except FileNotFoundError:
        artist_database = []

    if artist not in artist_database:
        artist_database.append(artist)

    with open(artist_db_file, "w") as file:
        json.dump(artist_database, file, indent=4)