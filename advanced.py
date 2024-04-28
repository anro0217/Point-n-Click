import datetime
import time
import tkinter as tk
from random import *
from tkinter import *
from tkinter import ttk

from onbezaroMenu import main

COLOR = ""
TIME = 60
SCORE = 0
LEVEL = ""
NAME = ""
DATE = str(datetime.date.today())
MIN = 100
MAX = 150
DELAY = 1000

""" # Constants:
COLOR_OPTIONS = [
    "red",
    "green",
    "blue",
    "yellow",
    "purple",
    "orange",
    "pink",
    "black",
    "brown",
    "grey",
] """
COLOR_OPTIONS = ["red", "green", "blue", "yellow", "purple", "orange", "random"]
DIFFICULTY_LEVELS = ["tutorial", "easy", "normal", "hard", "painful", "impossible"]

root = tk.Tk()
root.attributes("-fullscreen", True)
root.title("Point'n Click")
root.geometry("1920x1080")


def start_page():

    label = tk.Label(root, text="Point'n Click\nThe Game", font=("Arial", 30))
    label.pack()

    player_name_box = tk.Label(root, text="Enter your player name:", width=20)
    player_name_var = tk.Entry(root)
    player_name_box.pack()
    player_name_var.pack()

    difficulty_level_var = StringVar(root)
    difficulty_level_var.set("Choose the difficulty")
    difficulty_level_dropdown = OptionMenu(root, difficulty_level_var, *DIFFICULTY_LEVELS)
    difficulty_level_dropdown.pack()

    color_to_search_var = StringVar(root)
    color_to_search_var.set("Choose the color")
    color_to_search_dropdown = OptionMenu(root, color_to_search_var, *COLOR_OPTIONS)
    color_to_search_dropdown.pack()

    total_time_box = tk.Label(root, text="Enter the time in seconds:", width=20)
    total_time_var = tk.Entry(root)
    total_time_box.pack()
    total_time_var.pack()

    start_btn = tk.Button(
        root,
        text="Start Game",
        width=15,
        command=lambda: startButton(
            difficulty_level_var, total_time_var, player_name_var, color_to_search_var
        ),
    )
    start_btn.pack()

    # Vissza gomb
    backButton = tk.Button(root, text="Back", width=10, command=lambda: back())
    backButton.pack()

    # Kilépés gomb
    closeButton = tk.Button(root, text="Close", width=10, command=exit)
    closeButton.pack()


def startButton(difficulty_level_var, total_time_var, player_name_var, color_to_search_var):
    global LEVEL
    global TIME
    global NAME
    global MIN
    global MAX
    global DELAY
    LEVEL = difficulty_level_var.get()
    try:
        TIME = int(total_time_var.get())
    except:
        pass
    finally:
        NAME = player_name_var.get()
        global COLOR
        COLOR = color_to_search_var.get()
        while COLOR == "random":
            COLOR = choice(COLOR_OPTIONS)

        if LEVEL == "tutorial":
            MIN = 160
            MAX = 320
        elif LEVEL == "easy":
            MIN = 80
            MAX = 160
            DELAY = 800
        elif LEVEL == "medium":
            MIN = 40
            MAX = 80
            DELAY = 600
        elif LEVEL == "hard":
            MIN = 20
            MAX = 40
            DELAY = 400
        elif LEVEL == "painful":
            MIN = 10
            MAX = 20
            DELAY = 200
        elif LEVEL == "impossible":
            MIN = 40
            MAX = 60
            DELAY = 50
        else:
            LEVEL = "tutorial"

        start_game()


def start_game():
    global TIME
    global COLOR

    for widget in root.winfo_children():
        widget.destroy()

    canvas = Canvas(root, width=1500, height=700)
    canvas.pack()

    score_label = tk.Label(root, text="Score: 0")
    score_label.pack()

    timer_label = tk.Label(root, text="Time left: " + str(TIME))
    timer_label.pack()
    timer(TIME, timer_label)

    color_label = tk.Label(root, text="\n" + COLOR.capitalize())
    color_label.pack()

    create_circle(canvas, score_label)


