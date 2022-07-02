"""
## RaceAndWin ## - A Zero-Player Game made for fun

MIT License

Copyright (c) 2022 Bogdan Ungureanu

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Docs: 
https://pygame-menu.readthedocs.io/en/4.0.6/
https://www.pygame.org/docs/
"""

import json
import pygame
from pygame.constants import MOUSEBUTTONUP
import pygame.display, pygame.event, pygame.image, pygame.time, pygame.transform, pygame.rect, pygame.sprite, pygame.font, pygame.draw
from pygame_menu.locals import ALIGN_CENTER
from pygame_menu.widgets import *
from pygame.image import *
from pygame.transform import *
from Balance import Balance
from Bet import Bet
from Racer import Racer
from Constants import COLORS

pygame.init()


class Game:

    # STATES = ["main_menu", "bet_screen", "race", "leaderboard", "settings"(options), "about"]

    def __init__(self, width, height, fps) -> None:
        # app-related vars
        self._run = True
        self._width, self._height = width, height
        self._game_state = "main_menu"
        self._clock = pygame.time.Clock()
        self._fps = fps
        self._events = []

        # create instance of window
        self._win = pygame.display.set_mode((self._width, self._height))

        pygame.display.set_caption("RaceAndWin")

        # load textures
        self.load_textures()
        pygame.display.set_icon(scale(self._images[1], (30, 30)))

        # some variables
        self._race_sprites = []
        self._clasament = []
        self._option_selectors = []
        self._racer_attr = {
            "type": "default",
            "speed": "medium",
            "images": [
                load(e)
                for e in json.load(open("properties.json", "r"))["racers"][0]["images"]
            ],
        }

        # balance
        self._balance = Balance(
            "$ ",
            "balance",
            self._width - 50,
            50,
            maxchar=7,
            cursor_color=COLORS["white"],
        )
        self._balance.read_money()

        # init every attribute
        self._init_main_menu()
        self._init_options()
        self._init_about()
        self._init_bet_screen()

        self.set_state(self._game_state)  # set state menu

    def load_textures(self):
        self._bk = scale(load("assets/bk.png"), (self._width, self._height))
        self._drum = scale(
            load("assets/grass.png"), (int(self._width / 1.3), self._height // 10)
        )
        self._font = pygame.font.Font("assets/Minecraft.ttf", 50)
        self._finish = load("assets/finish.png")

        # default images for animation and character, this attribute can be changed inside _init_settings
        self._images = [
            load(e)
            for e in json.load(open("properties.json", "r"))["racers"][0]["images"]
        ]

        self._setting = scale(load("assets/settings.png"), (100, 100))
        self._raft = scale(load("assets/shelf.png"), (200, 25))

    def set_state(self, state):
        # sets the current window
        # put here the functions that execute only once before each screen and during the button callback
        self._game_state = state

        if self._game_state == "main_menu":
            self._init_main_menu()
            self._init_bet_screen()

        elif self._game_state == "settings":
            pass

        elif self._game_state == "bet_screen":
            self._init_racers()
            self._init_bet_screen()

        elif self._game_state == "race":
            self._init_race()

        elif self._game_state == "leaderboard":
            self._init_leaderboard()

        elif self._game_state == "about":
            self._init_about()

        elif self._game_state == "quit":
            self._run = False
            self._balance.write_money()

    def _init_leaderboard(self):
        # init widgets
        self.leaderboard_widgets = []
        lbl = Label("Leaderboard")
        lbl.set_font(
            font="assets/Minecraft.ttf",
            font_size=50,
            color=COLORS["green"],
            selected_color=COLORS["green"],
            readonly_color=COLORS["green"],
            readonly_selected_color=COLORS["green"],
            background_color=None,
            antialias=True,
        )
        lbl.add_underline(COLORS["white"], offset=5, width=3)
        lbl.set_position(self._width // 2 - lbl.get_width() // 2, self._height // 15)
        lbl.set_background_color(COLORS["black"])
        lbl.render()
        self.leaderboard_widgets.append(lbl)

        lbl = Label("")
        lbl.set_font(
            font="assets/Minecraft.ttf",
            font_size=40,
            color=COLORS["green"],
            selected_color=COLORS["green"],
            readonly_color=COLORS["green"],
            readonly_selected_color=COLORS["green"],
            background_color=None,
            antialias=True,
        )
        lbl.add_underline(COLORS["white"], offset=5, width=3)
        lbl.set_position(self._width // 2 - lbl.get_width() // 2, self._height - 100)
        lbl.set_background_color(COLORS["black"])
        lbl.render()
        self.leaderboard_widgets.append(lbl)

        btn = Button("Again?", "again", self.set_state, "bet_screen")
        btn.set_font(
            font="assets/Minecraft.ttf",
            font_size=30,
            color=COLORS["green"],
            selected_color=COLORS["white"],
            readonly_color=COLORS["green"],
            readonly_selected_color=COLORS["green"],
            background_color=None,
            antialias=True,
        )
        btn.set_background_color(COLORS["black"])

        def onmouseover():
            btn.set_background_color(COLORS["green"]),
            btn.update_font({"color": COLORS["black"]})

        def onmouseleave():
            btn.set_background_color(COLORS["black"])
            btn.update_font({"color": COLORS["green"]})

        btn.set_onmouseover(onmouseover)
        btn.set_onmouseleave(onmouseleave)
        btn.set_padding((20, 20))
        btn.set_border(4, COLORS["green"])
        btn.set_position(
            self._width - btn.get_width() - 10, self._height - btn.get_height() - 10
        )
        btn.render()
        self.leaderboard_widgets.append(btn)

        # return money
        return_money = 0
        total_bet = 0
        has_bet = 0
        for racer in self._race_sprites:
            if racer.bet != 0:
                has_bet = 1

            if (
                racer.index == self._clasament[0].index
                or racer.time == self._clasament[0].time
            ):
                return_money = max(4 * racer.bet, return_money)

            total_bet += racer.bet

        if has_bet == 1:
            profit = return_money - total_bet
            if profit >= 0:
                self.leaderboard_widgets[1].set_title(f"You've won {profit}$")
            elif profit < 0:
                self.leaderboard_widgets[1].set_title(f"You've lost {profit}$")

            self._balance.money = self._balance.money + return_money
        else:
            self.leaderboard_widgets[1].set_title("You didn't bet")

        self._balance.set_position(20, 20)
        self.back_btn.set_position(50, self._height - btn.get_height() - 10)

    def _init_main_menu(self):
        self.menu_widgets = []

        lbl = Label("Race And Win")
        lbl.set_font(
            font="assets/Minecraft.ttf",
            font_size=50,
            color=COLORS["white"],
            selected_color=COLORS["white"],
            readonly_color=COLORS["white"],
            readonly_selected_color=COLORS["white"],
            background_color=None,
            antialias=True,
        )
        lbl.add_underline(COLORS["white"], offset=5, width=3)
        lbl.set_position(self._width // 2 - lbl.get_width() // 2, self._height // 15)
        lbl.render()

        self.menu_widgets.append(lbl)

        btn = Button("Play", "play", self.set_state, "bet_screen")
        btn.set_font(
            font="assets/Minecraft.ttf",
            font_size=50,
            color=COLORS["green"],
            selected_color=COLORS["white"],
            readonly_color=COLORS["green"],
            readonly_selected_color=COLORS["green"],
            background_color=None,
            antialias=True,
        )
        btn.set_position(self._width // 2 - btn.get_width() // 2, self._height // 4)

        self.menu_widgets.append(btn)

        btn = Button("About", "about", self.set_state, "about")
        btn.set_font(
            font="assets/Minecraft.ttf",
            font_size=50,
            color=COLORS["white"],
            selected_color=COLORS["green"],
            readonly_color=COLORS["white"],
            readonly_selected_color=COLORS["white"],
            background_color=None,
            antialias=True,
        )
        btn.set_position(
            self._width // 2 - btn.get_width() // 2, self._height // 4 + 100
        )

        self.menu_widgets.append(btn)
        # btn
        btn = Button("Options", "settings", self.set_state, "settings")
        btn.set_font(
            font="assets/Minecraft.ttf",
            font_size=50,
            color=COLORS["white"],
            selected_color=COLORS["green"],
            readonly_color=COLORS["white"],
            readonly_selected_color=COLORS["white"],
            background_color=None,
            antialias=True,
        )
        btn.set_position(
            self._width // 2 - btn.get_width() // 2, self._height // 4 + 200
        )
        self.menu_widgets.append(btn)

        btn = Button("Quit", "quit", self.set_state, "quit")
        btn.set_font(
            font="assets/Minecraft.ttf",
            font_size=50,
            color=COLORS["red"],
            selected_color=COLORS["red_black"],
            readonly_color=COLORS["red"],
            readonly_selected_color=COLORS["red_black"],
            background_color=None,
            antialias=True,
        )
        btn.set_position(
            self._width // 2 - btn.get_width() // 2, self._height // 4 + 300
        )
        self.menu_widgets.append(btn)

        for widget in self.menu_widgets:
            widget.set_padding((20, 20))

        self.current_button = 1

    def set_options(self, opt_name, *args):
        opt_name = opt_name[0][0]
        # print(opt_name)
        if opt_name in ["slow", "medium", "fast", "ultrasonic"]:
            self._racer_attr["speed"] = opt_name

        elif opt_name in ["1280x720"]:
            pass
        # self.width, self.height = int(opt.split('x')[0]), int(opt.split('x')[0])
        else:

            with open("properties.json") as f:
                opt_obj: dict = json.load(f)
            for horse_obj in opt_obj["racers"]:

                if horse_obj["name"] == opt_name:
                    self._racer_attr["images"] = [
                        scale(load(e), (180, 180)) for e in horse_obj["images"]
                    ]
                    self._racer_attr["type"] = opt_name

    def _init_options(self):
        self._option_selectors = []
        with open("properties.json") as f:
            opt_obj: dict = json.load(f)

        horse_names = [(e["name"], i) for i, e in enumerate(opt_obj["racers"])]
        drop = Selector(title="Select Racer: ", items=horse_names, default=0)
        self._option_selectors.append(drop)
        drop = Selector(
            title="Select Speed: ",
            items=[("slow", 1), ("medium", 2), ("fast", 3), ("ultrasonic", 4)],
            default=1,
        )
        self._option_selectors.append(drop)
        drop = Selector(
            title="Video Resolution: ",
            items=[
                ("1280x720", 1)
                # ("1920x1080", 2),
            ],
        )

        self._option_selectors.append(drop)

        for i in range(len(self._option_selectors)):
            drop = self._option_selectors[i]
            drop.set_position(self._width // 4, self._height // 4 + (i + 1) * 100)
            drop.set_font(
                font="assets/Minecraft.ttf",
                font_size=50,
                color=COLORS["green"],
                selected_color=COLORS["red_black"],
                readonly_color=COLORS["red"],
                readonly_selected_color=COLORS["red_black"],
                background_color=None,
                antialias=True,
            )
            drop.set_padding((15, 15))
            # drop.set_alignment(ALIGN_CENTER)
            drop.set_border(5, COLORS["green"])
            drop.set_onchange(self.set_options)
            drop.render()

        lbl = Label("Options")
        lbl.set_font(
            font="assets/Minecraft.ttf",
            font_size=50,
            color=COLORS["white"],
            selected_color=COLORS["white"],
            readonly_color=COLORS["white"],
            readonly_selected_color=COLORS["white"],
            background_color=None,
            antialias=True,
        )
        lbl.add_underline(COLORS["white"], offset=5, width=3)
        lbl.set_position(self._width // 2 - lbl.get_width() // 2, self._height // 15)
        lbl.render()
        self._option_selectors.append(lbl)

    def _init_bet_screen(self):
        btn = Button("Race!", "race", self.set_state, "race")
        btn.set_font(
            font="assets/Minecraft.ttf",
            font_size=50,
            color=COLORS["green"],
            selected_color=COLORS["white"],
            readonly_color=COLORS["green"],
            readonly_selected_color=COLORS["green"],
            background_color=None,
            antialias=True,
        )
        btn.set_position(
            self._width - btn.get_width() - 30, self._height - btn.get_height() - 30
        )
        btn.set_background_color(COLORS["black"])

        def onmouseover():
            btn.set_background_color(COLORS["green"]),
            btn.update_font({"color": COLORS["black"]})

        def onmouseleave():
            btn.set_background_color(COLORS["black"])
            btn.update_font({"color": COLORS["green"]})

        btn.set_onmouseover(onmouseover)
        btn.set_onmouseleave(onmouseleave)
        btn.set_padding((20, 20))
        btn.set_border(4, COLORS["green"])
        btn.render()
        self.race_btn = btn

        btn2 = Button("Menu", "back", self.set_state, "main_menu")  # self.prev_state
        btn2.set_font(
            font="assets/Minecraft.ttf",
            font_size=30,
            color=COLORS["green"],
            selected_color=COLORS["white"],
            readonly_color=COLORS["green"],
            readonly_selected_color=COLORS["green"],
            background_color=None,
            antialias=True,
        )
        btn2.set_position(15, 15)
        btn2.set_background_color(COLORS["black"])

        def onmouseover():
            btn2.set_background_color(COLORS["green"]),
            btn2.update_font({"color": COLORS["black"]})

        def onmouseleave():
            btn2.set_background_color(COLORS["black"])
            btn2.update_font({"color": COLORS["green"]})

        btn2.set_onmouseover(onmouseover)
        btn2.set_onmouseleave(onmouseleave)
        btn2.set_padding((20, 20))
        btn2.set_border(4, COLORS["green"])
        btn2.render()

        self.back_btn = btn2

        self.race_labels = []

        for i in range(1, len(self._race_sprites) + 1):
            self._race_sprites[i - 1].set_pos(i * 250 - 50, self._height - 200)
            lbl = Balance(
                "$",
                f"{self._race_sprites[i-1].display_name}",
                i * 250 - 100,
                self._height - 350,
                maxchar=6,
            )
            lbl.money = 0
            self.race_labels.append(lbl)

        self._balance.set_alignment(ALIGN_CENTER)
        self._balance.set_font(
            font="assets/Minecraft.ttf",
            font_size=50,
            color=COLORS["green"],
            selected_color=COLORS["red_black"],
            readonly_color=COLORS["red"],
            readonly_selected_color=COLORS["red_black"],
            background_color=None,
            antialias=True,
        )
        # self.balance.set_max_width(200)
        self._balance.set_position(self._width - 250, self._balance.get_height() // 2)

        self.bet = Bet(
            "Bet: ",
            "main_bet",
            self._width - 100,
            100,
            maxchar=7,
            cursor_size=(5, 5),
            cursor_color=(255, 255, 255),
            maxwidth_dynamically_update=False,
        )
        self.bet.set_position(
            self._width // 2 - self.bet.get_width(),
            self._height // 3 - self.bet.get_height() // 2,
        )

    def _init_racers(self):
        self._race_sprites = []
        font = pygame.font.Font("assets/Minecraft.ttf", 20)

        with open("properties.json", "r") as f:
            names = json.load(f)["names"]

        for i in range(1, 5):
            race_sprite = Racer(
                self._racer_attr["images"][0].get_width(),
                self._racer_attr["images"][0].get_height(),
                self._width // 9,
                i * self._height // 6 - 50,
                i,
                font,
                names[i - 1].strip("\n"),
                self._racer_attr["images"],
                self._racer_attr["speed"],
                self._racer_attr["type"],
            )
            # race_sprite.prepare_race()
            self._race_sprites.append(race_sprite)

    def _init_about(self):
        pass

    def _init_race(self):
        self._clasament = []

        self._balance.set_position(
            self._width // 2 + self._balance.get_width(),
            self._balance.get_height() // 2,
        )
        border = self._finish.get_rect()
        border.x, border.y = (self._width - 120, 0)
        font = pygame.font.Font("assets/Minecraft.ttf", 80)
        font.set_bold(True)
        font.set_italic(True)

        for i in range(3, -1, -1):

            self._win.blit(self._bk, (0, 0))
            self._win.blit(self._finish, border)
            for j in range(4):
                self._win.blit(
                    self._drum, ((self._width // 9, (j + 1) * self._height // 5))
                )
                self._win.blit(
                    pygame.font.Font("assets/Minecraft.ttf", 30).render(
                        f"{self._race_sprites[j].bet}$", True, COLORS["green"]
                    ),
                    (self._width // 9, (j + 1) * self._height // 5 - 50),
                )

            self._balance.draw(self._win)
            self.back_btn.draw(self._win)

            if i != 0:
                self._win.blit(
                    font.render(str(i), True, COLORS["red"]), (self._width // 2, 20)
                )
            else:
                self._win.blit(
                    font.render("RACE!", True, COLORS["red"]), (self._width // 4, 20)
                )

            pygame.display.update()
            pygame.time.delay(1000)

        for i in range(len(self._race_sprites)):
            self._race_sprites[i].set_pos(self._width // 9, (i + 1) * self._height // 5)
            self._race_sprites[i].prepare_race()
            # print(self.race_sprites[i].racer_speed)

    def loop_menu(self):
        self._win.blit(self._bk, (0, 0))

        for event in self._events:
            if event.type == pygame.KEYDOWN:
                self.menu_widgets[self.current_button].select(False)

                if event.key == pygame.K_DOWN:
                    self.current_button += 1
                elif event.key == pygame.K_UP:
                    self.current_button -= 1

            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                for e in self.menu_widgets:
                    if e.get_rect().collidepoint(pos) == True:
                        e.apply()

        if self.current_button >= len(self.menu_widgets):
            self.menu_widgets[self.current_button - 1].select(False)
            self.current_button = 1

        if self.current_button < 1:
            self.current_button = len(self.menu_widgets) - 1
            self.menu_widgets[1].select(False)

        self.menu_widgets[self.current_button].select(True)

        # print(f"{self.current_button} selected")

        self.menu_widgets[0].draw(self._win)  # the first is the label
        dec = pygame.transform.scale(self._racer_attr["images"][0], (100, 100))
        for i in range(1, len(self.menu_widgets)):

            if self.menu_widgets[i].is_selected():  # important
                self.menu_widgets[i].update(self._events)
                self._win.blit(
                    dec,
                    (
                        self.menu_widgets[self.current_button].get_rect().centerx - 200,
                        self.menu_widgets[self.current_button].get_rect().y - 20,
                    ),
                )
                self._win.blit(
                    dec,
                    (
                        self.menu_widgets[self.current_button].get_rect().centerx
                        + dec.get_width()
                        - 10,
                        self.menu_widgets[self.current_button].get_rect().y - 20,
                    ),
                )

            self.menu_widgets[i].draw(self._win)

    def loop_bet_screen(self):
        self._win.blit(self._bk, (0, 0))

        for i in range(len(self._race_sprites)):
            racer = self._race_sprites[i]
            # print(racer.racer_type)
            lbl = self.race_labels[i]
            if racer.is_clicked(self._events):

                displaybet, value = racer.add_bet(
                    self.bet.get_value(), self._balance.money
                )
                lbl.money = displaybet

                if value != 0:
                    self._balance.money = self._balance.money - value

                # print(racer.bet, value)
                # lbl.set_value(input("value: "))
                # print(racer.index)

            racer.show_name(self._win, "down")
            racer.standby_run()
            racer.draw(self._win)
            lbl.draw(self._win)

        self._balance.draw(self._win)
        # self.balance.update(self.events)
        self.bet.draw(self._win)
        self.bet.update(self._events)

        self.race_btn.update(self._events)
        self.race_btn.draw(self._win)

        self.back_btn.update(self._events)
        self.back_btn.draw(self._win)

    def loop_settings(self):
        self._win.blit(self._bk, (0, 0))
        # self.win.blit(self._font.render("NOT READY YET", True, colors["red"]), (self.width//2-100, self.height//2-100))
        self.back_btn.draw(self._win)
        self.back_btn.update(self._events)

        for event in self._events:
            if event.type == MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for e in self._option_selectors:
                    if e.get_rect().collidepoint(pos) == True:
                        e.select(True)
                    else:
                        e.select(False)

        for e in self._option_selectors:
            e.draw(self._win)
            if e.is_selected():
                e.update(self._events)

    def loop_race(self):
        border = self._finish.get_rect()
        border.x, border.y = (self._width - 120, 0)
        font = pygame.font.Font("assets/Minecraft.ttf", 50)
        font.set_bold(True)
        font.set_italic(True)

        self._win.blit(self._bk, (0, 0))
        self._win.blit(self._finish, border)
        self._balance.draw(self._win)
        self.back_btn.draw(self._win)
        self.back_btn.update(self._events)

        if len(self._clasament) == 4:
            self.set_state("leaderboard")
            pygame.time.delay(800)

        for i in range(len(self._race_sprites)):
            self._win.blit(self._drum, (self._width // 9, (i + 1) * self._height // 5))
            self._win.blit(
                pygame.font.Font("assets/Minecraft.ttf", 30).render(
                    f"{self._race_sprites[i].bet}$", True, COLORS["green"]
                ),
                (self._width // 9, (i + 1) * self._height // 5 - 50),
            )
            self._race_sprites[i].update()
            self._race_sprites[i].draw(self._win)
            self._race_sprites[i].show_name(self._win, "mid")

            if (
                self._race_sprites[i].rect.colliderect(border) == True
                and self._race_sprites[i].place == 0
            ):  # daca o terminat race-ul
                # print("finished")
                self._race_sprites[i].time = round(
                    (self._race_sprites[i].time - self._race_sprites[i].tzero), 2
                )
                self._clasament.append(self._race_sprites[i])
                self._race_sprites[i].place = len(self._clasament)

            self._race_sprites[i].show_place(self._win, font)

    def loop_leaderboard(self):
        racer_image = self._racer_attr["images"][len(self._racer_attr["images"]) - 1]
        racer_image = scale(racer_image, (180, 180))
        racer_rect = racer_image.get_rect()
        # racers = self.clasament
        font = pygame.font.Font("assets/Minecraft.ttf", 35)
        font.set_underline(True)
        font.set_bold(True)

        self._win.blit(self._bk, (0, 0))

        self._balance.draw(self._win)
        self.leaderboard_widgets[0].draw(self._win)  # label leaderboard
        self.leaderboard_widgets[1].draw(self._win)  # label status
        self.leaderboard_widgets[2].draw(self._win)  # button menu
        self.leaderboard_widgets[2].update(self._events)
        self.back_btn.draw(self._win)
        self.back_btn.update(self._events)
        for j in range(len(self._clasament)):
            i = len(self._clasament) - j - 1
            racer = self._clasament[i]
            x_raft, y_raft = (
                (j + 1) * (self._width // 6),
                (self._height - (j + 1) * (self._height // 7) - 150),
            )
            self._win.blit(self._raft, (x_raft, y_raft))
            # self._raft.get_rect()
            racer_rect.center = (x_raft + 50, y_raft - 40)

            self._win.blit(racer_image, racer_rect)
            self._win.blit(
                font.render(
                    f"{racer.display_name}: {self._clasament[i].time}s",
                    True,
                    COLORS["green"],
                ),
                (x_raft + 100, y_raft - 10),
            )
            self._win.blit(
                self._font.render(str(racer.place), True, COLORS["green"]),
                (x_raft - 50, y_raft - 10),
            )
            # print(self.clasament[i].display_name)

    def loop_about(self):
        self._win.blit(self._bk, (0, 0))
        self._win.blit(
            self._font.render("A simple racing game. Have fun!", True, COLORS["green"]),
            (self._width // 2 - 400, self._height // 2 - 200),
        )

        self.back_btn.draw(self._win)
        self.back_btn.update(self._events)

    def handle_events(self):
        # an event handler
        self._events = pygame.event.get()
        for event in self._events:
            if event.type == pygame.QUIT:
                self._run = False
                self._balance.write_money()

            elif event.type == pygame.VIDEORESIZE:
                pass

    def main_loop(self):
        # STATES = ["main_menu", "settings", "bet_screen", "race", "leaderboard", "about"]
        while self._run:
            self._clock.tick(self._fps)
            self.handle_events()

            if self._game_state == "main_menu":
                self.loop_menu()

            elif self._game_state == "settings":
                self.loop_settings()

            elif self._game_state == "bet_screen":
                self.loop_bet_screen()

            elif self._game_state == "race":
                self.loop_race()

            elif self._game_state == "about":
                self.loop_about()

            elif self._game_state == "leaderboard":
                self.loop_leaderboard()

            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    app = Game(1280, 720, 144)
    app.main_loop()
