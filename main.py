import tkinter as tk
import os

def run_game():
    os.system('python src/game.py')

def run_server_game():
    os.system('start cmd /k python src/server.py & python src/game.py')

# Create the main window
root = tk.Tk()
root.title("Игра")

# Button for "Я игрок"
player_button = tk.Button(root, text="Я игрок", command=run_game)
player_button.pack()

# Button for "Я сервер"
server_button = tk.Button(root, text="Я сервер", command=run_server_game)
server_button.pack()

# Start the Tkinter main loop
root.mainloop()
