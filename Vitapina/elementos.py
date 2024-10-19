from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import ButtonBehavior
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics import Line, Color, Rectangle, RoundedRectangle
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from kivy.properties import NumericProperty


class ImageButton(ButtonBehavior, Image):
    pass


class LabelButton(ButtonBehavior, Label):
    pass


class TextInputRounded(TextInput, FloatLayout, Image):
    pass


class Retangulo(Widget):
    def __init__(self, **kwargs):
        super(Retangulo, self).__init__(**kwargs)
        with self.canvas:
            Color(0, 0, 0, 0)
            self.rect = Rectangle(pos=(0, 0), size=(200, 150))


class CurvaGlicemicaWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(CurvaGlicemicaWidget, self).__init__(**kwargs)

        # Dados fictícios da curva glicêmica (tempo em minutos e nível de glicose em mg/dL)
        tempo = [0, 30, 60, 90, 120, 150, 180]  # Tempo em minutos
        glicose = [90, 140, 160, 130, 110, 100, 90]  # Nível de glicose (mg/dL)

        # Criando o gráfico
        fig, ax = plt.subplots(figsize=(3, 1))
        ax.plot(tempo, glicose, marker='o', linestyle='-', color='b', label='Nível de Glicose')

        # Configurações do gráfico
        ax.set_title("Histórico")
        ax.set_xlabel("Tempo (min)")
        ax.set_ylabel("Glicose (mg/dL)")
        ax.legend()
        ax.grid(False)

        # Convertendo o gráfico para um widget do Kivy
        canvas = FigureCanvasKivyAgg(fig)

        # Adicionando o gráfico ao layout
        self.add_widget(canvas)


class HeatMapLabel(Label):
    intensity = NumericProperty(0.7)  # Propriedade que controla a intensidade de calor

    def __init__(self, **kwargs):
        super(HeatMapLabel, self).__init__(**kwargs)
        self.bind(size=self.update_rect, pos=self.update_rect)
        self.bind(intensity=self.update_color)

        # Desenhando o fundo da Label
        with self.canvas.before:
            self.rect_color = Color(1, 1, 1, 0)  # Cor inicial (branco)
            self.rect = Rectangle(size=self.size, pos=self.pos)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_color(self, *args):
        # Atualizando a cor com base na intensidade (valor entre 0 e 1)
        heat_color = self.get_color_for_intensity(self.intensity)
        self.rect_color.rgba = heat_color

    def get_color_for_intensity(self, intensity):
        # Define as cores de acordo com a intensidade (0 = frio, 1 = quente)
        # Transição de azul (frio) -> verde -> amarelo -> vermelho (quente)
        if intensity < 0.33:
            return (0, 0, 1, 1)  # Azul (frio)
        elif intensity < 0.66:
            return (0, 1, 0, 1)  # Verde (médio)
        else:
            return (1, 0, 0, 1)  # Vermelho (quente)

class RoundedTextInput(TextInput):
    def __init__(self, **kwargs):
        super(RoundedTextInput, self).__init__(**kwargs)
        self.background_normal = ''  # Remove o background padrão
        self.background_active = ''  # Remove o background quando ativo
        self.bind(pos=self.update_background, size=self.update_background)

        with self.canvas.before:
            Color(0.8, 0.8, 0.8, 1)  # Cor de fundo cinza claro
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[15])  # Raio para cantos arredondados

    def update_background(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size