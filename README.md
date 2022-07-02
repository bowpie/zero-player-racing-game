# Race And Win - Zero Player Racing Game

> #### A simple game in which you can bet on 4 different characters who race to the finish line. This game was made using `pygame` and `pygame_menu`.

## **Description**

---

The game is structured on 6 main views: ["main_menu", "settings", "bet_screen", "race", "leaderboard", "about"].
It has a money management system and customizable racer avatars. These changes can be made inside `properties.json`.

### How to play?

![Menu](/screenshots/mainmenu.PNG)

The main menu consists of 4 buttons which you can directly click or move up and down with arrows.
You have `Play, About, Options, Quit`. If you want to customize either the speed or the current avatar for the racer you can to so in the `Options` part.

![Options](/screenshots/options.PNG)

After you click on the play button, you will be shown a `betting screen`. To bet, enter the amount in the `Bet: ` input and then click on a racer. Betting can be stacked and if you want to subtract money from a racer you can do so if you put the `-` symbol before the betting amount.

![BetScreen](/screenshots/betscreen.PNG)

Then, if you are ready, click on the `race` button. A countdown will start and then it will start the race.

![Race](/screenshots/race.PNG)

After the race is finished a `leaderboard` will be shown with the place and time of each racer + the amount you have won or lost this time.

![Leaderboard](/screenshots/leaderboard.PNG)

The speed of each racer is randomly generated using a true random function: `random.SystemRandom()`. The speed changes multiple times during the race and is not predetermined at the start, making it impossible to know which racer wins at the end.

## **Getting started**

---

### Dependencies

- The following Python 3.8.4 modules: pygame, pygame_menu, json, time, random

```
pip install -r requirements.txt
```

### Executing the program

```
py ./Game.py
```

## **License**

---

This project is licensed under the MIT License - see the LICENSE.md file for details.
