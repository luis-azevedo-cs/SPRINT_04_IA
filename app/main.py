import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import gradio as gr
from src.rag.retriever import buscar_contexto
from src.rag.prompt_rag import gerar_resposta_rag

def responder_duvida(pergunta):
    if not pergunta.strip():
        return "Por favor, digite uma pergunta.", ""
    
    try:
        contexto, fontes = buscar_contexto(pergunta)
        resposta = gerar_resposta_rag(pergunta, contexto)
        
        str_fontes = "\n".join([f"- {f}" for f in fontes])
        return resposta, f"### Fontes Consultadas:\n{str_fontes}\n\n### Contexto Bruto:\n{contexto}"
    except Exception as e:
        return f"Erro ao processar a pergunta: {str(e)}", ""

with gr.Blocks(title="GoodWe EV Assistant - Sprint 04") as demo:
    gr.Markdown("# 🔌 EV Challenge - Assistente GoodWe & Energisa")
    gr.Markdown("Consulte dúvidas técnicas sobre os carregadores GoodWe HCA G2 e a norma NDU-042.")
    
    with gr.Row():
        with gr.Column():
            input_pergunta = gr.Textbox(lines=3, placeholder="Ex: Quais são os modelos da linha HCA G2?")
            btn_enviar = gr.Button("Perguntar", variant="primary")
        with gr.Column():
            output_resposta = gr.Markdown(label="Resposta")
            output_detalhes = gr.Accordion("Ver Fontes e Contexto Recuperado", open=False)
            with output_detalhes:
                output_fontes = gr.Markdown()

    btn_enviar.click(
        fn=responder_duvida,
        inputs=[input_pergunta],
        outputs=[output_resposta, output_fontes]
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, inbrowser=True)