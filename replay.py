import pandas as pd
import time

class GameReplay:
    def __init__(self, file_path="data/games_history.xlsx"):
        self.file_path = file_path

    def replay_last_game(self):
        """Rejoue la dernière partie enregistrée"""
        try:
            df = pd.read_excel(self.file_path)
            for index, row in df.iterrows():
                print(f"{row['player']} a joué {row['move']}")
                time.sleep(1)
        except Exception as e:
            print(f"Erreur : {e}")