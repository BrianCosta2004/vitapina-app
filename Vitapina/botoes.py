from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import ButtonBehavior
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics import Line, Color


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
            Line(circle=(self.center_x, self.center_y, 100, 270, 90), width=15)

            # Cor da barra de progresso (arco preenchido)
            Color(0.2, 0.2, 0.8)
            Line(circle=(self.center_x, self.center_y, 100, 270, 270 - (self.progress / 100) * 180), width=15)


class MainWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'

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