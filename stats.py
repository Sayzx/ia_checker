import os
import pandas as pd
import matplotlib.pyplot as plt

class GameStats:
    def __init__(self, file_path="data/games_stats.xlsx"):
        self.file_path = file_path
        self.data = []
        
        # Créer le dossier data s'il n'existe pas
        if not os.path.exists("data"):
            os.makedirs("data")

    def record_move(self, player, move):
        self.data.append({"player": player, "move": move})

    def save_game(self):
        """Sauvegarde les parties dans un fichier Excel"""
        df = pd.DataFrame(self.data)

        # Sauvegarder dans le fichier
        if os.path.exists(self.file_path):
            with pd.ExcelWriter(self.file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                df.to_excel(writer, index=False, header=False)
        else:
            df.to_excel(self.file_path, index=False)

def show_stats():
    """Affiche les statistiques de jeu"""
    try:
        df = pd.read_excel("data/games_history.xlsx")
        moves_count = df["move"].value_counts()
        moves_count[:10].plot(kind='bar', title="Top 10 mouvements")
        plt.show()
    except Exception as e:
        print(f"Erreur lors du chargement des statistiques: {e}")

def calculate_global_stats():
    """Calcule les statistiques globales des parties"""
    try:
        df = pd.read_excel("data/game_history.xlsx")
        player_wins = df.groupby("Player")["Turn"].count()
        print("Statistiques globales :")
        print(player_wins)
    except Exception as e:
        print(f"Erreur lors du calcul des statistiques : {e}")