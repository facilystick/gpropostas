import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# 1. Configuração da Página
st.set_page_config(page_title="Facilizy | Proposta Premium", page_icon="💼", layout="centered")

# 2. Interface Visual (Ajustada para Máximo Contraste)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    .stApp { background-color: #f0f2f6; }
    
    label, p, .stMarkdown { 
        color: #1a1a1a !important; 
        font-weight: 600 !important;
    }
    
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 12px !important;
        border: 2px solid #ff6d00 !important; /* Borda Laranja para combinar */
        background-color: white !important;
        color: #000000 !important;
    }
    
    h1 { 
        color: #ff6d00; 
        font-family: 'Inter', sans-serif; 
        font-weight: 800; 
        text-align: center;
        padding-top: 1rem;
    }
    
    .subtitle {
        text-align: center;
        color: #1a1a1a;
        margin-top: -10px;
        margin-bottom: 30px;
        font-size: 1.1rem;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #ff6d00 0%, #e65100 100%);
        color: #ffffff !important;
        border: none;
        padding: 18px 30px;
        border-radius: 15px;
        font-weight: 700;
        font-size: 1.2rem;
        width: 100%;
        box-shadow: 0 4px 15px rgba(255, 109, 0, 0.3);
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>Gerador de Proposta</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Facilizy Technologies Corporation • Premium Orange Edition</p>", unsafe_allow_html=True)

with st.container():
    with st.form("proposta_completa"):
        st.write("### ✍️ Preencha os Dados Abaixo")
        logo = st.file_uploader("Logo da Loja", type=["png", "jpg", "jpeg"])
        
        c1, c2 = st.columns(2)
        nome_cliente = c1.text_input("👤 NOME DO CLIENTE", placeholder="Digite o nome completo")
        telefone_cliente = c2.text_input("📱 WHATSAPP / CELULAR", placeholder="(00) 00000-0000")
        
        detalhes_produto = st.text_area("📦 DESCRIÇÃO DOS PRODUTOS", height=120, placeholder="Liste os produtos e detalhes aqui...")
        
        c3, c4 = st.columns(2)
        valor_venda = c3.text_input("💰 VALOR TOTAL", placeholder="R$ 0,00")
        vendedor_nome = c4.text_input("🖊️ ASSINADO POR", placeholder="Nome do vendedor")
        
        submit_button = st.form_submit_button("GERAR PROPOSTA PREMIUM")

if submit_button:
    W, H = 1200, 1600
    img = Image.new('RGB', (W, H), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    def get_font(size, bold=False):
        paths = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "verdana.ttf", "Arial.ttf"]
        for p in paths:
            try: return ImageFont.truetype(p, size)
            except: continue
        return ImageFont.load_default()

    f_header = get_font(68, bold=True)
    f_sub = get_font(34, bold=True)
    f_label = get_font(38, bold=True)
    f_text = get_font(36)
    f_price = get_font(95, bold=True)
    f_footer = get_font(28)

    # 1. Moldura Arredondada Externa
    padding = 30
    draw.rounded_rectangle([padding, padding, W-padding, H-padding], radius=45, outline=(240, 240, 240), width=4)

    # 2. CABEÇALHO LARANJA SOFISTICADO (A Grande Mudança)
    # Cor: #ff6d00 (Laranja vibrante premium)
    cor_laranja = (255, 109, 0)
    draw.rounded_rectangle([padding, padding, W-padding, 320], radius=45, fill=cor_laranja)
    # Ajuste para base reta do cabeçalho
    draw.rectangle([padding, 280, W-padding, 320], fill=cor_laranja)
    
    # Textos do Cabeçalho em BRANCO para contraste total
    draw.text((100, 100), "PROPOSTA COMERCIAL", fill=(255, 255, 255), font=f_header)
    draw.text((100, 195), "NÓS TEMOS UM COMBINADO!", fill=(255, 255, 255), font=f_sub)

    if logo:
        try:
            logotipo = Image.open(logo).convert("RGBA")
            logotipo.thumbnail((240, 240))
            # Colocando a logo no fundo laranja (garanta que a logo tenha fundo transparente)
            img.paste(logotipo, (W - 340, 50), logotipo)
        except:
            pass

    # 3. Conteúdo Principal
    margin_x = 120
    y = 450
    
    draw.text((margin_x, y), "PREPARADO PARA:", fill=(100, 100, 100), font=f_sub)
    draw.text((margin_x, y+55), nome_cliente.upper(), fill=(0, 0, 0), font=f_label)
    draw.text((margin_x, y+110), f"CONTATO: {telefone_cliente}", fill=(0, 0, 0), font=f_text)

    y += 280
    draw.line([margin_x, y, W-margin_x, y], fill=(220, 220, 220), width=4)
    
    y += 60
    draw.text((margin_x, y), "ITENS DO ACORDO:", fill=cor_laranja, font=f_label)
    draw.multiline_text((margin_x, y+85), detalhes_produto, fill=(0, 0, 0), font=f_text, spacing=25)

    # 4. CARD DE VALOR (Verde Petróleo Profundo)
    card_margin = 100
    card_y = 1180
    draw.rounded_rectangle([card_margin, card_y, W-card_margin, card_y+280], radius=55, fill=(0, 77, 64))
    
    txt_inv = "INVESTIMENTO TOTAL"
    bbox_inv = draw.textbbox((0, 0), txt_inv, font=f_sub)
    draw.text(((W-(bbox_inv[2]-bbox_inv[0]))//2, card_y+60), txt_inv, fill=(178, 223, 219), font=f_sub)
    
    txt_val = f"R$ {valor_venda}"
    bbox_val = draw.textbbox((0, 0), txt_val, font=f_price)
    draw.text(((W-(bbox_val[2]-bbox_val[0]))//2, card_y+135), txt_val, fill=(255, 255, 255), font=f_price)

    # 5. Rodapé
    draw.text((margin_x, 1510), f"🖊️ Autorizado por: {vendedor_nome}", fill=(0, 0, 0), font=f_text)
    draw.text((W-450, 1510), "FACILIZY TECHNOLOGIES", fill=cor_laranja, font=f_footer)

    st.image(img, use_container_width=True)
    
    buf = io.BytesIO()
    img.save(buf, format='PNG', optimize=True)
    
    st.download_button(
        label="📥 BAIXAR PROPOSTA PREMIUM (HD)",
        data=buf.getvalue(),
        file_name=f"Proposta_{nome_cliente}.png",
        mime="image/png"
    )

st.markdown("<br><center><p style='color:#000000; font-weight:bold;'>Facilizy Design System • 2026</p></center>", unsafe_allow_html=True)