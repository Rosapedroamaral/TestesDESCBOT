from supabase import create_client

class MetricasClient:
    def __init__(self, supabase_client):
        self.supabase_client = supabase_client

    def insere_id(self, user_id):
        data = {"ID": user_id, "Acessos": 0, "Alteracoes": 0}
        self.supabase_client.client.table("Metricas").insert(data).execute()

    def atualizar_acessos(self, user_id):
        # Obter o valor atual de "Acessos" para o usuário com o ID fornecido
        response = self.supabase_client.client.table("Metricas").select("Acessos").eq("ID", user_id).execute()
        acessos_atuais = response.data[0]["Acessos"] if response.data else 0

        # Atualizar o registro incrementando "Acessos"
        data = {"ID": user_id, "Acessos": acessos_atuais + 1}
        response = self.supabase_client.client.table("Metricas").upsert(data).execute()
        return response


    def atualizar_alteracoes(self, user_id):
        # Obter o valor atual de "Alteracoes" e "Acessos" para o usuário com o ID fornecido
        response = self.supabase_client.client.table("Metricas").select("Alteracoes", "Acessos").eq("ID", user_id).execute()
        alteracoes_atuais = response.data[0]["Alteracoes"] if response.data else 0
        acessos_atuais = response.data[0]["Acessos"] if response.data else 0

        # Atualizar o registro incrementando "Alteracoes"
        data = {"ID": user_id, "Acessos": acessos_atuais + 1, "Alteracoes": alteracoes_atuais + 1}
        response = self.supabase_client.client.table("Metricas").upsert(data).execute()
        return response

    def deleta_id(self, user_id):
        self.supabase_client.client.table("Metricas").delete().eq("ID", user_id).execute()
