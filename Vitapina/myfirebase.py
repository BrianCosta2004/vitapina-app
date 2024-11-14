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

    def cadastrar_receita(self, tipo, nome, calorias, carboidratos, proteinas, gorduras, horario="", foto=""):
        link = f"https://vitapinabd-default-rtdb.firebaseio.com/{App.get_running_app().local_id}/Refeicoes/{datetime.now().strftime('%d-%m-%Y')}.json"
        info_usuario = f'{{"Tipo": "{tipo}", "Nome": "{nome}", "Calorias": "{calorias}", "Carboidratos": "{carboidratos}","Proteinas": "{proteinas}", "Gorduras": "{gorduras}", "Horario": "{datetime.now().strftime("%H:%M")}"}}'
        requisicao = requests.post(link, data=info_usuario)

        if requisicao.ok:
            App.get_running_app().carregar_calorias()
            App.get_running_app().carregar_infos_usuario()
            App.get_running_app().mudar_tela("caloriaspage")

    def criar_refeicao(self, tipo, data, ingredientes, horario, foto=""):
        calorias = 0
        carboidratos = 0
        proteinas = 0
        gorduras = 0
        link_ingredientes = f"https://vitapinabd-default-rtdb.firebaseio.com/Alimentos.json"
        requisicao = requests.get(link_ingredientes)
        requisicao_dic = requisicao.json()
        for ingrediente, quantidade in ingredientes.items():
            for alimento in requisicao_dic:
                if isinstance(alimento, dict):
                    if ingrediente == alimento["Nome"]:
                        calorias += float(alimento["Calorias"]) * float(quantidade)
                        carboidratos += float(alimento["Carboidratos"]) * float(quantidade)
                        proteinas += float(alimento["Proteinas"]) * float(quantidade)
                        gorduras += float(alimento["Gorduras"]) * float(quantidade)


        link = f"https://vitapinabd-default-rtdb.firebaseio.com/{App.get_running_app().local_id}/Refeicoes/{data.replace("/", "-")}.json"
        info_refeicao = f'{{"Tipo": "{tipo}", "Nome": "Refeição", "Calorias": "{str("{:.2f}".format(calorias))}", "Carboidratos": "{str("{:.2f}".format(carboidratos))}","Proteinas": "{str("{:.2f}".format(proteinas))}", "Gorduras": "{str("{:.2f}".format(gorduras))}", "Quantidade": "{quantidade}", "Horario": "{horario}"}}'
        requisicao = requests.post(link, data=info_refeicao)

        if requisicao.ok:
            App.get_running_app().carregar_infos_usuario()
            App.get_running_app().carregar_calorias()
            App.get_running_app().mudar_tela("caloriaspage")

    def adicionar_ingrediente_refeicao(self, altura_grid, nome, quantidade):
        tela_refeicao = App.get_running_app().root.ids["refeicaopage"]
        lista_ingredientes = tela_refeicao.ids["lista_ingredientes"]

        ingrediente_layout = BoxLayout(size_hint_y=None, height="40dp")

        nome_label = Label(text=nome)
        quantidade_label = Label(text=quantidade)

        btn_remover = Button(text="Remover", size_hint_x=None, width="100dp")
        btn_remover.bind(on_press=lambda instance: self.remover_ingrediente_refeicao(instance))

        ingrediente_layout.add_widget(nome_label)
        ingrediente_layout.add_widget(quantidade_label)
        ingrediente_layout.add_widget(btn_remover)

        lista_ingredientes.add_widget(ingrediente_layout)

        self.ingredientes = {}
        self.ingredientes[nome] = quantidade

        altura_grid_nova = str(float(str(altura_grid).replace("dp", "")) + 40)
        tela_refeicao.ids["tela"].height = f"{altura_grid_nova}dp"

    def adicionar_ingrediente_receita(self, altura_grid, nome, quantidade):
        tela_addreceitas = App.get_running_app().root.ids["adicionarreceitaspage"]
        lista_ingredientes = tela_addreceitas.ids["lista_ingredientes"]

        ingrediente_layout = BoxLayout(size_hint_y=None, height="40dp")

        nome_label = Label(text=nome)
        quantidade_label = Label(text=quantidade)

        btn_remover = Button(text="Remover", size_hint_x=None, width="100dp")
        btn_remover.bind(on_press=lambda instance: self.remover_ingrediente_receita(instance))

        ingrediente_layout.add_widget(nome_label)
        ingrediente_layout.add_widget(quantidade_label)
        ingrediente_layout.add_widget(btn_remover)

        lista_ingredientes.add_widget(ingrediente_layout)

        self.ingredientes = {}
        self.ingredientes[nome] = quantidade

        altura_grid_nova = str(float(str(altura_grid).replace("dp", "")) + 40)
        tela_addreceitas.ids["tela"].height = f"{altura_grid_nova}dp"


    def remover_ingrediente_refeicao(self, button):
        layout = button.parent
        layout.parent.remove_widget(layout)
        tela_refeicao = App.get_running_app().root.ids["refeicaopage"]
        altura_grid =  tela_refeicao.ids["tela"].height
        altura_grid_nova = str(float(str(altura_grid).replace("dp", "")) - 40)
        tela_refeicao.ids["tela"].height = f"{altura_grid_nova}dp"


    def remover_ingrediente_receita(self, button):
        layout = button.parent
        layout.parent.remove_widget(layout)
        tela_addreceitas = App.get_running_app().root.ids["adicionarreceitaspage"]
        altura_grid = tela_addreceitas.ids["tela"].height
        altura_grid_nova = str(float(str(altura_grid).replace("dp", "")) - 40)
        tela_addreceitas.ids["tela"].height = f"{altura_grid_nova}dp"

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

    def infos_card(self, id_refeicao, data):
        pagina_detalhesrefeicao = App.get_running_app().root.ids["detalhesrefeicaopage"]
        requisicao = requests.get(f"https://vitapinabd-default-rtdb.firebaseio.com/{App.get_running_app().local_id}/Refeicoes/{data}/{id_refeicao}.json")
        requisicao_dic = requisicao.json()
        pagina_detalhesrefeicao.ids["calorias"].text = f"[color=#000000][b]Calorias: {requisicao_dic["Calorias"]}Kcal[/b][/color]"
        pagina_detalhesrefeicao.ids["carboidratos"].text = f"[color=#000000][b]{requisicao_dic["Carboidratos"]}[/b][/color]"
        pagina_detalhesrefeicao.ids["proteinas"].text = f"[color=#000000][b]{requisicao_dic["Proteinas"]}[/b][/color]"
        pagina_detalhesrefeicao.ids["gorduras"].text = f"[color=#000000][b]{requisicao_dic["Gorduras"]}[/b][/color]"
        App.get_running_app().mudar_tela("detalhesrefeicaopage")

    def criar_receita(self, tipo, ingredientes, usuario, modo, foto=""):
        calorias = 0
        carboidratos = 0
        proteinas = 0
        gorduras = 0
        link_ingredientes = f"https://vitapinabd-default-rtdb.firebaseio.com/Alimentos.json"
        requisicao = requests.get(link_ingredientes)
        requisicao_dic = requisicao.json()
        for ingrediente, quantidade in ingredientes.items():
            for alimento in requisicao_dic:
                if isinstance(alimento, dict):
                    if ingrediente == alimento["Nome"]:
                        calorias += float(alimento["Calorias"]) * float(quantidade)
                        carboidratos += float(alimento["Carboidratos"]) * float(quantidade)
                        proteinas += float(alimento["Proteinas"]) * float(quantidade)
                        gorduras += float(alimento["Gorduras"]) * float(quantidade)

        link_receitas = f"https://vitapinabd-default-rtdb.firebaseio.com/Receitas.json"
        info_receita = f'{{"Tipo": "{tipo}", "Nome": "Refeição", "Calorias": "{str(calorias)}", "Carboidratos": "{str(carboidratos)}","Proteinas": "{str(proteinas)}", "Gorduras": "{str(gorduras)}", "Usuario": "{usuario}", "Modo": "{modo}", "Foto": "receitas.png"}}'
        requisicao = requests.post(link_receitas, data=info_receita)
        App.get_running_app().carregar_infos_usuario()
        App.get_running_app().mudar_tela("receitaspage")

    def update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def pegar_opcoes(self, valor):
        self.todos_alimentos = []
        link_ingredientes = f"https://vitapinabd-default-rtdb.firebaseio.com/Alimentos.json"
        requisicao = requests.get(link_ingredientes)
        requisicao_dic = requisicao.json()
        for alimento in requisicao_dic:
            if isinstance(alimento, dict):
                self.todos_alimentos.append(alimento["Nome"])

        return self.todos_alimentos