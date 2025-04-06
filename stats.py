import os
import pandas as pd
import matplotlib.pyplot as plt

class GameStats:
    def __init__(self, move_file="data/games_stats.csv", result_file="data/game_history.csv"):
        self.move_file = move_file
        self.result_file = result_file
        self.data = []

    def record_move(self, player, move):
        self.data.append({"player": player, "move": move})

    def record_result(self, winner):
        self.data.append({"player": winner, "result": "win"})


    def save_game(self):
        df = pd.DataFrame(self.data)
        try:
            if os.path.exists(self.move_file):
                df.to_csv(self.move_file, mode="a", header=False, index=False)
            else:
                df.to_csv(self.move_file, index=False)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")


    def show_stats(self):
        df_moves, df_results = None, None

        # Lire les fichiers
        if os.path.exists(self.move_file):
            try:
                df_moves = pd.read_csv(self.move_file)
            except Exception as e:
                print("❌ Erreur lecture coups (.csv):", e)

        if os.path.exists(self.result_file):
            try:
                df_results = pd.read_csv(self.result_file)
            except Exception as e:
                print("❌ Erreur lecture résultats (.csv):", e)

        if df_moves is None and df_results is None:
            print("Aucune donnée disponible pour afficher les statistiques.")
            return

        # Auto-rename des colonnes si elles ne sont pas bonnes
        if df_moves is not None:
            cols = [col.lower() for col in df_moves.columns]
            df_moves.columns = cols
            if "move" not in cols and "start" in cols and "end" in cols:
                df_moves["move"] = df_moves["start"].astype(str) + " → " + df_moves["end"].astype(str)

        if df_results is not None:
            cols = [col.lower() for col in df_results.columns]
            df_results.columns = cols
            if "player" not in cols and "joueur" in cols:
                df_results.rename(columns={"joueur": "player"}, inplace=True)
            if "result" not in cols and "résultat" in cols:
                df_results.rename(columns={"résultat": "result"}, inplace=True)

        # Graphiques
        fig, axs = plt.subplots(1, 2, figsize=(12, 5))

        # Coups les plus joués
        if df_moves is not None and "move" in df_moves.columns:
            move_counts = df_moves["move"].value_counts().head(10)
            move_counts.plot(kind="barh", ax=axs[1], title="Coups les plus joués")
            axs[1].set_xlabel("Fréquence")
            axs[1].invert_yaxis()
        else:
            axs[1].text(0.5, 0.5, "Aucun coup disponible", ha="center")

        # Victoires (à la fin de la partie)
        if df_moves is not None and "player" in df_moves.columns and "result" in df_moves.columns:
            filtered = df_moves[df_moves["result"].notnull()]
            filtered = filtered[filtered["player"].isin(["Joueur", "IA"])]
            win_counts = filtered.groupby("player")["result"].count()
            win_counts.plot(kind="bar", ax=axs[0], title="Victoires par joueur")
            axs[0].set_ylabel("Nombre de victoires")
            axs[0].set_xlabel("Joueur")
        else:
            axs[0].text(0.5, 0.5, "Aucune victoire enregistrée", ha="center")


        plt.tight_layout()
        plt.show()
