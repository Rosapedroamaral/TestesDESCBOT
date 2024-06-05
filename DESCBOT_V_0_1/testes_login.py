import os
import random
import string
from supabase import create_client, Client
from metricas import MetricasClient
from source.modules.chat_pdf import ChatPDFAPI
import streamlit as st

def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()

class SupabaseClient:
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key
        self.client = create_client(url, api_key)
        self.metricas_client = MetricasClient(self)

    def gera_id(self):
        while True:
            id = random.randint(1, 1000)
            n = self.client.table("Registros").select("ID").eq("ID", id).execute()
            if len(n.data) == 0:
                return id
          
    def gera_api_key(self):
        while True:
            api_key_length = random.randint(5, 20)
            characters = string.ascii_letters + string.digits
            api_key = ''.join(random.choice(characters) for _ in range(api_key_length))
            n = self.client.table("Registros").select("APIKey").eq("APIKey", api_key).execute()
            if len(n.data) == 0:
                return api_key

    def insere_dados(self, nome, email, senha, chat_pdf_api_key):
        try:
            result = self.client.table("Registros").select("ID").eq("Email", email).execute()
            if len(result.data) > 0:
                print("Email já cadastrado")
                return False
            
            id = self.gera_id()
           
            data = {
                "ID": id,
                "Nome": nome,
                "Email": email,
                "Senha": senha,
                "APIKey": chat_pdf_api_key
            }
            insert_response = self.client.table("Registros").insert(data).execute()
            self.metricas_client.insere_id(id)
            print("Registro inserido com sucesso.")
            return True
        except Exception as e:
            print(f"Erro ao inserir os dados: {e}")
            return False

        # Inserir o ID na tabela Metricas
        self.metricas_client.insere_id(id)
    
        print("Registro inserido com sucesso.")
        return True


    def deleta_dados(self, email, senha):
        # Verificar se o email está cadastrado
        email_result = self.client.table("Registros").select("ID", "Senha").eq("Email", email).execute()
        if len(email_result.data) == 0:
            print("Email não cadastrado")
            return
        
        # Verificar se a senha corresponde ao ID do email
        record = email_result.data[0]
        if record["Senha"] != senha:
            print("senha incorreta")
            return
        
        # Deletar a linha se a senha corresponder
        record_id = record["ID"]
        self.client.table("Registros").delete().eq("ID", record_id).execute()

        # Deletar o ID na tabela Metricas
        self.metricas_client.deleta_id(record_id)

        print(f"Registro deletado com sucesso para o email {email}")

    def atualiza_dados(self, email, senha):
        # Verificar se o email está cadastrado e a senha está correta
        result = self.client.table("Registros").select("ID", "Nome", "Email", "Senha", "APIKey").eq("Email", email).execute()
        if len(result.data) == 0 or result.data[0]["Senha"] != senha:
            print("Email ou senha inválidos")
            return
        
        # Pedir novos dados ao usuário
        novo_nome = input("Insira o novo nome: ")
        novo_email = input("Insira o novo email: ")
        nova_senha = input("Insira a nova senha: ")
        novo_apikey = input("Insira seu APIKey: ")
        
        # Atualizar o registro mantendo o mesmo ID e APIKey
        record = result.data[0]
        data = {
            "Nome": novo_nome,
            "Email": novo_email,
            "Senha": nova_senha,
            "APIKey": novo_apikey
        }
        self.client.table("Registros").update(data).eq("ID", record["ID"]).execute()

        # Atualizar a tabela Metricas
        self.metricas_client.atualizar_alteracoes(record["ID"])

        print("Dados atualizados com sucesso.")

    def autentica_dados(self, email, senha):
        # Verificar se o email está cadastrado
        result = self.client.table("Registros").select("ID", "Senha", "APIKey").eq("Email", email).execute()
        if len(result.data) == 0:
            print("Usuário não cadastrado")
            return False, None
        
        # Verificar se a senha corresponde ao email
        record = result.data[0]
        if record["Senha"] != senha:
            print("Senha inválida")
            return False, None
        
        # Atualizar a tabela Metricas
        self.metricas_client.atualizar_acessos(record["ID"])
    
        print("Acesso liberado")
        return True, record["APIKey"]



def menu_principal():
    supabase_client = SupabaseClient(url, key)
    while True:
        print("1. Inserir novo registro")
        print("2. Atualizar registro")
        print("3. Deletar registro")
        print("4. Autenticar registro")
        print("5. Sair")
        
        opcao = input("Escolha uma opção: ")

        print("-"*40)
        
        if opcao == "1":
            nome = input("Insira o nome: ")
            email = input("Insira o email: ")
            senha = input("Insira a senha: ")

            supabase_client.insere_dados(nome, email, senha)

        elif opcao == "2":
            email = input("Insira o email: ")
            senha = input("Insira a senha: ")

            supabase_client.atualiza_dados(email, senha)
                    
        elif opcao == "3":
            email = input("Digite seu email: ")
            senha = input("Digite sua senha: ")
            
            supabase_client.deleta_dados(email, senha)

        elif opcao == "4":
            email = input("Digite seu email: ")
            senha = input("Digite sua senha: ")
            
            supabase_client.autentica_dados(email, senha)

        elif opcao == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Defina supabase_client no escopo global
supabase_client = SupabaseClient(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])


def login():
    # Verifica se o usuário já está autenticado
    if 'autenticado' in st.session_state and st.session_state['autenticado']:
        return True
    
    with st.form(key='user_form'):
        email = st.text_input("Digite seu email: ")
        senha = st.text_input("Digite sua senha: ", type="password")
        
        # Botão para autenticar usuário
        submit_button = st.form_submit_button('Autenticar')
        if submit_button:
            success, _ = supabase_client.autentica_dados(email, senha)
            if success:
                st.success("Login bem-sucedido!")
                st.session_state['autenticado'] = True  # Define a sessão como autenticada
                return True
            else:
                st.error("Email ou senha inválidos")
                return False
    # Movendo a criação de novo usuário para fora do formulário de login
    with st.form(key='new_user_form'):
        create_user_button = st.form_submit_button('Criar novo usuário')
        if create_user_button:
            nome = st.text_input("Digite seu nome para registro: ", key='nome_registro')
            email_registro = st.text_input("Digite seu email para registro: ", key='email_registro')
            senha_registro = st.text_input("Digite sua senha para registro: ", type="password", key='senha_registro')
            user_api_key = st.text_input("Digite sua chave API para registro: ", key='user_api_key')
            
            if nome and email_registro and senha_registro and user_api_key:
                result = supabase_client.insere_dados(nome, email_registro, senha_registro, user_api_key)
                if result:
                    st.success("Usuário criado com sucesso! Por favor, autentique-se.")
                else:
                    st.error("E-mail já cadastrado")
            else:
                st.warning("Por favor, preencha todos os campos para registro.")






# Page title
st.set_page_config(page_title='ChatBot UERJ', page_icon='🤖')
st.title('🤖 ChatBot UERJ')

if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False  # Inicializa a sessão como não autenticada
if login():
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
