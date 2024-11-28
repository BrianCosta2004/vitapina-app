from kivy.uix.label import Label
from kivy.uix.button import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle
from myfirebase import MyFirebase


class BannerRefeicao(ButtonBehavior, GridLayout):
    def __init__(self, **kwargs):
        self.cols = 1
        super().__init__()

        with self.canvas:
            Color(rgb=(1, 0.949, 0.871, 1))
            self.rec = RoundedRectangle(size=self.size, pos=self.pos, radius=[10, 10, 10, 10])
        self.bind(pos=self.atualizar_rec, size=self.atualizar_rec)

        calorias = kwargs["calorias"]
        tipo = (kwargs["tipo"])
        horario = (kwargs["horario"])
        id_ref = kwargs["id"]
        data = kwargs["data"]

        self.on_release = lambda : MyFirebase().infos_card(id_ref, data)

        layout_texto = BoxLayout(orientation='vertical', padding=(10, 5), spacing=1)

        tipo_label = Label(text=f"[color=#000000][b]{tipo}[/b][/color]", markup=True,
                           size_hint_y=None, height=20, halign='left', valign='middle')
        tipo_label.bind(size=tipo_label.setter('text_size'))

        calorias_label = Label(text=f"[color=#000000]{calorias} Kcal[/color]", markup=True,
                               size_hint_y=None, height=20, halign='left', valign='middle')
        calorias_label.bind(size=calorias_label.setter('text_size'))

        horario_label = Label(text=f"[color=#000000]{horario}[/color]", markup=True,
                              size_hint_y=None, height=20, halign='left', valign='middle')
        horario_label.bind(size=horario_label.setter('text_size'))

        aux_label = Label(text="", size_hint_y=None, height=15, halign='left', valign='middle')
        aux_label.bind(size=aux_label.setter('text_size'))

        layout_texto.add_widget(tipo_label)
        layout_texto.add_widget(calorias_label)
        layout_texto.add_widget(aux_label)
        layout_texto.add_widget(horario_label)

        self.add_widget(layout_texto)


    def atualizar_rec(self, *args):
        self.rec.pos = self.pos
        self.rec.size = self.size