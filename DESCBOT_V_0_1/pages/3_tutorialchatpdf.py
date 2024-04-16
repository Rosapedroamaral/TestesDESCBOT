import streamlit as st
from PIL import Image

# Page title
st.set_page_config(page_title='Crie sua API key ', page_icon='🤖')
st.title('🤖 Como criar sua API key?')


img = Image.open("DESCBOT_V_0_1/pages/DESCBOT.jpg")
st.image(
    img,
    caption = "Olá!",
    width = 400,
    channels = "RGB"
)
st.write(
    '''
    Crie uma Conta no ChatPDF: Primeiro, acesse o site do ChatPDF e crie uma conta. Se você já tiver uma conta, faça login.
    Obtenha sua Chave de API:
    Após fazer login, vá para a seção “My Account” (Minha Conta).
    Expanda as configurações de desenvolvedor (Developer settings).
    Lá, você encontrará sua chave de API (API key).
    '''
)
st.link_button("Crie sua key agora mesmo", "https://www.chatpdf.com/")

