from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

from Vitapina.cardreceita import CardReceita
from telas import *
from elementos import *
import requests
import os
from functools import partial
from myfirebase import MyFirebase
from datetime import datetime
from kivy.core.window import Window
from bannerrefeicao import BannerRefeicao

GUI = Builder.load_file("main.kv")
Window.size = (450, 600)

class MainApp(App):

    def build(self):
        self.firebase = MyFirebase()
        return GUI

    def on_start(self):

        arquivos = os.listdir("icones/fotos_alimentos_cafe")
        pagina_receitas = self.root.ids["receitaspage"]
        lista_produtos = pagina_receitas.ids["lista_alimentos_cafe"]
        for foto_produto in arquivos:
            card = CardReceita(nome=foto_produto.replace(".png", ""), pasta="icones/fotos_alimentos_cafe/")
            lista_produtos.add_widget(card)

        arquivos = os.listdir("icones/fotos_alimentos_almoco")
        pagina_receitas = self.root.ids["receitaspage"]
        lista_produtos = pagina_receitas.ids["lista_alimentos_almoco"]
        for foto_produto in arquivos:
            card = CardReceita(nome=foto_produto.replace(".png", ""), pasta="icones/fotos_alimentos_almoco/")
            lista_produtos.add_widget(card)

        arquivos = os.listdir("icones/fotos_alimentos_lanche")
        pagina_receitas = self.root.ids["receitaspage"]
        lista_produtos = pagina_receitas.ids["lista_alimentos_lanche"]
        for foto_produto in arquivos:
            card = CardReceita(nome=foto_produto.replace(".png", ""), pasta="icones/fotos_alimentos_lanche/")
            lista_produtos.add_widget(card)

        arquivos = os.listdir("icones/fotos_alimentos_janta")
        pagina_receitas = self.root.ids["receitaspage"]
        lista_produtos = pagina_receitas.ids["lista_alimentos_janta"]
        for foto_produto in arquivos:
            card = CardReceita(nome=foto_produto.replace(".png", ""), pasta="icones/fotos_alimentos_janta/")
            lista_produtos.add_widget(card)

    def carregar_infos_usuario(self):
        try:
            self.carregar_calorias()
        except:
            pagina_calorias = self.root.ids["caloriaspage"]
            pagina_calorias.ids["calorias_consumidas"].text = "[color=#000000][size=32][b]0[/b][/size][/color]"
            pagina_calorias.ids["calorias_total"].text = "[color=#000000][size=32][b]1700[/b][/size][/color]"
            pagina_calorias.ids["calorias_restantes"].text = "[color=#000000][size=60][b]1700[/b][/size][/color]"
            pagina_calorias.ids["carboidratos"].text = "[color=#000000][b]0g[/b][/color]"
            pagina_calorias.ids["proteinas"].text = "[color=#000000][b]0g[/b][/color]"
            pagina_calorias.ids["gorduras"].text = "[color=#000000][b]0g[/b][/color]"
        try:
            with open("refreshtoken.txt", "r") as arquivo:
                refresh_token = arquivo.read()
            local_id, id_token = self.firebase.trocar_token(refresh_token)
            self.local_id = local_id
            self.id_token = id_token


            requisicao = requests.get(f"https://vitapinabd-default-rtdb.firebaseio.com/{self.local_id}.json")
            requisicao_dic = requisicao.json()
            print(requisicao_dic)
            nome = requisicao_dic["Nome"]
            sobrenome = requisicao_dic["Sobrenome"]
            data = requisicao_dic["Data de Cadastro"]
            self.nome = nome
            self.sobrenome = sobrenome
            self.data = data
            pagina_perfil = self.root.ids["perfilpage"]
            pagina_perfil.ids["label_nome"].text = f"[size=25][b]{nome} {sobrenome}[/b][/size]"
            pagina_perfil.ids["label_data"].text = f"Usuário há {(datetime.now() - datetime.strptime(data, '%d/%m/%Y')).days} dias"


            self.mudar_tela("homepage")
        except:
            pass

        try:
            requisicao = requests.get(f"https://vitapinabd-default-rtdb.firebaseio.com/{self.local_id}/Refeicoes.json")
            requisicao_dic = requisicao.json()

            pagina_historico = self.root.ids["historicorefeicoespage"]
            lista_vendas = pagina_historico.ids["lista_refeicoes"]
            lista_vendas.clear_widgets()
            for data, refeicao in reversed(list(requisicao_dic.items())):
                dia = Label(text="[color=#000000][size=25][b]" + data.replace("-", "/") + "[/b][/size][/color]", markup=True)
                lista_vendas.add_widget(dia)
                for ref, info in refeicao.items():
                    banner = BannerRefeicao(carboidratos=info["Carboidratos"], calorias=info["Calorias"],
                                         gorduras=info["Gorduras"], nome=info["Nome"],
                                         proteinas=info["Proteinas"], quantidade=info["Quantidade"],
                                         tipo=info["Tipo"], horario=info["Horario"])
                    lista_vendas.add_widget(banner)
        except:
            pass

        try:
            perfil = self.root.ids["perfilpage"]
            requisicao = requests.get(f"https://vitapinabd-default-rtdb.firebaseio.com/{self.local_id}.json")
            requisicao_dic = requisicao.json()
            perfil.ids["nome"].text = self.nome
            perfil.ids["sobrenome"].text = self.sobrenome
            perfil.ids["telefone"].text = requisicao_dic["telefone"]
            perfil.ids["email"].text = requisicao_dic["E-mail"]
            dia, mes, ano = requisicao_dic["Data de Nascimento"].split("/")

        except:
            pass


    def show_popup(self):
        popup_layout = GridLayout(cols=2, padding=[20, 20, 20, 20], spacing=[20, 20])

        with popup_layout.canvas.before:
            Color(0.8, 0.9, 1, 1)
            self.bg_rect = RoundedRectangle(pos=popup_layout.pos, size=popup_layout.size, radius=[20])
            popup_layout.bind(pos=self.update_bg, size=self.update_bg)

        buttons = [
            ('Café da manhã', self.on_button_press),
            ('Almoço', self.on_button_press),
            ('Jantar', self.on_button_press),
            ('Lanche', self.on_button_press)
        ]

        for text, callback in buttons:
            btn = Button(
                text=text,
                background_normal='',
                background_color=(1, 1, 1, 1),
                color=(0, 0, 0, 1),
                size_hint=(0.8, 0.8)
            )

            btn.bind(on_release=callback)
            popup_layout.add_widget(btn)

        self.popup = Popup(
            title='',
            content=popup_layout,
            size_hint=(0.9, 0.6),
            auto_dismiss=True,
            separator_height=0,
            background_color=(0, 0, 0, 0),
        )
        self.popup.open()

    def show_popup_receita(self, nome):
        popup_layout = GridLayout(cols=2, padding=[20, 20, 20, 20], spacing=[20, 20])

        with popup_layout.canvas.before:
            Color(0.8, 0.9, 1, 1)
            self.bg_rect = RoundedRectangle(pos=popup_layout.pos, size=popup_layout.size, radius=[20])
            popup_layout.bind(pos=self.update_bg, size=self.update_bg)
        buttons = [
            ('Fechar', self.fechar_popup),
            ('Cadastrar', partial(self.on_button_press_receita, nome=nome))
        ]

        for text, callback in buttons:
            if text == "Cadastrar":
                btn = Button(
                    text=text,
                    background_normal='',
                    background_color=(1, 1, 1, 1),
                    color=(0, 0, 0, 1),
                    size_hint=(0.8, 0.8)
                )
            else:
                btn = Button(
                    text=text,
                    background_normal='',
                    background_color=(1, 0, 0, 0.6),
                    color=(0, 0, 0, 1),
                    size_hint=(0.8, 0.8)
                )

            btn.bind(on_release=callback)
            popup_layout.add_widget(btn)

        self.popup_receita = Popup(
            title='',
            content=popup_layout,
            size_hint=(0.9, 0.3),
            auto_dismiss=True,
            separator_height=0,
            background_color=(0, 0, 0, 0)
        )
        self.popup_receita.open()

    def on_button_press(self, instance):
        self.popup.dismiss()
        self.root.ids["refeicaopage"].ids["tipo_refeicao"].text = instance.text
        self.mudar_tela("refeicaopage")

    def on_button_press_receita(self, instance, nome):
        self.popup_receita.dismiss()
        requisicao = requests.get(f"https://vitapinabd-default-rtdb.firebaseio.com/Receitas.json")
        requisicao_dic = requisicao.json()


        for info in requisicao_dic:
            if isinstance(info, dict):
                if info.get('Nome') == nome:
                    self.firebase.criar_refeicao(carboidratos=info.get("Carboidratos"), calorias=info.get("Calorias"),
                                             gorduras=info.get("Gorduras"), nome=info.get("Nome"),
                                             proteinas=info.get("Proteinas"), quantidade=info.get("Quantidade"),
                                             tipo=info.get("Tipo"), foto=info.get("Foto"), horario=info.get("Horario"))
                    break

        self.mudar_tela("caloriaspage")

    def fechar_popup(self, instance):
        self.popup_receita.dismiss()

    def update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def carregar_calorias(self):
        pagina_calorias = self.root.ids["caloriaspage"]
        pagina_calorias.ids["calorias_consumidas"].text = "0"
        pagina_calorias.ids["calorias_total"].text = "1700"
        pagina_calorias.ids["calorias_restantes"].text = "1700"
        pagina_calorias.ids["carboidratos"].text = "0"
        pagina_calorias.ids["proteinas"].text = "0"
        pagina_calorias.ids["gorduras"].text = "0"
        requisicao = requests.get(f"https://vitapinabd-default-rtdb.firebaseio.com/{self.local_id}/Refeicoes/{datetime.now().strftime('%d-%m-%Y')}.json")
        requisicao_dic = requisicao.json()
        aux_calorias = 0
        aux_carboidratos = 0
        aux_proteinas = 0
        aux_gorduras = 0
        for chave, valor in requisicao_dic.items():

            calorias = valor["Calorias"]
            carboidratos = valor["Carboidratos"]
            proteinas = valor["Proteinas"]
            gorduras = valor["Gorduras"]
            quantidade = valor["Quantidade"]
            aux_calorias += int(calorias) * int(quantidade)
            aux_carboidratos += int(carboidratos) * int(quantidade)
            aux_proteinas += int(proteinas) * int(quantidade)
            aux_gorduras += int(gorduras) * int(quantidade)


        pagina_calorias.ids["calorias_consumidas"].text = "[color=#000000][size=32][b]" + str(aux_calorias) + "[/b][/size][/color]"
        if int(pagina_calorias.ids["calorias_total"].text) - int(aux_calorias) > 0:
            pagina_calorias.ids["calorias_restantes"].text = "[color=#000000][size=60][b]" + str(int(pagina_calorias.ids["calorias_total"].text) - int(aux_calorias)) + "[/b][/size][/color]"
        else:
            pagina_calorias.ids["calorias_restantes"].text = "[color=#000000][size=60][b]0[/b][/size][/color]"
        pagina_calorias.ids["calorias_total"].text = "[color=#000000][size=32][b]1700[/b][/size][/color]"
        pagina_calorias.ids["carboidratos"].text = "[color=#000000][b]" + str(aux_carboidratos) + "g" + "[/b][/color]"
        pagina_calorias.ids["proteinas"].text = "[color=#000000][b]" + str(aux_proteinas) + "g" + "[/b][/color]"
        pagina_calorias.ids["gorduras"].text = "[color=#000000][b]" + str(aux_gorduras) + "g" + "[/b][/color]"


    def alterar_campos(self):
        perfil = self.root.ids["perfilpage"]
        if perfil.ids["nome"].disabled:
            perfil.ids["nome"].disabled = False
            perfil.ids["sobrenome"].disabled = False
            perfil.ids["telefone"].disabled = False
            perfil.ids["email"].disabled = False
            perfil.ids["dia_nas"].disabled = False
            perfil.ids["ano_nas"].disabled = False
            perfil.ids["mes_nas"].disabled = False
            perfil.ids["sexo"].disabled = False
            perfil.ids["botao_logoff"].text = "[color=#FFFFFF]Alterar Dados[/color]"
            with perfil.ids["botao_logoff"].canvas.before:
                Color(31 / 255, 69 / 255, 153 / 255)
                RoundedRectangle(
                    pos=perfil.ids["botao_logoff"].pos,
                    size=perfil.ids["botao_logoff"].size,
                    radius=[(20, 20), (20, 20), (20, 20), (20, 20)]
                )

        else:
            requisicao = requests.get(f"https://vitapinabd-default-rtdb.firebaseio.com/{self.local_id}.json")
            requisicao_dic = requisicao.json()
            nome = requisicao_dic["Nome"]

            data = requisicao_dic["Data de Cadastro"]
            perfil.ids["botao_logoff"].text = "[color=#0000FF][u]Sair[/u][/color]"
            perfil.ids["botao_logoff"].canvas.before.clear()

            self.data = data
            perfil.ids["nome"].disabled = True
            perfil.ids["nome"].text = self.nome
            perfil.ids["sobrenome"].disabled = True
            perfil.ids["sobrenome"].text = self.sobrenome
            perfil.ids["telefone"].disabled = True
            perfil.ids["telefone"].text = requisicao_dic["telefone"]
            perfil.ids["email"].disabled = True
            perfil.ids["email"].text = requisicao_dic["E-mail"]
            perfil.ids["dia_nas"].disabled = True
            perfil.ids["ano_nas"].disabled = True
            perfil.ids["mes_nas"].disabled = True
            perfil.ids["sexo"].disabled = True

    def mudar_tela(self, id_tela):
        login = self.root.ids["loginpage"]
        login.ids["email"].text = ""
        login.ids["senha"].text = ""

        refeicao = self.root.ids["refeicaopage"]
        refeicao.ids["quantidade"].text = ""
        refeicao.ids["nome"].text = ""
        refeicao.ids["calorias"].text = ""
        refeicao.ids["carboidratos"].text = ""
        refeicao.ids["proteinas"].text = ""
        refeicao.ids["gorduras"].text = ""
        gerenciador = self.root.ids["screen_manager"]
        gerenciador.current = id_tela

MainApp().run()