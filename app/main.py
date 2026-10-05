import sys
import os
import html

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import gradio as gr
from src.rag.retriever import buscar_contexto
from src.rag.prompt_rag import gerar_resposta_rag

try:
    from markdown_it import MarkdownIt
    _md = MarkdownIt("commonmark", {"html": False}).enable("table")
except Exception:  # fallback simples se markdown-it não estiver disponível
    _md = None

SAUDACAO = (
    "Olá! 👋 Sou a Norah, assistente inteligente da GoodWe.\n\n"
    "Como posso ajudar você hoje?"
)

PERGUNTAS_RAPIDAS = [
    "Carregar durante meu filme",
    "Isso prejudica minha bateria?",
    "Meu carregador suporta isso?",
    "Eu recebo por ceder energia?",
    "Preciso sair com urgência",
]

# ----------------------------------------------------------------- RAG ----
def responder_duvida(pergunta, ultima_pergunta=""):
    """Chama o RAG. Perguntas curtas/ambíguas ('Isso prejudica...?') usam a
    pergunta anterior como contexto apenas na BUSCA."""
    consulta = pergunta
    if ultima_pergunta and len(pergunta.split()) <= 6:
        consulta = f"{ultima_pergunta} {pergunta}"
    try:
        contexto, fontes = buscar_contexto(consulta)
        resposta = gerar_resposta_rag(pergunta, contexto)
        return resposta, list(dict.fromkeys(fontes))
    except Exception as e:
        return f"Erro ao processar a pergunta: {e}", []

# ------------------------------------------------------------ RENDER ------
def _texto_para_html(texto):
    if _md is not None:
        return _md.render(texto)
    return "<p>" + html.escape(texto).replace("\n", "<br>") + "</p>"


def _bolha_bot(msg):
    if msg.get("typing"):
        corpo = '<div class="typing"><span></span><span></span><span></span></div>'
    else:
        corpo = _texto_para_html(msg["text"])
        if msg.get("fontes"):
            itens = "".join(f"<li>{html.escape(str(f))}</li>" for f in msg["fontes"])
            corpo += f'<details class="fontes"><summary>Ver fontes consultadas</summary><ul>{itens}</ul></details>'
    return f"""
    <div class="msg bot">
      <div class="avatar">GW</div>
      <div class="msg-body">
        <div class="msg-meta"><b>GoodWe</b><span>agora</span></div>
        <div class="bubble">{corpo}</div>
      </div>
    </div>"""


def _bolha_user(msg):
    return f"""
    <div class="msg user">
      <div class="msg-body">
        <div class="msg-meta"><span>agora</span><b>Você</b></div>
        <div class="bubble">{html.escape(msg["text"]).replace(chr(10), "<br>")}</div>
      </div>
    </div>"""


def render_chat(msgs):
    partes = [(_bolha_bot(m) if m["role"] == "bot" else _bolha_user(m)) for m in msgs]
    return f'<div class="chat-scroll"><div class="chat-inner">{"".join(partes)}</div></div>'


def inicial():
    return [{"role": "bot", "text": SAUDACAO}]


def enviar(texto, msgs):
    texto = (texto or "").strip()
    if not texto:
        yield msgs, render_chat(msgs), ""
        return

    ultima = next((m["text"] for m in reversed(msgs) if m["role"] == "user"), "")

    msgs = msgs + [{"role": "user", "text": texto}]
    pensando = msgs + [{"role": "bot", "text": "", "typing": True}]
    yield msgs, render_chat(pensando), ""

    resposta, fontes = responder_duvida(texto, ultima)
    msgs = msgs + [{"role": "bot", "text": resposta, "fontes": fontes}]
    yield msgs, render_chat(msgs), ""

