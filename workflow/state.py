from typing import TypedDict, List, Optional

class State(TypedDict):
    # Stores the current file's path
    file_path: str
    # Stores the extracted or recognized artist
    recognized_artist: Optional[str]
    # Stores the final artist name after checking with the database or LLM
    final_artist: Optional[str]
    # Clean file name
    clean_file_name: Optional[str]
    # Stores the extracted track title
    track_title: Optional[str]
    # Stores the file extension
    file_extension: str
    # Flag indicating whether the process was successful
    success: bool
    # Stores the artist database as a list of known artists
    artist_database: List[str]
