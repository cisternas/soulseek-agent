from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from workflow.state import State
from workflow.llm import get_llm
import os, yaml
from workflow.utils import extract_metadata, clean_filename

llm = get_llm()

def artist_recognition_node(state: State):
    """
    Recognize the artist from the file name based on the known artist database.
    """
    artist_database = state["artist_database"]
    file_name = state["file_path"].split("\\")[-1]
    artist_found = None

    for artist in artist_database:
        if artist.lower() in file_name.lower():
            artist_found = artist
            break
    
    if artist_found:
        state["recognized_artist"] = artist_found
        state["success"] = True
        return {"recognized_artist": artist_found, "success": True}
    else:
        state["recognized_artist"] = None
        state["success"] = False
        return {"recognized_artist": None, "success": False}


def load_prompts():
    # Obtener la ruta del directorio actual del script
    current_dir = os.path.dirname(__file__)
    
    # Construir la ruta al archivo prompts.json en la carpeta 'workflow'
    prompts_file_path = os.path.join(current_dir, 'prompts.yml')
    
    # Cargar el archivo JSON con los prompts
    with open(prompts_file_path, 'r') as file:
        return yaml.safe_load(file)
    
# Cargar los prompts desde el archivo JSON
prompts = load_prompts()

# Obtener los prompts individuales
filename_prompt_text = prompts["filename_prompt"]["template"]
artist_filename_prompt_text = prompts["artist_filename_prompt"]["template"]

# Ahora puedes usar estos prompts en tu código, como en el ejemplo anterior
def extract_artist_and_title_node(state: State):
    """
    Extract the artist and track title from the file name using a language model.
    If a recognized artist is found, include it in the prompt to improve accuracy.
    """
    file_name = clean_filename(os.path.basename(state["file_path"]))
    suggested_artist = state.get("recognized_artist")

    metadata_artist, metadata_title = extract_metadata(state["file_path"])
    

    if suggested_artist:
        # Si se reconoció un artista, lo incluimos en el prompt
        prompt_text = artist_filename_prompt_text.format(file_name=file_name, suggested_artist=suggested_artist)

    else:
        # Prompt completo sin sugerencia
        prompt_text = filename_prompt_text.format(file_name=file_name)

    # Si hay metadata, añadimos al final del prompt
    if metadata_artist or metadata_title:
        metadata_block = "\nThe audio file also contains metadata that may help with extraction:"
        if metadata_artist:
            metadata_block += f"\nMetadata Artist: {metadata_artist}"
        if metadata_title:
            metadata_block += f"\nMetadata Title: {metadata_title}"
        prompt_text += metadata_block

    message = HumanMessage(content=prompt_text)
    response = llm.invoke([message]).content.strip()

    artist = suggested_artist if suggested_artist else None
    title = None

    for line in response.splitlines():
        if line.lower().startswith("artist:") and not suggested_artist:
            artist = line.split(":", 1)[1].strip()
        elif line.lower().startswith("track title:"):
            title = line.split(":", 1)[1].strip()

    return {
        "final_artist": artist,
        "track_title": title,
        "success": artist is not None and title is not None,
        "clean_file_name": file_name
    }