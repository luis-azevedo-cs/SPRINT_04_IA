import os
from langchain_ollama import ChatOllama

PROMPT_RAG_V1 = """
Você é um assistente virtual especializado em mobilidade elétrica e equipamentos GoodWe.
Sua tarefa é responder à pergunta do usuário utilizando EXCLUSIVAMENTE o contexto fornecido abaixo.

Regras Obrigatórias:
1. Responda apenas com base no contexto fornecido. Se a resposta não estiver explícita no contexto, diga claramente: "Desculpe, não encontrei essa informação na base de conhecimento fornecida."
2. Não invente especificações técnicas nem assuma dados não presentes no texto.
3. Sempre cite a fonte (Nome do arquivo e número da página) no final de cada afirmação ou da resposta.

Contexto Recuperado:
{contexto}

Pergunta do Usuário:
{pergunta}

Resposta:
"""

def gerar_resposta_rag(pergunta: str, contexto: str) -> str:
    """
    Gera a resposta utilizando o ChatOllama e o prompt RAG versionado.
    """
    prompt = PROMPT_RAG_V1.format(contexto=contexto, pergunta=pergunta)
    
    # Utilizando o modelo gemma configurado no Ollama ou na nuvem
    llm = ChatOllama(model="gemma3:4b", temperature=0.0)
    
    resposta = llm.invoke(prompt)
    return resposta.content
