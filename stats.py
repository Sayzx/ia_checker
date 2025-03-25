import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class GameStats:
    def __init__(self, file_path="data/games_stats.xlsx"):
        self.file_path = file_path
        self.data = []
        if not os.path.exists("data"):
            os.makedirs("data")

    def record_move(self, player, move):
        self.data.append({"player": player, "move": move})

    def save_game(self):
            df = pd.DataFrame(self.data)
            
            try:
                if os.path.exists(self.file_path):
                    print("Fichier CSV existant, ajout de nouvelles données.")
                    df.to_csv(self.file_path, mode='a', header=False, index=False)
                else:
                    print("Création d'un nouveau fichier CSV.")
                    df.to_csv(self.file_path, index=False)
            except Exception as e:
                print(f"Erreur lors de la sauvegarde : {e}")

def show_stats():
    try:
        df = pd.read_excel("data/games_history.xlsx")
        moves_count = df["move"].value_counts()
        moves_count[:10].plot(kind='bar', title="Top 10 mouvements")
        plt.show()
    except Exception as e:
        print(f"Erreur lors du chargement des statistiques: {e}")

def calculate_global_stats():
    try:
        df = pd.read_excel("data/game_history.xlsx")
        player_wins = df.groupby("Player")["Turn"].count()
        print("Statistiques globales :")
        print(player_wins)
    except Exception as e:
        print(f"Erreur lors du calcul des statistiques : {e}")