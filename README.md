# finalExam

# TIC-TAC-TOE IA - PROJET DATA-DRIVEN

## Thème
Intelligence Artificielle du jeu Tic-Tac-Toe (morpion) de type *data driven only*.

L'objectif de ce projet est de concevoir une IA capable de jouer au Tic-Tac-Toe, en s'appuyant sur des données existantes et sans codage manuel de règles explicites, tout en intégrant cette IA dans une interface graphique interactive.

---

## Partie I - Dataset

Le dataset utilisé provient de la plateforme Kaggle :  
https://www.kaggle.com/datasets/redsilhouette/tic-tac-toe-synthetic-data?resource=download

Explication du créateur (RedSilhouette) :  
> These datasets were made for my Tic Tac Toe neural network agent. Given a tictactoe board (flattened into a vector represented by a string) my implementations of the algorithms choose the optimal move. For something like minimax, this will be objectively the best move. Running the algorithms themselves can be sometimes time consuming whereas training a neural network agent to make the same moves without exploring options can create a less deterministic but faster agent. I limited my neural network approach but this dataset could easily be used to make better agents.

En résumé, ces données ont été générées à partir d’algorithmes de recherche comme Minimax qui produisent le meilleur coup possible, puis sauvegardées sous forme d’états du plateau et du coup optimal associé. Cela permet d’entraîner un réseau de neurones à reproduire les décisions d’un algorithme parfait, tout en étant plus rapide à exécuter une fois entraîné.

---

## Partie II - Apprentissage

Un modèle de classification a été entraîné sur ce dataset :
- le plateau est encodé en vecteur de 9 positions (X, O, vide)
- la cible est la case choisie (1 à 9)
- l’architecture retenue est un Multi-Layer Perceptron (MLP) avec une sortie softmax
- la perte utilisée est la categorical crossentropy
- entraînement réalisé en Python avec TensorFlow / Keras

Ce modèle apprend ainsi à prédire le **meilleur coup** à jouer pour chaque situation, de manière data-driven.

---

## Partie III - Implémentation

L’implémentation se compose d’une interface graphique réalisée en Python avec Tkinter.  
L’utilisateur peut jouer contre l’IA, qui sélectionne ses coups en s’appuyant sur le modèle entraîné.  

---

## Explication des fichiers

### 1. `tic_tac_toe_records_minimax.csv`
Il s’agit du dataset utilisé pour entraîner le modèle.  
Chaque ligne contient :
- l’état du plateau sous forme de chaîne de 9 caractères (X, O ou vide)
- la case à jouer (1 à 9)  
C’est un jeu de données supervisé basé sur des décisions Minimax, garantissant la qualité optimale des coups.

---

### 2. `mlp_tictactoe.h5`
C’est le modèle entraîné (format TensorFlow/Keras).  
Ce fichier est généré par `train_model.py` et contient :
- la structure du MLP
- les poids appris
Il est chargé au moment de lancer le jeu via `gui.py` et permet à l’IA de prédire le meilleur coup sur un plateau donné.

---

### 3. `preprocessing.py`
Un module Python qui :
- charge le CSV
- convertit les X/O/vides en valeurs numériques (1, -1, 0)
- prépare la cible en labels 0..8 (pour 9 classes)
Il est importé dans `train_model.py` pour garantir un prétraitement cohérent des données.

---

### 4. `train_model.py`
Un module Python qui :
- appelle la fonction de `preprocessing.py` pour charger et préparer le jeu de données
- définit l’architecture MLP
- compile et entraîne le modèle
- sauvegarde le modèle entraîné au format HDF5 (`mlp_tictactoe.h5`)
C’est le point de départ si l’on souhaite réentraîner l’IA sur un autre dataset.

---

### 5. `main.py`
L’interface principale du jeu :
- gestion du plateau
- affichage des boutons et des scores
- interaction utilisateur
- intégration de l’IA entraînée  
Le script permet de choisir la difficulté (facile, moyen, difficile) et de lancer une partie contre l’IA.

---

## Niveaux de difficulté dans gui.py

- **Facile** : l’IA joue uniquement au hasard, facile à battre
- **Moyen** : l’IA utilise le modèle MLP la plupart du temps, mais 30% de ses coups sont aléatoires, ce qui la rend plus humaine et imparfaite
- **Difficile** : l’IA suit strictement le modèle MLP, ce qui correspond à un joueur optimal

---

## Lancement

Depuis la racine :
    python3 main.py

---

## Points importants

- Projet **data-driven only** (pas de règles codées à la main)
- IA fixe après entraînement (pas de réapprentissage automatique)
- Modèle MLP multiclasses
- Interface claire et évolutive

---

## Remarques finales

Ce projet répond intégralement aux questions posées :
- Dataset récupéré et expliqué
- Modèle de classification entraîné
- Interface avec intégration de l’IA
- Niveaux de difficulté détaillés
- Explication complète des scripts fournis

---

## Membres du groupe

POPP Dietmar Ndremarolahy ;ISAIA 4 ;N°08 
RANJASON Sitrakaniaina Brundy Joel ;ISAIA 4 ;N°09 
RAKOTOFARA Nainantsalamana ;ISAIA 4 ;N°13 
DIMBINIERANA Tolojanahary Nisandratampifaliana;ISAIA 4; N°16 
ANDRIANASOLO Hasina Tovonambinintsoa ;IGGLIA 4;N°19 
RAKOTOMANALINARIVO Andy Nantenaina ;IGGLIA 4; N°56


