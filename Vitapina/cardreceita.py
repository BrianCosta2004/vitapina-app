from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle
from Vitapina.elementos import ImageButton, LabelButton
from kivy.app import App


class CardReceita(GridLayout):
    def __init__(self, **kwargs):
        self.rows = 1
        super().__init__()

        with self.canvas:
            Color(rgb=(1, 1, 1, 1))
            self.rec = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])
        self.bind(pos=self.atualizar_rec, size=self.atualizar_rec)

        nome = kwargs["nome"]
        pasta = kwargs["pasta"]


        meio = FloatLayout()
        meio_imagem = ImageButton(pos_hint={"right": 0.75, "top": 0.95}, size_hint= (0.5, 0.5),
                                source=f"{pasta}{nome}.png", on_press=lambda x: App.get_running_app().show_popup_receita(nome))
        meio_label = LabelButton(text="[color=#000000][b]" + nome + "[/b][/color]",
                               size_hint=(1, 0.2), pos_hint={"right": 1, "top": 0.4}, markup=True, on_press=lambda x: App.get_running_app().show_popup_receita(nome))
        meio.add_widget(meio_imagem)
        meio.add_widget(meio_label)

        self.add_widget(meio)

    def atualizar_rec(self, *args):
        self.rec.pos = self.pos
        self.rec.size = self.size