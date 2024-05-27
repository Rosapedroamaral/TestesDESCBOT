import os
import random
import string
from supabase import create_client, Client
from dotenv import load_dotenv
from metricas import MetricasClient

load_dotenv('creds.env')

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

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

    def insere_dados(self, nome, email, senha):
        # Verificar se o email já está cadastrado
        result = self.client.table("Registros").select("ID").eq("Email", email).execute()
        if len(result.data) > 0:
            print("Email já cadastrado")
            return
        
        # Gerar um novo ID e APIKey únicos
        id = self.gera_id()
        api_key = self.gera_api_key()

        data = {"ID": id, "Nome": nome, "Email": email, "Senha": senha, "APIKey": api_key}
        self.client.table("Registros").insert(data).execute()

        # Inserir o ID na tabela Metricas
        self.metricas_client.insere_id(id)

        print("Registro inserido com sucesso.")

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
        result = self.client.table("Registros").select("ID", "Senha").eq("Email", email).execute()
        if len(result.data) == 0:
            print("Usuário não cadastrado")
            return False
        
        # Verificar se a senha corresponde ao email
        record = result.data[0]
        if record["Senha"] != senha:
            print("Senha inválida")
            return False
        
        # Atualizar a tabela Metricas
        self.metricas_client.atualizar_acessos(record["ID"])

        print("Acesso liberado")
        return True

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

menu_principal()
