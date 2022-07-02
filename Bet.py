from pygame_menu.widgets import *
from Constants import COLORS


class Bet(TextInput):
    def __init__(self, title, textinput_id, x, y, **kwargs) -> None:
        super().__init__(title, textinput_id, **kwargs)
        self.set_position(x, y)
        self.set_border(5, COLORS["white"])
        self.set_padding((15, 15))
        self.set_font(
            font="assets/Minecraft.ttf",
            font_size=50,
            color=COLORS["green"],
            selected_color=COLORS["red_black"],
            readonly_color=COLORS["red"],
            readonly_selected_color=COLORS["red_black"],
            background_color=COLORS["black"],
            antialias=True,
        )
        self.set_background_color(COLORS["black"])
