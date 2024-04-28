import datetime
import time
import tkinter as tk
from random import *
from tkinter import ttk

from onbezaroMenu import main

# Globális változók
TOTAL_TIME = 0
TIME = 60
SCORE = 0
LEVEL = ""
NAME = ""
DATE = str(datetime.date.today())

""" 
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
COLOR_OPTIONS = ["red", "green", "blue", "yellow", "purple", "orange"]
DIFFICULTY_LEVELS = ["tutorial", "easy", "normal", "hard", "painful"]

# Ablak létrehozása, beállítása
root = tk.Tk()
root.attributes("-fullscreen", True)
root.title("Point'n Click")
root.geometry("1920x1080")


def start_page():
    """
    Start oldal
    """
    # Cím
    label = tk.Label(root, text="Point'n Click\nThe Game", font=("Arial", 30))
    label.pack()

    # A játékosnév megadásának szövegdoboza
    player_name_box = tk.Label(root, text="Enter your player name:", width=20)
    player_name_var = tk.Entry(root)
    player_name_box.pack()
    player_name_var.pack()

    # Lenyitható menü a nehézségi szinthez
    difficulty_level_var = tk.StringVar(root)
    difficulty_level_var.set("Choose the difficulty")
    difficulty_level_dropdown = tk.OptionMenu(root, difficulty_level_var, *DIFFICULTY_LEVELS)
    difficulty_level_dropdown.pack()

    # Idő megadása szövegboxban
    total_time_box = tk.Label(root, text="Enter the time in seconds:", width=20)
    total_time_var = tk.Entry(root)
    total_time_box.pack()
    total_time_var.pack()

    # Start gomb észlelése
    start_btn = tk.Button(
        root,
        text="Start Game",
        width=15,
        command=lambda: startButton(difficulty_level_var, total_time_var, player_name_var),
    )
    start_btn.pack()

    # Vissza gomb
    backButton = tk.Button(root, text="Back", width=10, command=lambda: back())
    backButton.pack()

    # Kilépés gomb
    closeButton = tk.Button(root, text="Close", width=10, command=exit)
    closeButton.pack()


def startButton(difficulty_level_var, total_time_var, player_name_var):
    """
    Start gomb
    """
    global LEVEL
    LEVEL = difficulty_level_var.get()
    global TIME
    try:
        TIME = int(total_time_var.get())
    except:
        pass
    finally:
        global TOTAL_TIME
        TOTAL_TIME = total_time_var.get() + " seconds"
        global NAME
        NAME = player_name_var.get()
        start_game()


def start_game():
    """
    A játék indítása
    """
    # A start oldal törlése
    for widget in root.winfo_children():
        widget.destroy()

    # Játéktér létrehozása (vászon)
    canvas = tk.Canvas(root, width=1500, height=700)
    canvas.pack()

    # A pontszám kiiratása
    score_label = tk.Label(root, text="Score: 0")
    score_label.pack()

    # Az idő kiiratása
    global TIME
    timer_label = tk.Label(root, text="Time left: " + str(TIME))
    timer_label.pack()
    timer(TIME, timer_label)

    # Kör készítése

    create_circle(canvas, score_label)


def create_circle(canvas, score_label):
    global LEVEL
    # Random kör tulajdonságok
    random_color = choice(COLOR_OPTIONS)
    random_size = 200

    if LEVEL == "tutorial":
        random_size = randint(160, 320)
    elif LEVEL == "easy":
        random_size = randint(80, 160)
    elif LEVEL == "normal":
        random_size = randint(40, 80)
    elif LEVEL == "hard":
        random_size = randint(20, 40)
    elif LEVEL == "painful":
        random_size = randint(10, 20)
    else:
        LEVEL = "not picked"  # alapértelmezett, ha nem választunk a listából
        random_size = randint(160, 320)

    random_position_x = randint(0 + random_size, 1500 - random_size)
    random_position_y = randint(0 + random_size, 700 - random_size)

    # Kör létrehozása
    circle = canvas.create_oval(
        random_position_x,
        random_position_y,
        random_position_x + random_size,
        random_position_y + random_size,
        fill=random_color,
    )

    # A körre kattintás észlelése
    canvas.tag_bind(
        circle, "<Button-1>", lambda event: destroyAndScore(canvas, circle, score_label)
    )


def destroyAndScore(canvas, circle, score_label):
    """
    Pontozás, és körök törlése
    """
    global SCORE
    SCORE += 1

    # Pontszám kiiratása
    score_label.config(text="Score: " + str(SCORE))

    # Kör törlése
    canvas.delete(circle)

    # Új kör
    create_circle(canvas, score_label)


def timer(time_left, timer_label):
    """
    Visszaszámláló
    """
    # Az idő kiiratás frissítése
    timer_label.config(text="Time left: " + str(time_left))

    # Check if the time is over
    if time_left > 0:
        # Az idő csökkentése
        root.after(1000, timer, time_left - 1, timer_label)
    else:
        # Váltás a Játék vége képernyőre
        time_is_over()


def time_is_over():
    """
    A játék vége
    """
    global SCORE
    global NAME
    global DATE
    global LEVEL
    global TOTAL_TIME

    # A játékos tér törlése
    for widget in root.winfo_children():
        widget.destroy()

    # Értékek eltárolása
    with open("scores.txt", "a") as scores_file:
        scores_file.write(
            str(SCORE) + "," + DATE + "," + LEVEL + "," + TOTAL_TIME + "," + NAME + "\n"
        )

    other_label = tk.Label(root, text="High Scores", font=("Arial", 30)).grid(row=0, columnspan=3)
    # fejlécek
    cols = ("Position", "Name", "Score", "Level", "Time", "Date")
    listBox = ttk.Treeview(root, columns=cols, show="headings")
    listBox.HorizontalScrollBar = True  # Ha betelik a scoreboard, a görgővel lehet tekerni

    for col in cols:
        listBox.heading(col, text=col)
    listBox.grid(row=1, column=0, columnspan=2)

    """a show score gomb nincs megjelenítve, nem is lenne funkciója, de ha nincs 
       létrehozva, akkor néha nem jelenik meg a scoreboard....!!TODO!!"""
    showScores = tk.Button(root, text="Show scores", command=show(listBox))
    newButton = tk.Button(root, text="New Game", width=15, command=again).grid(row=4, column=0)
    backButton = tk.Button(root, text="Menu", width=15, command=lambda: back()).grid(
        row=4, column=1
    )
    closeButton = tk.Button(root, text="Close", width=10, command=exit).grid(row=5, column=1)


def show(listBox):
    """
    Az új és régi eredmények rendezése
    """
    lines = []
    with open("scores.txt", "r") as scores_file:
        for line in scores_file:
            lines.append(line.split(",", 4))

    lines.sort(key=lambda e: e[2])

    for i, (score, date, level, time, name) in enumerate(lines, start=1):
        listBox.insert(
            "",
            "end",
            values=(i, name, score, level, time, date),
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
