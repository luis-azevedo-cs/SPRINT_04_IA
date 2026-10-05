from src.rag.vector_store import criar_ou_carregar_vector_store

def buscar_contexto(pergunta: str, k: int = 4):
    """
    Realiza a busca por similaridade no ChromaDB e retorna os chunks mais relevantes
    juntamente com as citações das fontes.
    """
    vector_store = criar_ou_carregar_vector_store()
    documentos_recuperados = vector_store.similarity_search(pergunta, k=k)
    
    contexto_formatado = ""
    fontes = []

    for doc in documentos_recuperados:
        fonte_nome = doc.metadata.get("fonte", "Documento desconhecido")
        pagina = doc.metadata.get("page", 0) + 1  # Ajuste de índice base 0 para 1
        
        citacao = f"[{fonte_nome}, Pág. {pagina}]"
        fontes.append(citacao)
        contexto_formatado += f"\n--- Trecho {citacao} ---\n{doc.page_content}\n"
        
    return contexto_formatado, list(set(fontes))
