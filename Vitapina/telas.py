from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.clock import Clock
from datetime import datetime


class SplashScreen(Screen):
    pass
    #Clock.schedule_once(lambda dt: App.get_running_app().mudar_tela("loginpage"), 4.1)


class LoginPage(Screen):
    pass


class CadastroPage(Screen):
    pass


class CaloriasPage(Screen):
    pass


class GlicemiaPage(Screen):
    pass


class PerfilPage(Screen):
    pass


class ReceitasPage(Screen):
    pass


class AdicionarReceitasPage(Screen):
    pass


class EditarPerfilPage(Screen):
    pass


class HistoricoRefeicoesPage(Screen):
    pass


class RefeicaoPage(Screen):
    pass


class DetalhesReceitaPage(Screen):
    pass


class DetalhesRefeicaoPage(Screen):
    pass