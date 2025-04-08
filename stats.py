import os
import pandas as pd
import matplotlib.pyplot as plt

class GameStats:
    def __init__(self, result_file="data/game_history.csv"):
        self.result_file = result_file
        self.data = []

    def record_move(self, player, move):
        self.data.append({"player": player, "move": move})

    def record_result(self, winner):
        self.data.append({"player": winner, "result": "win"})

    def save_game(self):
        df = pd.DataFrame(self.data)
        try:
            move_file = "data/games_stats.csv"
            if os.path.exists(move_file):
                df.to_csv(move_file, mode="a", header=False, index=False)
            else:
                df.to_csv(move_file, index=False)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")

    def show_stats(self):
        if not os.path.exists(self.result_file):
            print("❌ Le fichier game_history.csv n'existe pas.")
            return

        try:
            df = pd.read_csv(self.result_file, encoding="utf-8-sig")
        except Exception as e:
            print("❌ Erreur de lecture du fichier :", e)
            return

        df.columns = df.columns.str.strip().str.lower()

        if not {"turn", "start", "end", "player", "captured piece"}.issubset(df.columns):
            print("❌ Colonnes manquantes dans game_history.csv")
            return

        df["move"] = df.apply(lambda row: f"{row['start']}->{row['end']}" if pd.notna(row['start']) and pd.notna(row['end']) else None, axis=1)

        moves_df = df[df["turn"].apply(lambda x: str(x).isdigit()) & df["move"].notna()].copy()
        moves_df["turn"] = moves_df["turn"].astype(int)

        # Découper les parties par quartiles pour savoir où se trouve un tour dans la partie
        def phase_label(turn, max_turn):
            if turn <= max_turn * 0.33:
                return "Début"
            elif turn <= max_turn * 0.66:
                return "Milieu"
            else:
                return "Fin"

        result_rows = df[df["turn"].str.lower() == "résultat"]
        winners = result_rows["captured piece"].value_counts()

        # Graphique 1 : Coups les plus joués
        move_counts = moves_df["move"].value_counts().head(10)

        # Définir les phases de jeu
        game_ids = df[df["turn"].str.contains("---debut-partie", na=False)].index.tolist()
        end_ids = df[df["turn"].str.contains("---fin-partie", na=False)].index.tolist()

        phases = []
        turn_by_game = []
        for game_number, (start_idx, end_idx) in enumerate(zip(game_ids, end_ids), 1):
            game = df.iloc[start_idx + 1:end_idx]
            game_moves = game[game["turn"].apply(lambda x: str(x).isdigit())].copy()
            game_moves["turn"] = game_moves["turn"].astype(int)
            max_turn = game_moves["turn"].max()
            game_moves["phase"] = game_moves["turn"].apply(lambda x: phase_label(x, max_turn))
            game_moves["move"] = game_moves.apply(lambda row: f"{row['start']}->{row['end']}" if pd.notna(row['start']) and pd.notna(row['end']) else None, axis=1)
            game_moves["winner"] = df.loc[end_idx - 1, "captured piece"]
            phases.append(game_moves)
            turn_by_game.append({"game_id": game_number, "turns": max_turn})

        phase_df = pd.concat(phases)
        turn_df = pd.DataFrame(turn_by_game)

        # Graphique 2 : Coups les plus joués par phase
        phase_counts = phase_df.groupby(["phase", "move"]).size().unstack(fill_value=0)
        phase_counts = phase_counts.T.apply(lambda x: x.sort_values(ascending=False).head(3))

        # Graphique 3 : Coups menant à la victoire par phase
        win_moves = phase_df.copy()
        win_moves = win_moves[win_moves["player"] == "N"]  # Suppose que N est IA gagnante
        win_moves = win_moves[win_moves["winner"] == "IA"]
        win_effectiveness = win_moves.groupby(["phase", "move"]).size().unstack(fill_value=0)
        win_effectiveness = win_effectiveness.T.apply(lambda x: x.sort_values(ascending=False).head(3))

        # Affichage des graphiques
        fig, axs = plt.subplots(3, 2, figsize=(14, 14))

        winners.plot(kind="bar", ax=axs[0][0], title="Victoires par camp", color="skyblue")
        axs[0][0].set_ylabel("Nombre de victoires")
        axs[0][0].set_xlabel("Camp gagnant")

        move_counts.plot(kind="barh", ax=axs[0][1], title="Top 10 des coups les plus joués", color="lightgreen")
        axs[0][1].set_xlabel("Fréquence")
        axs[0][1].invert_yaxis()

        phase_counts.plot(kind="barh", ax=axs[1][0], title="Top 3 coups par phase (fréquence)")
        axs[1][0].set_xlabel("Fréquence")
        axs[1][0].invert_yaxis()

        win_effectiveness.plot(kind="barh", ax=axs[1][1], title="Top 3 coups gagnants par phase")
        axs[1][1].set_xlabel("Fréquence de victoire")
        axs[1][1].invert_yaxis()

        # Graphique 5 : Nombre de tours par partie
        axs[2][0].plot(turn_df["game_id"], turn_df["turns"], marker="o", linestyle="-", color="purple")
        axs[2][0].set_title("Nombre de tours par partie")
        axs[2][0].set_xlabel("ID Partie")
        axs[2][0].set_ylabel("Nombre de tours")

        axs[2][1].axis("off") 
        plt.tight_layout()
        plt.show()