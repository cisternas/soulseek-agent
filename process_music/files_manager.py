import os
import shutil
from typing import List, Dict
from mutagen import File
from mutagen.id3 import ID3, TIT2, TPE1
from mutagen.mp4 import MP4
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis

AUDIO_EXTENSIONS = [
    ".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg",
    ".aif", ".aiff", ".alac", ".wma", ".opus"
]

def has_metadata(file_path: str) -> bool:
    """Check if an audio file has any metadata."""
    try:
        audio = File(file_path)
        if audio is None:
            return False
            
        if file_path.lower().endswith('.mp3'):
            return bool(ID3(file_path))
        elif file_path.lower().endswith('.m4a'):
            return bool(audio.tags)
        elif file_path.lower().endswith('.flac'):
            return bool(audio.tags)
        elif file_path.lower().endswith('.ogg'):
            return bool(audio.tags)
        return False
    except:
        return False

def write_metadata(file_path: str, artist: str, title: str):
    """Write artist and title metadata to an audio file."""
    try:
        audio = File(file_path)
        if audio is None:
            return False

        if file_path.lower().endswith('.mp3'):
            try:
                audio = ID3(file_path)
            except:
                audio = ID3()
            audio.add(TIT2(encoding=3, text=title))
            audio.add(TPE1(encoding=3, text=artist))
            audio.save(file_path)
        elif file_path.lower().endswith('.m4a'):
            audio.tags['\xa9ART'] = artist
            audio.tags['\xa9nam'] = title
            audio.save()
        elif file_path.lower().endswith('.flac'):
            audio.tags['ARTIST'] = artist
            audio.tags['TITLE'] = title
            audio.save()
        elif file_path.lower().endswith('.ogg'):
            audio.tags['ARTIST'] = artist
            audio.tags['TITLE'] = title
            audio.save()
        return True
    except Exception as e:
        print(f"❌ Error writing metadata to {file_path}: {str(e)}")
        return False

def find_audio_files(folder: str) -> List[str]:
    audio_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in AUDIO_EXTENSIONS:
                audio_files.append(os.path.join(root, file))
            else:
                print(f"❌ Ignored: {file} (ext: {ext})")
    return audio_files

def copy_audio_files(processed_tracks: List[Dict], destination_folder: str):
    """
    Copy audio files with new names after processing and add metadata if needed.
    
    Each dict in processed_tracks should have:
    - 'original_path': full original file path
    - 'new_name': new name for the file (including extension)
    - 'final_artist': artist name
    - 'track_title': track title
    """
    for track in processed_tracks:
        original = track["original_path"]
        new_name = track["new_name"]
        destination_path = os.path.join(destination_folder, new_name)
        
        # Copy the file
        shutil.copy2(original, destination_path)
        
        # Check if we need to add metadata
        if not has_metadata(original):
            artist = track.get("final_artist")
            title = track.get("track_title")
            if artist and title:
                if write_metadata(destination_path, artist, title):
                    print(f"📝 Added metadata to {new_name}")
                else:
                    print(f"⚠️ Failed to add metadata to {new_name}")
