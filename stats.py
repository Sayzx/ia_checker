import pandas as pd
import matplotlib.pyplot as plt

class GameStats:
    def __init__(self, file_path="data/games_history.xlsx"):
        self.file_path = file_path
        self.data = []

    def record_move(self, player, move):
        self.data.append({"player": player, "move": move})

    def save_game(self):
        """Sauvegarde les parties dans un fichier Excel"""
        df = pd.DataFrame(self.data)
        df.to_excel(self.file_path, index=False, mode='a', header=False)

def show_stats():
    """Affiche les statistiques de jeu"""
    try:
        df = pd.read_excel("data/games_history.xlsx")
        moves_count = df["move"].value_counts()
        moves_count[:10].plot(kind='bar', title="Top 10 mouvements")
        plt.show()
    except Exception as e:
        print(f"Erreur lors du chargement des statistiques: {e}")