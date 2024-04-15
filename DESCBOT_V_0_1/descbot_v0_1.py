from source.modules.chat_pdf import ChatPDFAPI
import streamlit as st
from dataclasses import dataclass
from streamlit_option_menu import option_menu
from PIL import Image
import cv2


with st.sidebar:
  selected = option_menu(
      menu_title=None,
      options = ["ChatBot UERJ", "Crie sua API key", "Sobre os criadores"]
  )


if selected == "ChatBot UERJ": #Homepage
  # Page title
  st.set_page_config(page_title='ChatBot UERJ', page_icon='🤖')
  st.title('🤖 ChatBot UERJ')


  with st.expander('Sobre essa aplicação'):
    st.markdown('*O que essa aplicação pode fazer?*')
    st.info('Este projeto foi desenvolvido para facilitar a extração de informações e interações com documentos PDF por meio de uma interface de chat. Utilizando a biblioteca ChatPDF, é possível realizar operações como leitura de texto, busca por palavras-chave, marcação de trechos relevantes e muito mais, tudo de forma automatizada e intuitiva.')


    st.markdown('**Como usar a aplicação?**')
    st.warning('Para iniciar, basta inserir sua Key do framework ChatPDF e o Documento que deseja extrair informações. Depois disso, é só perguntar para o chat')




  st.subheader('Insira seu Documento e sua Key Para inicializar')
  user_key = st.text_input('Digite sua key:', key='chave')
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
if selected == "Crie sua API key":
  # Page title
  st.set_page_config(page_title='Crie sua API key ', page_icon='🤖')
  st.title('🤖 Como criar sua API key?')


  img = Image.open("descbot.jpg")
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


if selected == "Sobre os criadores":
  st.write(
      '''
      Somos alunos da Universidade do Estado do Rio de Janeiro (UERJ). E desenvolvemos esse chatbot para aa disciplina Projetos de Ambiente Computacional
      '''
  )