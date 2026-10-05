from langchain_text_splitters import RecursiveCharacterTextSplitter

def dividir_documentos(documentos, chunk_size: int = 512, chunk_overlap: int = 50):
    """
    Divide os documentos em pedaços (chunks) utilizando RecursiveCharacterTextSplitter,
    mantendo uma percentagem de overlap para preservar o contexto.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", ","]
    )
    
    chunks = splitter.split_documents(documentos)
    print(f"Total de chunks gerados ({chunk_size=}): {len(chunks)}")
    return chunks
