from tkinter import Tk, Button, Frame, Label
from game import Game
from stats import GameStats
from replay_visual import select_game_to_replay
from iaversus import start_ia_vs_ia 


def start_game():
    def launch():
        game_root = Tk()
        Game(game_root, restart_callback=launch)
        game_root.mainloop()
    launch()

def show_menu():
    root = Tk()
    root.title("Menu Principal")
    root.attributes('-fullscreen', True)
    root.configure(bg="#1e1e1e")

    container = Frame(root, bg="#1e1e1e")
    container.pack(expand=True)

    title_label = Label(
        container, text="JEU DE DAMES", font=("Helvetica", 48, "bold"), fg="white", bg="#1e1e1e"
    )
    title_label.pack(pady=(0, 40))

    button_style = {
        "font": ("Helvetica", 24),
        "bg": "#444", "fg": "white", "activebackground": "#666",
        "padx": 40, "pady": 20, "bd": 0, "relief": "flat",
        "width": 20
    }

    Button(container, text="Jouer", command=lambda: [root.destroy(), start_game()], **button_style).pack(pady=20)
    Button(container, text="IA vs IA", command=lambda: [root.destroy(), start_ia_vs_ia()], **button_style).pack(pady=20)
    Button(container, text="Voir les statistiques", command=lambda: GameStats().show_stats(), **button_style).pack(pady=20)
    Button(container, text="Rejouer une partie", command=lambda: [root.destroy(), select_game_to_replay()], **button_style).pack(pady=20)
    Button(container, text="Quitter", command=root.quit, **button_style).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    show_menu()
