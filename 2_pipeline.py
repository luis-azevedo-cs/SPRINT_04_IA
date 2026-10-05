from src.rag.loader import carregar_documentos
from src.rag.chunking import dividir_documentos
from src.rag.vector_store import criar_ou_carregar_vector_store

def executar_pipeline():
    print("--- PASSO 1: Carregando PDFs ---")
    docs = carregar_documentos()
    
    if not docs:
        print("Nenhum documento encontrado em data/knowledge_base/!")
        return

    print("\n--- PASSO 2: Dividindo em Chunks ---")
    chunks = dividir_documentos(docs, chunk_size=512, chunk_overlap=50)

    print("\n--- PASSO 3: Gerando ChromaDB ---")
    criar_ou_carregar_vector_store(chunks)
    print("\nPipeline concluído com sucesso!")

if __name__ == "__main__":
    executar_pipeline()
