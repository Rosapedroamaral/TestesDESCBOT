import requests
import logging
from source.modules.business_error import BusinessError

class ChatPDFAPI:
    """Escrita por Tiago Rodrigues de Souza - souzatiagojk@gmail.com"""
    def __init__(self,api_key,file_path=None,file_content=None):
        self.api_key = api_key
        self.base_url = 'https://api.chatpdf.com'
        self.aplication = 'application/octet-stream'
        self.file_id  = None
        self.headers = {'x-api-key': api_key}
        self.limite_chamadas = 3

        self.get_file_id(file_path,file_content)

    def get_file_id(self,file_path,file_content):
        try:
            if file_path!=None:
                files = [('file', ('file', open(file_path, 'rb'), self.aplication))]
            else:
                files={'file': file_content}
        except:
            raise BusinessError("Falha ao localizar arquivo")
        self.file_id = self.__request_file(url="/v1/sources/add-file",files=files)
        if self.file_id==None or self.file_id=="Falha na comunicação":
            raise BusinessError("Erro ao iniciar Chat - Falha na comunicação")
    
    def __request_file(self,url,files):
        rechamadas=0
        waiting_resposta=True
        try:
            while (rechamadas < self.limite_chamadas) and (waiting_resposta):
                response = requests.post(f'{self.base_url}{url}', headers=self.headers, files=files)
                if response.status_code == 200:
                    waiting_resposta=False
                    file_id = response.json().get('sourceId')
                    return file_id
                else:
                    rechamadas+=1
                    logging.error(f'Falha na {rechamadas} de {self.limite_chamadas} rechamadas')
        except Exception as erro:
            logging.error(f"ERRO na requisição - {erro}")
            logging.error(f"")

        return "Falha na comunicação"
    
    def __request(self,url,data):
        rechamadas=0
        waiting_resposta=True
        try:
            while (rechamadas < self.limite_chamadas) and (waiting_resposta):
                response = requests.post(f"{self.base_url}{url}", headers=self.headers, json=data)
                if response.status_code == 200:
                    waiting_resposta=False
                    resposta_IA = response.json().get('content')
                    return resposta_IA
                else:
                    rechamadas+=1
                    logging.error(f'Falha na {rechamadas} de {self.limite_chamadas} rechamadas')   
        except Exception as erro:
            logging.error(f"ERRO na requisição - {erro}")
            logging.error(f"")

        return "Falha na comunicação"

    def pergunta_pdf(self,pergunta):
        data=  {
                    "sourceId": self.file_id,
                    "messages": [
                        {
                            "role": "user",
                            "content": pergunta
                        }
                    ]
                }
        resposta = self.__request(url="/v1/chats/message",data=data)
        return resposta
    
    def pergunta_pdf_with_context(self,pergunta):
        data=  {
                    "sourceId": self.file_id,
                    "messages": pergunta
                }
        resposta = self.__request(url="/v1/chats/message",data=data)
        return resposta