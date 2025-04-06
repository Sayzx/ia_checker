import pandas as pd
import time
import os

class GameReplay:
    def __init__(self, file_path="data/game_history.csv"):
        self.file_path = file_path

    def get_last_game_moves(self):
        if not os.path.exists(self.file_path):
            print("❌ Fichier non trouvé :", self.file_path)
            return pd.DataFrame()

        df = pd.read_csv(self.file_path)

        if df.empty:
            print("❌ Le fichier est vide.")
            return pd.DataFrame()

        if "timestamp" not in df.columns:
            print("❌ Colonne 'timestamp' manquante.")
            return pd.DataFrame()

        # Conversion datetime sécurisée
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.dropna(subset=["timestamp"])

        if df.empty:
            print("❌ Aucune ligne avec un timestamp valide.")
            return pd.DataFrame()

        df["game_time"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
        last_game_time = df["game_time"].max()
        return df[df["game_time"] == last_game_time]

    def replay_last_game(self, speed=5):
        moves = self.get_last_game_moves()
        if moves.empty:
            print("❌ Aucune partie trouvée à rejouer.")
            return

        print(f"🎮 Relecture de la partie du {moves['game_time'].iloc[0]}")
        for _, row in moves.iterrows():
            print(f"{row['player']} : {row['start']} → {row['end']} | Capture: {row.get('captured', False)} | Promu: {row.get('promoted', False)}")
            time.sleep(max(0.1, 1.5 - (speed * 0.15)))
