from kivy.app import App
from kivy.lang import Builder
from telas import *
from botoes import *
import requests
from bannervenda import BannerVenda
import os
from functools import partial
from myfirebase import MyFirebase
from bannervendedor import BannerVendedor
from datetime import date

GUI = Builder.load_file("main.kv")


class MainApp(App):

    def build(self):
        return GUI

MainApp().run()