def create_circle(canvas, score_label):
    global COLOR

    try:
        if len(canvas.find_all()) > 10:
            canvas.delete(choice(canvas.find_all()))
    except:
        pass
        # print("Hiba észlelve")
    else:
        random_color = choice(COLOR_OPTIONS)
        while random_color == "random":
            random_color = choice(COLOR_OPTIONS)

        random_size = randint(MIN, MAX)

        random_position_x = randint(0 + random_size, 1500 - random_size)
        random_position_y = randint(0 + random_size, 700 - random_size)

        circle = canvas.create_oval(
            random_position_x,
            random_position_y,
            random_position_x + random_size,
            random_position_y + random_size,
            fill=random_color,
        )

        if random_color == COLOR:
            canvas.tag_bind(
                circle, "<Button-1>", lambda event: check_if_correct(canvas, circle, score_label)
            )
        else:
            canvas.tag_bind(
                circle, "<Button-1>", lambda event: check_if_wrong(canvas, circle, score_label)
            )

        root.after(DELAY, create_circle, canvas, score_label)


def check_if_correct(canvas, circle, score_label):

    global SCORE
    SCORE += 1

    score_label.config(text="Score: " + str(SCORE))

    canvas.delete(circle)


def check_if_wrong(canvas, circle, score_label):

    global SCORE
    SCORE -= 1

    score_label.config(text="Score: " + str(SCORE))

    canvas.delete(circle)


def timer(time_left, timer_label):

    timer_label.config(text="Time left: " + str(time_left))

    if time_left > 0:

        root.after(1000, timer, time_left - 1, timer_label)
    else:

        time_is_over()


def time_is_over():
    global SCORE
    global NAME
    global DATE
    global LEVEL

    for widget in root.winfo_children():
        widget.destroy()

    with open("scores2.txt", "a") as scores_file:
        scores_file.write(str(SCORE) + "," + DATE + "," + LEVEL + "," + NAME + "\n")

    other_label = tk.Label(root, text="High Scores", font=("Arial", 30)).grid(row=0, columnspan=3)

    cols = ("Position", "Name", "Score", "Level", "Date")
    listBox = ttk.Treeview(root, columns=cols, show="headings")
    listBox.HorizontalScrollBar = True  # Ha betelik a scoreboard, a görgővel lehet tekerni

    for col in cols:
        listBox.heading(col, text=col)
    listBox.grid(row=1, column=0, columnspan=2)

    showScores = tk.Button(root, text="Show scores", command=show(listBox))
    newButton = tk.Button(root, text="New Game", width=15, command=again).grid(row=4, column=0)
    backButton = tk.Button(root, text="Menu", width=15, command=lambda: back()).grid(
        row=4, column=1
    )
    closeButton = tk.Button(root, text="Close", width=10, command=exit).grid(row=5, column=1)


def show(listBox):
    lines = []
    with open("scores2.txt", "r") as scores_file:
        for line in scores_file:
            lines.append(line.split(",", 3))

    lines.sort(key=lambda e: e[2])

    for i, (score, date, level, name) in enumerate(lines, start=1):
        listBox.insert(
            "",
            "end",
            values=(i, name, score, level, date),
        )


def again():
    """
    Újraindítás
    """
    # értékek resetelése
    global TOTAL_TIME
    global TIME
    global SCORE
    global LEVEL
    global NAME

    TOTAL_TIME = 0
    TIME = 60
    SCORE = 0
    LEVEL = ""
    NAME = ""

    # Játék vége ablak törlése
    for widget in root.winfo_children():
        widget.destroy()

    # Ablak létrehozása, beállítása
    root.attributes("-fullscreen", True)
    root.title("Point'n Click")
    root.geometry("1920x1080")

    start_page()
    root.mainloop()


def back():
    """
    Visszalépés
    """
    main()
    root.destroy()


start_page()
root.mainloop()
