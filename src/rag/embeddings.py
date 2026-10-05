from langchain_ollama import OllamaEmbeddings

def obter_modelo_embeddings():
    """
    Retorna o modelo de embeddings nomic-embed-text via Ollama local.
    """
    return OllamaEmbeddings(
        model="nomic-embed-text",
        base_url="http://localhost:11434"
    )
