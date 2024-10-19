from kivy.app import App
from kivy.lang import Builder
from telas import *
from elementos import *
import requests
import os
from functools import partial
from myfirebase import MyFirebase
from datetime import datetime

GUI = Builder.load_file("main.kv")


class MainApp(App):

    def build(self):
        self.firebase = MyFirebase()
        return GUI

    def on_start(self):
        arquivos = os.listdir("icones/fotos_alimentos_cafe")
        pagina_receitas = self.root.ids["receitaspage"]
        lista_produtos = pagina_receitas.ids["lista_alimentos_cafe"]
        print(self.root.ids["receitaspage"].ids["lista_alimentos_cafe"])
        for foto_produto in arquivos:
            imagem = ImageButton(source=f"icones/fotos_alimentos_cafe/{foto_produto}")
            label = LabelButton(text=foto_produto.replace(".png", "").capitalize())
            lista_produtos.add_widget(imagem)
            lista_produtos.add_widget(label)

        arquivos = os.listdir("icones/fotos_alimentos_almoco")
        pagina_receitas = self.root.ids["receitaspage"]
        lista_produtos = pagina_receitas.ids["lista_alimentos_almoco"]
        for foto_produto in arquivos:
            imagem = ImageButton(source=f"icones/fotos_alimentos_almoco/{foto_produto}")
            label = LabelButton(text=foto_produto.replace(".png", "").capitalize())
            lista_produtos.add_widget(imagem)
            lista_produtos.add_widget(label)

        arquivos = os.listdir("icones/fotos_alimentos_janta")
        pagina_receitas = self.root.ids["receitaspage"]
        lista_produtos = pagina_receitas.ids["lista_alimentos_janta"]
        for foto_produto in arquivos:
            imagem = ImageButton(source=f"icones/fotos_alimentos_janta/{foto_produto}")
            label = LabelButton(text=foto_produto.replace(".png", "").capitalize())
            lista_produtos.add_widget(imagem)
            lista_produtos.add_widget(label)

    def carregar_infos_usuario(self):
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
            data = requisicao_dic["Data"]
            self.nome = nome
            self.sobrenome = sobrenome
            self.data = data
            pagina_perfil = self.root.ids["perfilpage"]
            pagina_perfil.ids["label_nome"].text = f"[size=25][b]{nome} {sobrenome}[/b][/size]"
            pagina_perfil.ids["label_data"].text = f"Usuário há {(datetime.now() - datetime.strptime(data, "%d/%m/%Y")).days} dias"


            self.mudar_tela("homepage")
        except:
            pass

    def mudar_tela(self, id_tela):
        gerenciador = self.root.ids["screen_manager"]
        gerenciador.current = id_tela

MainApp().run()