# --------------------------------------------------------------- CSS ------
CSS = """
:root{
  --gw-red:#e30613; --gw-red-dark:#c20511; --gw-red-soft:#fdecee;
  --ink:#1a1d21; --muted:#6b7280; --line:#e5e7eb; --bubble:#f6f8f7; --bg:#ffffff;
}
html,body,.gradio-container{background:#fff !important;}
.gradio-container{
  max-width:100% !important; padding:8px 12px !important;
  font-family:"Source Sans 3","Segoe UI",system-ui,-apple-system,Roboto,Arial,sans-serif !important;
}
footer{display:none !important;}
.gradio-container .block, .gradio-container .form{
  border:none !important; box-shadow:none !important; background:transparent !important; padding:0 !important;
}
#layout{gap:16px !important; align-items:stretch !important; flex-wrap:nowrap !important;}
@media (max-width:820px){ #layout{flex-wrap:wrap !important;} }

/* ---------- sidebar ---------- */
#sidebar{gap:14px !important; min-width:250px !important; max-width:290px;}
.card{background:#fff; border:1px solid var(--line); border-radius:18px;}
.brand{padding:22px 18px 18px; text-align:center;}
.logo{
  width:38px; height:38px; margin:0 auto 10px; border-radius:10px; background:var(--gw-red);
  color:#fff; font-weight:800; font-size:13px; display:flex; align-items:center; justify-content:center;
  letter-spacing:-.5px;
}
.brand h3{margin:0 0 6px; font-size:14px; font-weight:700; color:var(--ink);}
.brand p{margin:0 0 12px; font-size:9.5px; color:var(--muted);}
.pill{
  display:inline-flex; align-items:center; gap:5px; background:var(--gw-red-soft); color:var(--gw-red);
  font-size:9px; font-weight:700; padding:3px 9px; border-radius:999px;
}
.pill i{width:6px; height:6px; border-radius:50%; background:var(--gw-red); display:inline-block;}

#quick{padding:20px 14px 14px !important; border:1px solid var(--line) !important; border-radius:18px !important;
       background:#fff !important; gap:12px !important; flex-grow:1;}
.quick-title{font-size:8.5px; letter-spacing:.9px; color:#6b7280; font-weight:700; padding:0 8px 4px;}
.qbtn, .qbtn button{
  width:100%; background:#fff !important; color:#374151 !important; border:1px solid var(--line) !important;
  border-radius:10px !important; font-size:13px !important; font-weight:600 !important; padding:10px 8px !important;
  box-shadow:none !important; transition:all .15s;
}
.qbtn:hover, .qbtn button:hover{border-color:var(--gw-red) !important; color:var(--gw-red) !important; background:var(--gw-red-soft) !important;}

/* ---------- painel principal ---------- */
#main{
  border:1px solid var(--line) !important; border-radius:18px !important; background:#fff !important;
  gap:0 !important; padding:0 !important; min-height:calc(100vh - 40px); overflow:hidden;
}
.head{display:flex; align-items:center; justify-content:space-between; padding:22px 28px 14px; border-bottom:1px solid var(--line);}
.head h2{margin:0; font-size:15px; font-weight:700; color:var(--ink);}
.head small{display:block; margin-top:3px; font-size:9.5px; color:var(--muted);}
.badge{background:var(--gw-red-soft); color:var(--gw-red); font-size:8px; font-weight:800; padding:4px 10px; border-radius:8px; letter-spacing:.3px;}

.chat-scroll{
  height:calc(100vh - 250px); min-height:320px; overflow-y:auto; padding:0 34px;
  display:flex; flex-direction:column-reverse; /* mantém a última mensagem visível */
}
.chat-inner{padding:34px 0 16px; display:flex; flex-direction:column; gap:18px;}
.msg{display:flex; gap:10px; align-items:flex-start; max-width:78%;}
.msg.user{align-self:flex-end; flex-direction:row-reverse;}
.avatar{
  flex:none; width:32px; height:32px; border-radius:50%; background:var(--gw-red); color:#fff;
  font-size:10px; font-weight:800; display:flex; align-items:center; justify-content:center;
}
.msg-meta{display:flex; gap:7px; align-items:baseline; font-size:10px; margin-bottom:3px; color:var(--ink);}
.msg-meta span{color:#9ca3af; font-size:9.5px;}
.msg.user .msg-meta{justify-content:flex-end;}
.bubble{
  background:var(--bubble); border:1px solid var(--line); border-radius:10px 14px 14px 14px;
  padding:11px 16px; font-size:12px; line-height:1.55; color:#2b2f33;
}
.bubble p{margin:0 0 8px;} .bubble p:last-child{margin-bottom:0;}
.bubble ul,.bubble ol{margin:4px 0 8px 18px; padding:0;}
.bubble table{border-collapse:collapse; font-size:11px; margin:6px 0;}
.bubble th,.bubble td{border:1px solid var(--line); padding:4px 8px;}
.msg.user .bubble{background:var(--gw-red); border-color:var(--gw-red); color:#fff; border-radius:14px 10px 14px 14px;}
.fontes{margin-top:10px; font-size:10.5px; color:var(--muted);}
.fontes summary{cursor:pointer; color:var(--gw-red); font-weight:600;}
.typing{display:flex; gap:4px; padding:4px 0;}
.typing span{width:6px; height:6px; border-radius:50%; background:#9ca3af; animation:b 1.2s infinite;}
.typing span:nth-child(2){animation-delay:.15s;} .typing span:nth-child(3){animation-delay:.3s;}
@keyframes b{0%,60%,100%{transform:translateY(0);opacity:.5}30%{transform:translateY(-4px);opacity:1}}

/* ---------- entrada ---------- */
#inputbar{
  border-top:1px solid var(--line) !important; padding:16px 16px 6px !important; gap:10px !important;
  align-items:center !important; flex-wrap:nowrap !important; background:#fff !important;
}
#txt textarea, #txt input{
  border:1px solid #d1d5db !important; border-radius:999px !important; padding:14px 22px !important;
  font-size:13px !important; background:#fff !important; box-shadow:none !important; resize:none;
}
#txt textarea:focus, #txt input:focus{border-color:var(--gw-red) !important;}
#send, #send button{
  min-width:40px !important; width:40px; height:40px; padding:0 !important; border-radius:10px !important;
  background:var(--gw-red) !important; color:#fff !important; border:none !important; font-size:16px !important;
  box-shadow:none !important; flex:none !important;
}
#send:hover, #send button:hover{background:var(--gw-red-dark) !important;}
.disclaimer{text-align:center; font-size:7.5px; color:#9ca3af; padding:6px 0 14px;}

/* ---------- força cores (evita texto branco no tema escuro do Gradio) ---------- */
.head h2,.brand h3,.msg-meta,.msg-meta b{color:#1a1d21 !important;}
.head small,.brand p{color:#6b7280 !important;}
.pill{color:#e30613 !important; background:#fdecee !important;}
.badge{color:#e30613 !important; background:#fdecee !important;}
.logo,.avatar{color:#fff !important;}
.msg-meta span{color:#9ca3af !important;}
.bubble,.bubble p,.bubble li,.bubble td,.bubble th{color:#2b2f33 !important;}
.bubble{background:#f6f8f7 !important;}
.msg.user .bubble,.msg.user .bubble p{background:#e30613 !important; color:#fff !important;}
.quick-title{color:#6b7280 !important;}
.disclaimer{color:#9ca3af !important;}
.fontes,.fontes li{color:#6b7280 !important;}
.fontes summary{color:#e30613 !important;}
#txt textarea,#txt input{color:#1a1d21 !important; background:#fff !important;}
#txt textarea::placeholder,#txt input::placeholder{color:#9ca3af !important;}
.card,.head,#main,#inputbar,#quick{background:#fff !important;}
.chat-inner{margin-bottom:auto;}  /* mensagens começam no topo */
.chat-scroll{height:calc(100vh - 300px) !important;}
"""

