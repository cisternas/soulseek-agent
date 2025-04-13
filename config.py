# Configuration file for the agent

import os

# Get the parent directory of the current working directory
PARENT_DIR = os.path.dirname(os.getcwd())

# Define paths for source and destination folders
SOURCE_FOLDER = os.path.join(PARENT_DIR, "complete")
ARTIST_DB_FILE = "data/artist_database.json"