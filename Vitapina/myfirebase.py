import requests
from datetime import datetime
from kivy.app import App

class MyFirebase():
    API_KEY = "AIzaSyC-Xb5RIUljluE8_KI2W5kxWLT_eXZRnpk"

    def criar_conta(self, email, senha, nome, sobrenome, telefone):
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.API_KEY}"

        info = {"email": email,
                "password": senha,
                "returnSecureToken": True}

        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()

        if requisicao.ok:
            refresh_token = requisicao_dic["refreshToken"]
            local_id = requisicao_dic["localId"]
            id_token = requisicao_dic["idToken"]

            meu_aplicativo = App.get_running_app()
            meu_aplicativo.local_id = local_id
            meu_aplicativo.id_token = id_token

            with open("refreshtoken.txt", "w") as arquivo:
                arquivo.write(refresh_token)

            req_id = requests.get("https://vitapinabd-default-rtdb.firebaseio.com/proximo_id.json")
            id_usuario = req_id.json()

            link = f"https://vitapinabd-default-rtdb.firebaseio.com/{local_id}.json"
            info_usuario = f'{{"ID": "{id_usuario}", "Nome": "{nome}", "Sobrenome": "{sobrenome}", "telefone": "{telefone}","E-mail": "{email}", "Data de Cadastro": "{datetime.now().strftime("%d/%m/%Y")}", "Refeicoes": "", "Data de Nascimento": "", "Sexo": ""}}'
            requisicao_usuario = requests.patch(link, data=info_usuario)

            proximo_id = int(id_usuario) + 1
            info_id = f'{{"proximo_id": "{proximo_id}"}}'
            requests.patch("https://vitapinabd-default-rtdb.firebaseio.com/.json", data=info_id)

            meu_aplicativo.carregar_infos_usuario()
            meu_aplicativo.mudar_tela("glicemiapage")

        else:
            mensagem_erro = requisicao_dic["error"]["message"]
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids["cadastropage"]
            pagina_login.ids["mensagem_erro"].text = mensagem_erro
            pagina_login.ids["mensagem_erro"].color = (1, 0, 0, 1)

    def fazer_login(self, email, senha):
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.API_KEY}"

        info = {"email": email,
                "password": senha,
                "returnSecureToken": True}

        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()

        if requisicao.ok:
            refresh_token = requisicao_dic["refreshToken"]
            local_id = requisicao_dic["localId"]
            id_token = requisicao_dic["idToken"]

            meu_aplicativo = App.get_running_app()
            meu_aplicativo.local_id = local_id
            meu_aplicativo.id_token = id_token

            with open("refreshtoken.txt", "w") as arquivo:
                arquivo.write(refresh_token)

            meu_aplicativo.carregar_infos_usuario()
            meu_aplicativo.mudar_tela("glicemiapage")

        else:
            mensagem_erro = requisicao_dic["error"]["message"]
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids["loginpage"]
            pagina_login.ids["mensagem_erro"].text = mensagem_erro
            pagina_login.ids["mensagem_erro"].color = (1, 0, 0, 1)

    def trocar_token(self, refresh_token):
        link = f"https://securetoken.googleapis.com/v1/token?key={self.API_KEY}"
        info = {"grant_type": "refresh_token", "refresh_token": refresh_token}

        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()
        local_id = requisicao_dic["user_id"]
        id_token = requisicao_dic["id_token"]

        return local_id, id_token

    def criar_refeicao(self, tipo, nome, calorias, carboidratos, proteinas, gorduras, quantidade, horario="", foto=""):
            link = f"https://vitapinabd-default-rtdb.firebaseio.com/{App.get_running_app().local_id}/Refeicoes/{datetime.now().strftime('%d-%m-%Y')}.json"
            info_usuario = f'{{"Tipo": "{tipo}", "Nome": "{nome}", "Calorias": "{calorias}", "Carboidratos": "{carboidratos}","Proteinas": "{proteinas}", "Gorduras": "{gorduras}", "Quantidade": "{quantidade}", "Horario": "{datetime.now().strftime("%H:%M")}"}}'
            requisicao = requests.post(link, data=info_usuario)

            if requisicao.ok:
                App.get_running_app().carregar_calorias()
                App.get_running_app().carregar_infos_usuario()
                App.get_running_app().mudar_tela("caloriaspage")

    def alterar_dados(self, nome, sobrenome, telefone, email, dia_nas, mes_nas, ano_nas, sexo, local_id):
        perfil = App.get_running_app().root.ids["perfilpage"]
        if not perfil.ids["nome"].disabled:
            link = f"https://vitapinabd-default-rtdb.firebaseio.com/{local_id}.json"
            info_usuario = f'{{"Nome": "{nome}", "Sobrenome": "{sobrenome}", "telefone": "{telefone}","E-mail": "{email}", "Data de Nascimento": "{dia_nas}/{mes_nas}/{ano_nas}", "Sexo": "{sexo}"}}'
            requisicao_usuario = requests.patch(link, data=info_usuario)
            App.get_running_app().carregar_infos_usuario()
        else:
            App.get_running_app().mudar_tela("loginpage")