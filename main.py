import os
import random
import json
import time
from datetime import datetime
from tqdm import tqdm
from workflow.workflow import create_workflow
from workflow.utils import update_artist_database
from process_music.files_manager import find_audio_files, copy_audio_files, has_metadata
from workflow.state import State
from config import SOURCE_FOLDER, ARTIST_DB_FILE

# Default number of examples
DEFAULT_EXAMPLES = 10

class ProcessingStats:
    def __init__(self):
        self.total_files = 0
        self.processed_files = 0
        self.successful_files = 0
        self.failed_files = 0
        self.files_with_metadata = 0
        self.files_without_metadata = 0
        self.start_time = time.time()
        self.errors = []

    def add_error(self, file_path, error):
        self.errors.append({
            "file": file_path,
            "error": str(error),
            "timestamp": datetime.now().isoformat()
        })

    def get_report(self):
        duration = time.time() - self.start_time
        return {
            "total_files": self.total_files,
            "processed_files": self.processed_files,
            "successful_files": self.successful_files,
            "failed_files": self.failed_files,
            "files_with_metadata": self.files_with_metadata,
            "files_without_metadata": self.files_without_metadata,
            "processing_time": f"{duration:.2f} seconds",
            "errors": self.errors
        }

def save_report(report, dest_folder):
    report_file = os.path.join(dest_folder, "processing_report.json")
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)

def print_summary(report):
    print("\n📊 Processing Summary:")
    print(f"Total files processed: {report['total_files']}")
    print(f"Successfully processed: {report['successful_files']}")
    print(f"Failed to process: {report['failed_files']}")
    print(f"Files with existing metadata: {report['files_with_metadata']}")
    print(f"Files without metadata: {report['files_without_metadata']}")
    print(f"Processing time: {report['processing_time']}")
    
    if report['errors']:
        print("\n⚠️ Errors encountered:")
        for error in report['errors']:
            print(f"- {error['file']}: {error['error']}")

# Load the artist database from file
def load_artist_database():
    if os.path.exists(ARTIST_DB_FILE):
        with open(ARTIST_DB_FILE, "r") as file:
            return json.load(file)
    return []

def get_number_of_examples():
    while True:
        try:
            num = input(f"\n🔢 Enter the number of examples to show (default: {DEFAULT_EXAMPLES}): ").strip()
            if not num:
                return DEFAULT_EXAMPLES
            num = int(num)
            if num < 1:
                print("❌ Number of examples must be at least 1.")
                continue
            return num
        except ValueError:
            print("❌ Please enter a valid number.")

if __name__ == "__main__":
    # Get the parent directory of the current working directory
    parent_dir = os.path.dirname(os.getcwd())
    
    # Ask for destination folder
    while True:
        dest_folder = input("\n📁 Enter the destination folder name (will be created in parent directory): ").strip()
        if not dest_folder:
            print("❌ Destination folder name cannot be empty. Please try again.")
            continue
        
        # Create full path by joining parent directory with the folder name
        full_dest_path = os.path.join(parent_dir, dest_folder)
        
        # Create destination folder
        try:
            os.makedirs(full_dest_path, exist_ok=True)
            break
        except Exception as e:
            print(f"❌ Error creating destination folder: {str(e)}")
            print("Please try again with a valid folder name.")

    # Get number of examples
    num_examples = get_number_of_examples()

    stats = ProcessingStats()
    artist_database = load_artist_database()
    workflow = create_workflow()

    print("\n🔍 Scanning source folder...\n")
    audio_files = find_audio_files(SOURCE_FOLDER)
    stats.total_files = len(audio_files)

    if stats.total_files == 0:
        print("⚠️ No audio files found.")
        exit()

    print(f"🎶 Found {stats.total_files} audio files.\n")

    # 🔎 Show examples using the agent
    print(f"🔎 Running agent on {num_examples} examples:\n")
    samples = random.sample(audio_files, min(num_examples, stats.total_files))
    for file_path in samples:
        extension = os.path.splitext(file_path)[1].lower()
        example_state: State = {
            "file_path": file_path,
            "file_extension": extension,
            "recognized_artist": None,
            "final_artist": None,
            "track_title": None,
            "success": False,
            "artist_database": artist_database
        }
        example_result = workflow.invoke(example_state)

        original = os.path.basename(file_path)
        if example_result["success"]:
            proposed = f"{example_result['final_artist']} - {example_result['track_title']}{extension}"
            print(f"🎧 {original}")
            print(f"📝 Clean Version → {example_result['clean_file_name']}")
            print(f"🧠 Proposed → {proposed}")
            
            # Check and display metadata information
            has_existing_metadata = has_metadata(file_path)
            if has_existing_metadata:
                print("📋 Existing metadata found - will be preserved")
            else:
                print("📋 No existing metadata - will add:")
                print(f"   Artist: {example_result['final_artist']}")
                print(f"   Title: {example_result['track_title']}")
            print()
        else:
            print(f"❌ {original} → Could not process.\n")

    proceed = input("Do you want to continue processing all files? (y/n): ").strip().lower()
    if proceed != "y":
        print("❌ Operation canceled.")
        exit()

    print("\n🚀 Processing files...\n")
    processed_tracks = []

    # Process files with progress bar
    for file_path in tqdm(audio_files, desc="Processing files"):
        try:
            extension = os.path.splitext(file_path)[1].lower()
            state: State = {
                "file_path": file_path,
                "file_extension": extension,
                "recognized_artist": None,
                "final_artist": None,
                "track_title": None,
                "success": False,
                "artist_database": artist_database
            }

            updated_state = workflow.invoke(state)
            stats.processed_files += 1

            original = os.path.basename(file_path)

            if updated_state["success"]:
                final_name = f"{updated_state['final_artist']} - {updated_state['track_title']}{extension}"
                print(f"✅ {original} → {final_name}")

                processed_tracks.append({
                    "original_path": file_path,
                    "new_name": final_name,
                    "final_artist": updated_state["final_artist"],
                    "track_title": updated_state["track_title"]
                })

                if updated_state["final_artist"] not in artist_database:
                    update_artist_database(state, updated_state["final_artist"], ARTIST_DB_FILE)
                    artist_database.append(updated_state["final_artist"])

                stats.successful_files += 1
                if has_metadata(file_path):
                    stats.files_with_metadata += 1
                else:
                    stats.files_without_metadata += 1
            else:
                print(f"❌ Could not process {original}")
                stats.failed_files += 1
                stats.add_error(file_path, "Processing failed")
        except Exception as e:
            stats.failed_files += 1
            stats.add_error(file_path, str(e))
            print(f"❌ Error processing {file_path}: {str(e)}")

    print("\n📂 Copying files to destination folder...\n")
    try:
        copy_audio_files(processed_tracks, full_dest_path)
        print("✅ Files copied successfully.")
    except Exception as e:
        print(f"❌ Error copying files: {str(e)}")
        stats.add_error("File copying", str(e))

    # Generate and save report
    report = stats.get_report()
    save_report(report, full_dest_path)
    print_summary(report)
    print(f"\n📄 Detailed report saved to: {os.path.join(full_dest_path, 'processing_report.json')}")
    print("✅ Done.")
