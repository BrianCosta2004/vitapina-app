from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import ButtonBehavior, Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.effectwidget import EffectWidget, HorizontalBlurEffect
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color, Rectangle, RoundedRectangle, Ellipse
from kivy.uix.dropdown import DropDown
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from kivy.properties import NumericProperty
from kivy.app import App
from kivy.properties import ObjectProperty


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

         tempo = [0, 30, 60, 90, 120, 150, 180]
         glicose = [90, 98, 75, 102, 97, 88, 91]

         fig, ax = plt.subplots(figsize=(3, 1))
         ax.plot(tempo, glicose, marker='o', linestyle='-', color='k', label='Nível de Glicose')

         ax.set_title("Histórico")
         ax.set_xlabel("Tempo (min)")
         ax.set_ylabel("Glicose (mg/dL)")
         ax.legend()
         ax.grid(False)

         canvas = FigureCanvasKivyAgg(fig)

         self.add_widget(canvas)


class HeatMapLabel(Label):
    intensity = NumericProperty(0.7)

    def __init__(self, **kwargs):
        super(HeatMapLabel, self).__init__(**kwargs)
        self.bind(size=self.update_rect, pos=self.update_rect)
        self.bind(intensity=self.update_color)

        with self.canvas.before:
            self.rect_color = Color(1, 1, 1, 0)
            self.rect = Rectangle(size=self.size, pos=self.pos)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_color(self, *args):
        heat_color = self.get_color_for_intensity(self.intensity)
        self.rect_color.rgba = heat_color

    def get_color_for_intensity(self, intensity):
        if intensity < 0.33:
            return (0, 0, 1, 1)
        elif intensity < 0.66:
            return (0, 1, 0, 1)
        else:
            return (1, 0, 0, 1)

class RoundedTextInput(TextInput):
    def __init__(self, **kwargs):
        super(RoundedTextInput, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_active = ''
        self.bind(pos=self.update_background, size=self.update_background)

        with self.canvas.before:
            Color(0.8, 0.8, 0.8, 1)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[15])

    def update_background(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class AnimatedImage(ButtonBehavior, BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.effect_widget = EffectWidget()
        self.blur_effect = HorizontalBlurEffect(size=10)
        self.effect_widget.effects = [self.blur_effect]

        self.img = Image(source='icones/pina.png', size_hint=(None, None), size=(250, 250),)
        self.effect_widget.add_widget(self.img)

        self.add_widget(self.effect_widget)

        self.animate_image()

    def animate_image(self):
        anim1 = Animation(size=(300, 300), d=0.4) + Animation(size=(250, 250), d=0.4)
        anim1.bind(on_start=self.focus_in)
        anim1.bind(on_complete=self.focus_out)
        anim1.start(self.img)

    def focus_in(self, *args):
        anim_blur = Animation(size=0, d=0.2)
        anim_blur.start(self.blur_effect)

    def focus_out(self, *args):
        anim_blur = Animation(size=1, d=0.2)
        anim_blur.start(self.blur_effect)


class CircleAroundButton(Widget):

    def show_circle(self, pos, size):
        # Limpa o círculo anterior
        self.canvas.clear()

        # Desenha um novo círculo na posição do botão
        with self.canvas:
            Color(19/255, 155/255, 173/255, 1)  # Define a cor e a opacidade do círculo
            diameter = max(size) * 0.5  # Define o diâmetro do círculo
            Ellipse(pos=(pos[0] - diameter / 2, pos[1] - diameter / 2), size=(diameter, diameter))

class CircleLayout(FloatLayout):
    pass


class SearchBox(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.search_input = TextInput(hint_text="Digite para buscar...", multiline=False)
        self.search_input.bind(text=self.on_text)
        self.add_widget(self.search_input)

        self.dropdown = DropDown()
        self.suggestions = []

    def on_text(self, instance, value):
        self.dropdown.clear_widgets()

        if value == "":
            self.dropdown.dismiss()
            return

        todos_alimentos = App.get_running_app().firebase.pegar_opcoes(value)

        self.suggestions = [option for option in todos_alimentos if value.lower() in option.lower()]

        if self.suggestions:
            for option in self.suggestions:
                btn = Button(text=option, size_hint_y=None, height=30)
                btn.bind(on_release=lambda btn: self.select_option(btn.text))
                self.dropdown.add_widget(btn)

            if not self.dropdown.attach_to:
                self.dropdown.open(self.search_input)
        else:
            self.dropdown.dismiss()

    def select_option(self, text):
        self.search_input.text = text
        self.dropdown.dismiss()

    def validate(self):
        if self.search_input.text not in self.suggestions:
            self.search_input.text = ""