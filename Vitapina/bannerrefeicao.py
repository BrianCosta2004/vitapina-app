from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle


class BannerRefeicao(GridLayout):
    def __init__(self, **kwargs):
        self.rows = 1
        super().__init__()

        with self.canvas:
            Color(rgb=(1, 1, 1, 1))
            self.rec = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.atualizar_rec, size=self.atualizar_rec)

        carboidratos = kwargs["carboidratos"]
        calorias = kwargs["calorias"]
        gorduras = kwargs["gorduras"]
        proteinas = kwargs["proteinas"]
        nome = kwargs["nome"]
        quantidade = kwargs["quantidade"]
        tipo = (kwargs["tipo"])
        #foto_refeicao = (kwargs["foto"])
        horario = (kwargs["horario"])

        esquerda = FloatLayout()
        esquerda_imagem = Image(pos_hint={"right": 1, "top": 0.95}, size_hint= (1, 0.75),
                                source=f"icones/fotos_alimentos_almoco/Feijoada.png")
        esquerda_label = Label(text="[color=#000000][b]" + nome + "[/b][/color]",
                               size_hint=(1, 0.2), pos_hint={"right": 1, "top": 0.2}, markup=True)
        esquerda.add_widget(esquerda_imagem)
        esquerda.add_widget(esquerda_label)

        meio = FloatLayout()
        meio_label = Label(text="[color=#000000][b]" + calorias + " Kcal[/b][/color]",
                               size_hint=(1, 0.2), pos_hint={"right": 1, "top": 0.6}, markup=True)
        meio.add_widget(meio_label)

        direita = FloatLayout()
        direita_label_data = Label(text=f"[color=#000000][b]{tipo}[/b][/color]", size_hint= (1, 0.33), pos_hint={"right": 1, "top": 0.9}, markup=True)
        direita_label_preco = Label(text=f"[color=#000000][b]Quantidade: {quantidade}g[/b][/color]", size_hint= (1, 0.33), pos_hint={"right": 1, "top": 0.65}, markup=True)
        direita_label_quantidade = Label(text=f"[color=#000000][b]{horario}[/b][/color]", size_hint= (1, 0.33), pos_hint={"right": 1, "top": 0.4}, markup=True)
        direita.add_widget(direita_label_data)
        direita.add_widget(direita_label_preco)
        direita.add_widget(direita_label_quantidade)

        self.add_widget(esquerda)
        self.add_widget(meio)
        self.add_widget(direita)

    def atualizar_rec(self, *args):
        self.rec.pos = self.pos
        self.rec.size = self.size