> fix le fait quand tu clique sur Nouvelle partie sa renew une nouvelle parite propre

# Projet Python B2 - Jeu de Dames IA vs Joueur

## 🌐 Description
Ce projet consiste à développer un jeu de dames en Python en mode 1v1 (humain vs ordinateur) avec une intelligence artificielle adaptative. Le jeu propose une interface graphique (Tkinter), une sauvegarde automatique des parties, ainsi qu'une analyse statistique poussée à l'aide de `pandas` et `matplotlib`.

## 💻 Fonctionnalités principales
- Jeu de dames complet avec interface graphique
- IA basée sur l'analyse de coups passés
- Mode Humain vs IA
- Mode IA vs IA pour générer de la donnée automatiquement
- Enregistrement de chaque partie dans un fichier CSV
- Visualisation des statistiques de jeu sous forme de graphiques
- Relecture des parties précédentes via un système de replay interactif

## 🔖 Technologies et librairies utilisées
- Python 3
- `tkinter` pour l'interface graphique
- `pandas` pour le traitement de données
- `matplotlib` pour la visualisation statistique
- Programmation orientée objet (POO)

## 🌐 Structure du projet
```
.
├── board.py             # Gestion du plateau de jeu
├── game.py              # Logique du jeu
├── gui.py               # Interface graphique principale
├── ia.py                # Intelligence artificielle
├── iaversus.py          # Mode IA vs IA
├── replay_visual.py     # Relecture des parties
├── stats.py             # Statistiques et visualisations
├── data/
│   ├── game_history.csv     # Historique des parties
│   └── games_stats.csv      # Statistiques de coups
├── main.py              # Menu principal du jeu
└── README.md
```

## 📊 Statistiques générées
- Nombre de victoires par camp
- Coups les plus fréquemment joués
- Coups les plus joués par phase de partie (début, milieu, fin)
- Coups les plus souvent liés à une victoire
- Courbe du nombre de tours joués par partie

## 🧪 Fonctionnement de l'IA
L'intelligence artificielle suit les étapes suivantes :
1. Liste tous les coups possibles
2. Evalue les coups selon des stratégies de base (prise, avancement, position)
3. Consulte les parties précédentes enregistrées dans `game_history.csv`
4. Augmente la valeur d'un coup s'il a historiquement mené à une victoire
5. Sélectionne le coup ayant la meilleure note

## 🎮 Lancer le projet
```bash
python main.py
```

## 💡 Auteurs
Projet réalisé dans le cadre du module "Manipulation de données en Python" - YNOV B2 Informatique.

Encadrant : Nicolas Miotto