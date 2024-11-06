import requests
from datetime import datetime
from kivy.app import App
from elementos import LabelButton
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock

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

    def criar_refeicao(self, tipo, quantidade, data, ingredientes, horario, foto=""):
        calorias = 0
        carboidratos = 0
        proteinas = 0
        gorduras = 0
        link_ingredientes = f"https://vitapinabd-default-rtdb.firebaseio.com/Alimentos.json"
        requisicao = requests.get(link_ingredientes)
        requisicao_dic = requisicao.json()
        for ingrediente in ingredientes:
            for alimento in requisicao_dic:
                if isinstance(alimento, dict):
                    if ingrediente["Nome"] == alimento["Nome"]:
                        calorias += float(alimento["Calorias"]) * float(ingrediente["Quantidade"])
                        carboidratos += float(alimento["Carboidratos"]) * float(ingrediente["Quantidade"])
                        proteinas += float(alimento["Proteinas"]) * float(ingrediente["Quantidade"])
                        gorduras += float(alimento["Gorduras"]) * float(ingrediente["Quantidade"])


        link = f"https://vitapinabd-default-rtdb.firebaseio.com/{App.get_running_app().local_id}/Refeicoes/{data}.json"
        info_refeicao = f'{{"Tipo": "{tipo}", "Nome": "Refeição", "Calorias": "{str(calorias)}", "Carboidratos": "{str(carboidratos)}","Proteinas": "{str(proteinas)}", "Gorduras": "{str(gorduras)}", "Quantidade": "{quantidade}", "Horario": "{horario}"}}'
        requisicao = requests.post(link, data=info_refeicao)

        if requisicao.ok:
            App.get_running_app().carregar_calorias()
            App.get_running_app().carregar_infos_usuario()
            App.get_running_app().mudar_tela("caloriaspage")

    def adicionar_ingrediente(self, nome, quantidade):
        tela_refeicao = App.get_running_app().root.ids["refeicaopage"]
        lista_ingredientes = tela_refeicao.ids["lista_ingredientes"]

        ingrediente_layout = BoxLayout(size_hint_y=None, height="40dp")

        nome_label = Label(text=nome)
        quantidade_label = Label(text=quantidade)

        btn_remover = Button(text="Remover", size_hint_x=None, width="100dp")
        btn_remover.bind(on_press=lambda instance: self.remover_ingrediente(instance))

        ingrediente_layout.add_widget(nome_label)
        ingrediente_layout.add_widget(quantidade_label)
        ingrediente_layout.add_widget(btn_remover)

        lista_ingredientes.add_widget(ingrediente_layout)


    def remover_ingrediente(self, button):
        layout = button.parent
        layout.parent.remove_widget(layout)

    def alterar_dados(self, nome, sobrenome, telefone, email, dia_nas, mes_nas, ano_nas, sexo, local_id):
        perfil = App.get_running_app().root.ids["perfilpage"]
        if not perfil.ids["nome"].disabled:
            link = f"https://vitapinabd-default-rtdb.firebaseio.com/{local_id}.json"
            info_usuario = f'{{"Nome": "{nome}", "Sobrenome": "{sobrenome}", "telefone": "{telefone}","E-mail": "{email}", "Data de Nascimento": "{dia_nas}/{mes_nas}/{ano_nas}", "Sexo": "{sexo}"}}'
            requisicao_usuario = requests.patch(link, data=info_usuario)

            popup_layout = GridLayout(cols=1, padding=[20, 20, 20, 20], spacing=[20, 20])

            with popup_layout.canvas.before:
                Color(0.8, 0.9, 1, 0)
                self.bg_rect = RoundedRectangle(pos=popup_layout.pos, size=popup_layout.size, radius=[20])
                popup_layout.bind(pos=self.update_bg, size=self.update_bg)

                lbl = LabelButton(
                    text="[b]Dados Alterados![/b]",
                    color=(0, 0, 0, 1),
                    size_hint=(0.8, 0.8),
                    markup=True
                )
                with lbl.canvas.before:
                    Color(0, 1, 0, 1)
                    self.bg_rect = RoundedRectangle(pos=lbl.pos, size=lbl.size, radius=[20])
                popup_layout.add_widget(lbl)

            self.popup_confirm = Popup(
                title='',
                content=popup_layout,
                size_hint=(0.9, 0.3),
                auto_dismiss=True,
                separator_height=0,
                background_color=(0, 0, 0, 0)
            )
            self.popup_confirm.open()

            App.get_running_app().carregar_infos_usuario()
        else:
            App.get_running_app().mudar_tela("loginpage")

    def update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size