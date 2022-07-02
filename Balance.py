from Constants import COLORS
from pygame_menu.widgets import *
import json


class Balance(TextInput):
    def __init__(self, title, textinput_id, x, y, **kwargs) -> None:
        super().__init__(title, textinput_id, **kwargs)  # inherit from TextInput
        self.set_position(x, y)
        self.set_border(5, COLORS["green"])
        self.set_padding((15, 15))
        self.set_font(
            font="assets/Minecraft.ttf",
            font_size=40,
            color=COLORS["green"],
            selected_color=COLORS["red_black"],
            readonly_color=COLORS["red"],
            readonly_selected_color=COLORS["red_black"],
            background_color=None,
            antialias=True,
        )
        self.set_background_color(COLORS["black"])
        self._money = 0

    @property
    def money(self):
        return self._money

    @money.setter
    def money(self, value):
        try:
            self._money = int(value)
            msg_len = len(str(self._money))
            if msg_len > self._maxchar:  # validation for maxchar
                self.set_value("inv")
            else:
                self.set_value(str(self._money) + (6 - msg_len) * " ")
        except ValueError:
            self.set_value("inv")
        return

    def read_money(self):
        # reads money from the file
        with open("properties.json") as f:
            money_obj: dict = json.load(f)

        self.money = int(money_obj["coins"])

    def write_money(self):
        # writes money to file
        with open("properties.json", "r") as f:
            money_obj = json.load(f)

        money_obj["coins"] = self._money

        with open("properties.json", "w") as f:
            f.seek(0)
            json.dump(money_obj, f, indent=4)
            f.truncate()
