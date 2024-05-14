from source.modules.chat_pdf import ChatPDFAPI
import streamlit as st
from dataclasses import dataclass
# Page title
st.set_page_config(page_title='ChatBot UERJ', page_icon='🤖')
st.title('🤖 ChatBot UERJ')
st.sidebar.success("Select a page above.")

with st.expander('Sobre essa aplicação'):
  st.markdown('*O que essa aplicação pode fazer?*')
  st.info('Este projeto foi desenvolvido para facilitar a extração de informações e interações com documentos PDF por meio de uma interface de chat. Utilizando a biblioteca ChatPDF, é possível realizar operações como leitura de texto, busca por palavras-chave, marcação de trechos relevantes e muito mais, tudo de forma automatizada e intuitiva.')

  st.markdown('**Como usar a aplicação?**')
  st.warning('Para iniciar, basta inserir sua Key do framework ChatPDF e o Documento que deseja extrair informações. Depois disso, é só perguntar para o chat')

if "user_key" not in st.session_state:
    st.session_state["user_key"] = ""
  
st.subheader('Insira seu Documento e sua Key Para inicializar')
user_key = st.text_input('Digite sua key:',st.session_state["user_key"])

st.session_state["user_key"] = user_key


uploaded_file = st.file_uploader('Envie um documento PDF:', type=['pdf'])


USER = "user"
ASSISTANT = "assistant"
MESSAGES = "messages"
if (uploaded_file is not None) and (len(user_key)>0):
    if (MESSAGES not in st.session_state):
        file_contents = uploaded_file.read()
        chat1 = ChatPDFAPI(api_key=user_key,file_content=file_contents)
        st.session_state['CHAT']=chat1
        bemvindo="Olá !!! O que deseja saber sobre esse Documento?"
        st.session_state[MESSAGES] =  [{'role': ASSISTANT,'content':bemvindo}]

    for msg in st.session_state[MESSAGES]:
        st.chat_message(msg.get('role')).write(msg.get('content'))

    prompt: str = st.chat_input("Escreva sua dúvida aqui:")

    if prompt and uploaded_file is not None and len(user_key)>0:
        st.session_state[MESSAGES].append({'role': USER,'content':prompt})
        st.chat_message(USER).write(prompt)
        request=st.session_state[MESSAGES]
        if len(st.session_state[MESSAGES])>6:
            request= st.session_state[MESSAGES][-6:]
        resposta = st.session_state['CHAT'].pergunta_pdf_with_context(request)
        response = f"{resposta}"
        st.session_state[MESSAGES].append({'role': ASSISTANT,'content':resposta})
        st.chat_message(ASSISTANT).write(response)
