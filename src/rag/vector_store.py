import os
from langchain_chroma import Chroma
from src.rag.embeddings import obter_modelo_embeddings

CAMINHO_CHROMA = "chroma_db"

def criar_ou_carregar_vector_store(chunks=None):
    """
    Cria uma nova base vetorial no ChromaDB com os chunks fornecidos
    ou carrega a base existente se chunks for None.
    """
    embeddings = obter_modelo_embeddings()
    
    if chunks:
        print("Gerando embeddings e criando banco vetorial ChromaDB...")
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=CAMINHO_CHROMA
        )
        print(f"Banco vetorial criado com sucesso em '{CAMINHO_CHROMA}'.")
        return vector_store
    else:
        if os.path.exists(CAMINHO_CHROMA):
            print("Carregando banco vetorial ChromaDB existente...")
            return Chroma(
                persist_directory=CAMINHO_CHROMA,
                embedding_function=embeddings
            )
        else:
            raise FileNotFoundError("Banco vetorial não encontrado. Passe os chunks para criar um novo.")
