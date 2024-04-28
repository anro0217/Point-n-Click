import tkinter as tk


def main():
    program_selected = ""

    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.title("Game Selector")
    root.geometry("1920x1080")

    label = tk.Label(root, text="Select a game:")
    label.pack()

    start_game1_button = tk.Button(
        root, text="Point'n Click - Version 1", command=lambda: start_game1(root)
    )
    start_game1_button.pack()

    start_game2_button = tk.Button(
        root, text="Point'n Click - Version 2", command=lambda: start_game2(root)
    )
    start_game2_button.pack()

    closeButton = tk.Button(root, text="Close", width=15, command=exit)
    closeButton.pack()

    root.mainloop()


def start_game1(root):
    global program_selected
    program_selected = "game1"
    start_game()
    root.destroy()


def start_game2(root):
    global program_selected
    program_selected = "game2"
    start_game()
    root.destroy()


def start_game():
    if program_selected == "game1":
        import simple
    elif program_selected == "game2":
        import advanced

    # TODO:
    # A két játék végén, ha a scoreboardból a menübe lépünk, onnan nem választható ki a másik játék


if __name__ == "__main__":
    main()