# ------------------------------------------------------------ INTERFACE ---
SIDEBAR_BRAND = """
<div class="card brand">
  <div class="logo">GW</div>
  <h3>Assistente GoodWe</h3>
  <p>Seu assistente inteligente para carregamento de veículos elétricos.</p>
  <span class="pill"><i></i> IA online</span>
</div>"""

HEADER = """
<div class="head">
  <div><h2>Assistente de Energia</h2><small>Como posso ajudar com seu carregamento?</small></div>
  <span class="badge">GOODWE AI</span>
</div>"""

DISCLAIMER = """<div class="disclaimer">Assistente demonstrativo. Confirme funções, limites e condições comerciais nos documentos oficiais do produto.</div>"""

with gr.Blocks(title="Assistente GoodWe") as demo:
    gr.HTML(f"<style>{CSS}</style>")
    estado = gr.State(inicial())

    with gr.Row(elem_id="layout"):
        with gr.Column(scale=1, min_width=250, elem_id="sidebar"):
            gr.HTML(SIDEBAR_BRAND)
            with gr.Column(elem_id="quick"):
                gr.HTML('<div class="quick-title">PERGUNTAS RÁPIDAS</div>')
                botoes = [gr.Button(p, elem_classes="qbtn") for p in PERGUNTAS_RAPIDAS]

        with gr.Column(scale=4, elem_id="main"):
            gr.HTML(HEADER)
            chat = gr.HTML(render_chat(inicial()))
            with gr.Row(elem_id="inputbar"):
                txt = gr.Textbox(
                    placeholder="Digite sua pergunta sobre o carregador...",
                    show_label=False, container=False, lines=1, max_lines=1,
                    scale=20, elem_id="txt",
                )
                enviar_btn = gr.Button("➤", elem_id="send", scale=0, min_width=40)
            gr.HTML(DISCLAIMER)

    saidas = [estado, chat, txt]
    txt.submit(enviar, [txt, estado], saidas)
    enviar_btn.click(enviar, [txt, estado], saidas)
    def _fazer_handler(pergunta):
        def handler(msgs):
            yield from enviar(pergunta, msgs)
        return handler

    for b, p in zip(botoes, PERGUNTAS_RAPIDAS):
        b.click(_fazer_handler(p), [estado], saidas)

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, inbrowser=True)
