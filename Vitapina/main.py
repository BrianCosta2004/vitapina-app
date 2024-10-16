from kivy.app import App
from kivy.lang import Builder
from telas import *
from elementos import *
import requests
import os
from functools import partial
from myfirebase import MyFirebase
from datetime import date

GUI = Builder.load_file("main.kv")


class MainApp(App):
    cliente = None
    produto = None
    unidade = None

    def build(self):
        self.firebase = MyFirebase()
        return GUI


    def mudar_tela(self, id_tela):
        gerenciador = self.root.ids["screen_manager"]
        gerenciador.current = id_tela

MainApp().run()