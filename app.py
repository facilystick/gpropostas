import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# 1. Configuração da Página
st.set_page_config(page_title="Nós temos um Combinado!", page_icon="📝")

# 2. Interface Visual
st.markdown("""
<style>
    .stApp { background-color: #e0f7fa; }
    h1 { color: #00838f; font-family: 'Arial Black', sans-serif; margin-bottom: 0rem; }
    .desenvolvedora { color: #546e7a; font-size: 0.9rem; margin-top: -0.5rem; margin-bottom: 2rem; font-style: italic; }
    div.stButton > button:first-child {
        background-color: #ff6d00; color: white; border: none; border-radius: 8px;
        font-weight: bold; padding: 0.6rem 2rem; width: 100%;
    }
    div.stButton > button:first-child:hover { background-color: #e65100; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>Gerador de Proposta Comercial</h1>", unsafe_allow_html=True)
st.markdown("<p class='desenvolvedora'>by Facilizy Technologies Corporation</p>", unsafe_allow_html=True)

# 3. Formulário
with st.form("proposta_completa"):
    st.write("### 🛠️ Dados do Orçamento")
    logo = st.file_uploader("1. Selecione a Logo da Loja", type=["png", "jpg", "jpeg"])
    
    col1, col2 = st.columns(2)
    with col1:
        nome_cliente = st.text_input("2. Nome do Cliente")
    with col2:
        telefone_cliente = st.text_input("3. WhatsApp/Telefone")
    
    detalhes_produto = st.text_area("4. Descrição dos Produtos", height=100)
    
    col3, col4 = st.columns(2)
    with col3:
        valor_venda = st.text_input("5. Valor Total (R$)")
    with col4:
        vendedor_nome = st.text_input("6. Nome do Vendedor")
    
    submit_button = st.form_submit_button("GERAR PROPOSTA")

# 4. Geração da Imagem
if submit_button:
    largura_img = 1200
    img = Image.new('RGB', (largura_img, 1600), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # AJUSTE NA FUNÇÃO DE FONTE: Adicionando caminhos do Linux (Streamlit Cloud)
    def carregar_fonte(tamanho):
        fontes_tentar = [
            "verdana.ttf", 
            "Verdana.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", # Fonte padrão do Linux/Streamlit
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "Arial.ttf"
        ]
        for f in fontes_tentar:
            try:
                return ImageFont.truetype(f, tamanho)
            except:
                continue
        return ImageFont.load_default()

    fonte_principal = carregar_fonte(76)
    fonte_tit_info = carregar_fonte(45)
    fonte_corpo = carregar_fonte(35)
    fonte_valor = carregar_fonte(76)
    fonte_marca = carregar_fonte(25)

    # Cabeçalho
    draw.rectangle([0, 0, largura_img, 250], fill=(0, 131, 143))
    
    # --- LÓGICA DE CENTRALIZAÇÃO DO TÍTULO ---
    texto_titulo = "NÓS TEMOS UM COMBINADO!"
    bbox = draw.textbbox((0, 0), texto_titulo, font=fonte_principal)
    largura_texto = bbox[2] - bbox[0]
    x_centralizado = (largura_img - largura_texto) // 2
    
    # Desenha o Título Centralizado
    draw.text((x_centralizado, 90), texto_titulo, fill=(255, 255, 255), font=fonte_principal)
    
    # Marca Facilizy
    draw.text((750, 20), "Facilizy Technologies Corporation", fill=(200, 200, 200), font=fonte_marca)
    
    if logo:
        logotipo = Image.open(logo).convert("RGBA")
        logotipo.thumbnail((200, 200))
        img.paste(logotipo, (50, 25), logotipo)

    # Informações do Cliente
    y_pos = 350
    draw.text((50, y_pos), "DADOS DO CLIENTE:", fill=(0, 131, 143), font=fonte_tit_info)
    draw.text((50, y_pos + 70), f"CLIENTE: {nome_cliente.upper()}", fill=(0, 0, 0), font=fonte_corpo)
    draw.text((50, y_pos + 120), f"CONTATO: {telefone_cliente}", fill=(0, 0, 0), font=fonte_corpo)
    
    # Descrição (Aumentei um pouco o spacing para 15 para melhor leitura)
    draw.text((50, y_pos + 250), "PRODUTOS SELECIONADOS:", fill=(0, 131, 143), font=fonte_tit_info)
    draw.multiline_text((50, y_pos + 310), f"{detalhes_produto}", fill=(50, 50, 50), font=fonte_corpo, spacing=15)
    
    # Bloco de Valor (Destaque Laranja)
    draw.rectangle([50, 1050, 1150, 1300], fill=(255, 109, 0))
    
    texto_invest = "INVESTIMENTO TOTAL"
    bbox_inv = draw.textbbox((0, 0), texto_invest, font=fonte_corpo)
    x_inv = (largura_img - (bbox_inv[2] - bbox_inv[0])) // 2
    draw.text((x_inv, 1080), texto_invest, fill=(255, 255, 255), font=fonte_corpo)
    
    texto_rs = f"R$ {valor_venda}"
    bbox_rs = draw.textbbox((0, 0), texto_rs, font=fonte_valor)
    x_rs = (largura_img - (bbox_rs[2] - bbox_rs[0])) // 2
    draw.text((x_rs, 1150), texto_rs, fill=(255, 255, 255), font=fonte_valor)
    
    # Rodapé
    draw.text((50, 1450), f"Vendedor: {vendedor_nome}", fill=(0, 0, 0), font=fonte_corpo)

    # Exibição
    st.image(img)

    # Download
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    
    st.download_button(
        label="📥 BAIXAR PROPOSTA",
        data=img_buffer.getvalue(),
        file_name="Proposta_Facilizy.png",
        mime="image/png"
    )

st.markdown("<center><p style='color:gray;'>Facilizy Technologies Corporation</p></center>", unsafe_allow_html=True)