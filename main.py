from tkinter import Tk, Button
from game import Game
from stats import show_stats
from replay import GameReplay

def start_game():
    game_root = Tk()
    game = Game(game_root)
    game_root.mainloop()

def show_menu():
    root = Tk()
    root.title("Menu Principal")

    Button(root, text="Jouer", command=lambda: [root.destroy(), start_game()]).pack(pady=10)
    Button(root, text="Voir les stats", command=show_stats).pack(pady=10)
    Button(root, text="Rejouer", command=lambda: GameReplay().replay_last_game()).pack(pady=10)
    Button(root, text="Quitter", command=root.quit).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    show_menu()