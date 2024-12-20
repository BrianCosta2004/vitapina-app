from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import ButtonBehavior, Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.effectwidget import EffectWidget, HorizontalBlurEffect
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, RoundedRectangle, Ellipse
from kivy.uix.dropdown import DropDown
from kivy.app import App
from datetime import datetime
from calendar import monthrange


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


class TimeInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        # Permite apenas números
        filtered = "".join(c for c in substring if c.isdigit())
        text = self.text.replace(":", "")  # Remove ":" temporariamente
        new_text = text + filtered

        # Limita o comprimento máximo para 4 dígitos
        if len(new_text) > 4:
            return

        # Valida a primeira entrada: deve ser 0, 1 ou 2
        if len(new_text) == 1 and new_text[0] not in "012":
            return

        # Valida horas completas (dois dígitos no início)
        if len(new_text) >= 2:
            hours = int(new_text[:2])
            if hours > 23:  # Horas inválidas
                return

        # Valida minutos enquanto o usuário digita
        if len(new_text) > 2:
            # Obtém os minutos digitados
            minutes_str = new_text[2:]
            minutes = int(minutes_str) if minutes_str.isdigit() else 0

            if minutes > 59:  # Minutos inválidos
                return

            # Adiciona zero à esquerda apenas se os minutos forem 6, 7, 8 ou 9
            if len(minutes_str) == 1 and minutes in range(6, 10):
                minutes_str = "0" + minutes_str

            formatted_text = new_text[:2] + ":" + minutes_str
        else:
            formatted_text = new_text

        self.text = formatted_text
        self.cursor = (len(self.text), 0)

class DateSelector(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="horizontal", spacing=10, **kwargs)

        # Obter data atual
        self.current_date = datetime.now()
        self.current_day = self.current_date.day
        self.current_month = self.current_date.month


    def get_valid_months(self):
        """Retorna os meses válidos até o mês atual."""
        months = [f"{i:02}" for i in range(1, self.current_month + 1)]
        return months

    def get_valid_days(self, selected_month):
        """Retorna os dias válidos para o mês selecionado."""
        # Converte o mês selecionado para inteiro
        selected_month = int(selected_month)
        days_in_month = monthrange(self.current_date.year, selected_month)[1]

        # Lista de dias até o dia atual se o mês for o atual
        if selected_month == self.current_month:
            return [f"{i:02}" for i in range(1, self.current_day)]
        else:
            return [f"{i:02}" for i in range(1, days_in_month + 1)]

    def update_days(self, spinner, selected_month):
        """Atualiza os valores do spinner de dias com base no mês selecionado."""
        self.day_spinner.values = self.get_valid_days(selected_month)
        self.day_spinner.text = "Dia"


class PhoneInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        # Permitir apenas dígitos
        substring = ''.join(filter(str.isdigit, substring))

        # Obter o texto atual sem formatação
        text = self.text.replace("(", "").replace(")", "").replace(" ", "").replace("-", "")

        # Adicionar o novo caractere
        text = text + substring

        # Impedir que o texto exceda 11 dígitos (DDD + número)
        if len(text) > 11:
            return

        # Formatar o número
        formatted = ""
        if len(text) > 0:
            formatted += "(" + text[:2]
        if len(text) > 2:
            formatted += ") " + text[2:7]
        if len(text) > 7:
            formatted += "-" + text[7:]

        # Atualizar o texto no campo
        self.text = formatted

        # Garantir que o cursor esteja na posição correta
        self.cursor = (len(self.text), 0)


class PhoneApp(App):
    def build(self):
        layout = BoxLayout(padding=10)
        phone_input = PhoneInput(
            hint_text="(XX) XXXXX-XXXX",
            font_size=24,
            size_hint=(1, None),
            height=50
        )
        layout.add_widget(phone_input)
        return layout