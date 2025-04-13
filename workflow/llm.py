from langchain_community.chat_models import ChatOllama

def get_llm():
    """
    Initialize and return the Ollama LLM model.
    """
    return ChatOllama(model="llama3.2")  # Make sure to confirm the model name with `ollama list`