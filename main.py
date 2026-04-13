import json
import os
from datetime import datetime
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from lunardate import LunarDate

ZODIAC = ["Macaco 猴", "Galo 雞", "Cão 狗", "Porco 豬", 
          "Rato 鼠", "Boi 牛", "Tigre 虎", "Coelho 兔", 
          "Dragão 龍", "Serpente 蛇", "Cavalo 馬", "Cabra 羊"]

ELEMENTS = [("Metal", "金"), ("Água", "水"), ("Madeira", "木"), ("Fogo", "火"), ("Terra", "土")]


class MainScreen(Screen):
    result_text = StringProperty("Insira os dados e clique em Calcular")

    def calculate(self, *args):
        try:
            d = int(self.ids.day.text)
            m = int(self.ids.month.text)
            y = int(self.ids.year.text)

            dt = datetime(y, m, d)
            lunar = LunarDate.fromSolarDate(dt.year, dt.month, dt.day)

            signo = ZODIAC[lunar.year % 12]
            element_idx = (dt.year % 10) // 2
            el_nome, el_hanzi = ELEMENTS[element_idx]
            pol = "Yang 陽" if dt.year % 2 == 0 else "Yin 陰"

            self.result_text = f"[b]{signo}[/b]\nElemento: {el_nome} {el_hanzi}\nPolaridade: {pol}"

        except Exception:
            self.result_text = "Data Inválida! Verifique os campos."

    def save_profile(self):
        if "Inválida" in self.result_text or self.ids.year.text == "":
            return

        nome = self.ids.name_input.text or "Sem Nome"

        novo_perfil = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "nome": nome,
            "dia": self.ids.day.text,
            "mes": self.ids.month.text,
            "ano": self.ids.year.text,
            "info": self.result_text
        }

        perfis = self.load_data()
        perfis.append(novo_perfil)
        self.save_data(perfis)

        self.result_text = "Perfil guardado com sucesso!"

    def load_data(self):
        if os.path.exists('perfis.json'):
            try:
                with open('perfis.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
            except:
                pass
        return []

    def save_data(self, data):
        with open('perfis.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


class MenuScreen(Screen):
    perfis_list = ListProperty([])

    def on_enter(self):
        self.refresh_list()

    def refresh_list(self):
        if os.path.exists('perfis.json'):
            try:
                with open('perfis.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.perfis_list = data
                    else:
                        self.perfis_list = []
            except:
                self.perfis_list = []
        else:
            self.perfis_list = []

        self.update_container()

    def update_container(self):
        container = self.ids.container
        container.clear_widgets()

        for p in self.perfis_list:
            # 🔒 Proteção contra dados inválidos
            if not isinstance(p, dict):
                continue

            try:
                nome = p.get('nome', 'Sem Nome')
                dia = p.get('dia', '?')
                mes = p.get('mes', '?')
                ano = p.get('ano', '?')
                pid = p.get('id', '')

                row = BoxLayout(size_hint_y=None, height='65dp', spacing=10)

                btn_txt = f"{nome} ({dia}/{mes}/{ano})"

                item_btn = Button(
                    text=btn_txt,
                    background_color=(0.15, 0.15, 0.15, 1),
                    background_normal=''
                )
                item_btn.bind(on_release=lambda x, p=p: self.load_profile(p))

                del_btn = Button(
                    text="X",
                    size_hint_x=None,
                    width='60dp',
                    background_color=(0.7, 0.2, 0.2, 1),
                    background_normal=''
                )
                del_btn.bind(on_release=lambda x, pid=pid: self.delete_profile(pid))

                row.add_widget(item_btn)
                row.add_widget(del_btn)
                container.add_widget(row)

            except Exception:
                continue  # ignora qualquer perfil quebrado

    def delete_profile(self, profile_id):
        self.perfis_list = [
            p for p in self.perfis_list
            if isinstance(p, dict) and p.get('id') != profile_id
        ]

        with open('perfis.json', 'w', encoding='utf-8') as f:
            json.dump(self.perfis_list, f, indent=4, ensure_ascii=False)

        self.update_container()

    def load_profile(self, profile):
        if not isinstance(profile, dict):
            return

        main = self.manager.get_screen('main')

        main.ids.name_input.text = profile.get('nome', '')
        main.ids.day.text = profile.get('dia', '')
        main.ids.month.text = profile.get('mes', '')
        main.ids.year.text = profile.get('ano', '')

        main.calculate()
        self.manager.current = 'main'


class WindowManager(ScreenManager):
    pass


class AstroApp(App):
    def build(self):
        return Builder.load_file("style.kv")


if __name__ == "__main__":
    AstroApp().run()
