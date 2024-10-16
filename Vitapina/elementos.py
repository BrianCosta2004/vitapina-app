from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import ButtonBehavior
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics import Line, Color, Rectangle
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


class ImageButton(ButtonBehavior, Image):
    pass


class LabelButton(ButtonBehavior, Label):
    pass


class TextInputRounded(TextInput, FloatLayout, Image):
    pass


class SemicircleProgressBar(Widget):
    def __init__(self, **kwargs):
        super(SemicircleProgressBar, self).__init__(**kwargs)
        self.progress = 0
        Clock.schedule_interval(self.update_progress, 0.1)

    def update_progress(self, dt):
        self.progress = (self.progress + 1) % 101
        self.canvas.clear()
        with self.canvas:
            # Cor de fundo (base do arco)
            Color(0.9, 0.9, 0.6)
            Line(circle=(self.center_x, self.center_y, 100, -90, 90), width=10)

            # Cor da barra de progresso (arco preenchido)
            Color(0.2, 0.2, 0.8)
            Line(circle=(self.center_x, self.center_y, 100, -90, -90 + (self.progress / 100) * 180), width=10)


class MainWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.orientation = 'horizontal'

        # ProgressBar semicircular
        self.progress_bar = SemicircleProgressBar(size=(200, 200), size_hint=(None, None))
        self.add_widget(self.progress_bar)

        # Label para mostrar o valor da barra de progresso
        self.value_label = Label(text="0", font_size=50)
        self.add_widget(self.value_label)

        # Atualizar o valor da label conforme o progresso
        Clock.schedule_interval(self.update_label, 0.1)

    def update_label(self, dt):
        self.value_label.text = str(self.progress_bar.progress)


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