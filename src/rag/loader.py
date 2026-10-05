import os
from langchain_community.document_loaders import PyMuPDFLoader

def carregar_documentos(diretorio_docs: str = "data/knowledge_base"):
    """
    Carrega todos os ficheiros PDF do diretório especificado mantendo os metadados
    (nome do arquivo e número de página) para posterior citação de fontes.
    """
    documentos = []
    if not os.path.exists(diretorio_docs):
        print(f"Aviso: O diretório '{diretorio_docs}' não existe.")
        return documentos

    for arquivo in os.listdir(diretorio_docs):
        if arquivo.endswith(".pdf"):
            caminho_completo = os.path.join(diretorio_docs, arquivo)
            print(f"Carregando: {arquivo}...")
            loader = PyMuPDFLoader(caminho_completo)
            docs = loader.load()
            
            # Adicionar metadados explícitos de origem
            for doc in docs:
                doc.metadata["fonte"] = arquivo
            
            documentos.extend(docs)
            
    print(f"Total de páginas carregadas: {len(documentos)}")
    return documentos
