import random
import pygame
import time
from Constants import COLORS


class Racer(pygame.sprite.Sprite):
    """
    Base class for racer characters
    """

    def __init__(
        self,
        width,
        height,
        x,
        y,
        index,
        display_font,
        name="",
        images=[],
        racer_speed="slow",
        racer_type="default",
    ) -> None:
        pygame.sprite.Sprite.__init__(self)
        self._width, self._height = (width, height)
        self._index = index  # number in race
        self._racer_type = racer_type
        self._racer_speed = racer_speed
        self._display_name = name
        # bet
        self._bet = 0
        # animation
        self._images = images
        self._current_image = 0
        self._image = self._images[int(self._current_image)]
        # control
        self._rect = self._image.get_rect()
        self._rect.centerx, self._rect.centery = x, y
        # etc
        self._display_font = display_font
        self._current_speed = 0
        self._place = 0
        # setting speed range
        self.set_range()

    def prepare_race(self):
        # we start the race timer
        self.set_speed(self._speed_range)
        self.tzero = time.time()
        self.time = time.time()

    def add_bet(self, value, money):
        # check if the bet is valid
        try:
            value = int(value)
            if (
                value >= 999999
                or (money - value < 0)
                or (value < 0 and self._bet + value < 0)
            ):
                raise ValueError

        except ValueError:
            value = 0

        self._bet += value

        if self._bet < 0:
            self._bet = 0
        elif self._bet > 999999:
            self._bet = 999999

        return (self._bet, value)

    @property
    def display_name(self):
        return self._display_name

    @property
    def index(self):
        # print("getting index")
        return self._index

    @property
    def bet(self):
        return self._bet

    @property
    def rect(self):
        return self._rect

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, value):
        self._place = value

    def set_speed(self, speed: tuple):
        # set a random speed in a range
        self._current_speed = (
            random.SystemRandom().randint(max(1, speed[0]), max(2, speed[1]))
            + random.SystemRandom().random()
        )

    def set_pos(self, x, y):
        # we set the racer's position
        self._rect.centerx = x
        self._rect.centery = y

    def set_range(self):
        if self._racer_speed == "slow":
            self._speed_range = (1, 5)
        elif self._racer_speed == "medium":
            self._speed_range = (5, 10)
        elif self._racer_speed == "fast":
            self._speed_range = (10, 15)
        elif self._racer_speed == "ultrasonic":
            self._speed_range = (15, 20)

    def set_curentimage(self):
        # basic running animation
        if (time.time() - self.time) > 2 / self._current_speed:
            self.set_speed((self._speed_range[0] - 2, self._speed_range[1] - 2))
            self.time = time.time()

        self._current_image += self._current_speed / 60

        if self._current_image >= len(self._images):
            self._current_image = 0

        self._image = self._images[int(self._current_image)]

    def standby_run(self):
        # standby animation
        self._current_image += 4 / 60
        if self._current_image >= len(self._images):
            self._current_image = 0

        self._image = self._images[int(self._current_image)]

    def is_clicked(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if self._rect.collidepoint(pos):
                    return True
        return False

    def update(self):
        if self._place == 0:  # has not finished yet
            self.set_curentimage()
            self._rect.centerx += self._current_speed
        else:
            self._image = self._images[0]

    def draw(self, surface):  # draw the image
        surface.blit(self._image, self._rect)

    def show_name(self, surface, pos):
        assert pos in ["down", "mid"]
        if pos == "down":
            surface.blit(
                self._display_font.render(self._display_name, True, COLORS["green"]),
                (
                    self._rect.centerx - self._width // 4,
                    self._rect.centery + self._height // 2,
                ),
            )
        elif pos == "mid":
            surface.blit(
                self._display_font.render(self._display_name, True, COLORS["white"]),
                (self._rect.centerx - self._width // 4, self._rect.centery - 10),
            )

    def show_place(self, surface, font):
        if self._place != 0:
            surface.blit(
                font.render(str(self._place), True, COLORS["green"]),
                (self._rect.centerx + self._width - 20, self._rect.centery),
            )
