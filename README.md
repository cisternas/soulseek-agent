# SoulSeek Agent

A Python-based music file organization tool that uses AI to process and organize music files. The agent can extract artist and track information from filenames, add metadata to audio files, and organize them in a structured way.

## Features

- 🔍 Automatic artist and track title extraction from filenames
- 📝 Metadata management for audio files
- 🎵 Support for multiple audio formats (MP3, FLAC, M4A, OGG, etc.)
- 📊 Progress tracking and detailed reporting
- 🎯 Smart file organization
- 🔄 Artist database for consistent naming

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

## Installation

1. Navigate to your SoulSeek download folder (where the "complete" folder is located):
```bash
cd /path/to/SoulSeek/download/folder
```

2. Clone the repository:
```bash
git clone git@github.com:cisternas/soulseek-agent.git
cd soulseek-agent
```

3. Create and activate a virtual environment (recommended):
```bash
python -m venv env
# On Windows
env\Scripts\activate
# On Unix or MacOS
source env/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
soulseek-agent/
├── code/
│   ├── main.py              # Main application entry point
│   ├── config.py            # Configuration settings
│   ├── requirements.txt     # Project dependencies
│   ├── workflow/            # Workflow and processing logic
│   │   ├── workflow.py
│   │   ├── nodes.py
│   │   ├── state.py
│   │   ├── prompts.yml
│   │   └── utils.py
│   └── process_music/       # Music file processing utilities
│       └── files_manager.py
├── complete/                # Source folder for audio files
└── (organized/)            # Destination folder (created during processing)
```

## Usage

1. Place your audio files in the `complete` folder in the parent directory.

2. Run the application:
```bash
python main.py
```

3. When prompted:
   - Enter the number of examples you want to see (default: 10)
   - Enter the name for the destination folder (it will be created in the parent directory)

4. The application will:
   - Show examples of how files will be processed
   - Ask for confirmation to proceed
   - Process all files
   - Create a detailed report

## Configuration

The application can be configured by modifying `config.py`:

- `SOURCE_FOLDER`: Path to the folder containing audio files
- `ARTIST_DB_FILE`: Path to the artist database file

## How It Works

1. **File Scanning**: The application scans the source folder for audio files.
2. **Example Processing**: Shows examples of how files will be processed.
3. **User Confirmation**: Asks for confirmation before processing all files.
4. **Processing**:
   - Extracts artist and track information
   - Checks for existing metadata
   - Updates metadata if needed
   - Organizes files in the destination folder
5. **Reporting**: Generates a detailed report of the processing.

## Output

The application creates:
- Organized files in the destination folder
- A JSON report file with processing statistics
- An artist database for consistent naming

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.