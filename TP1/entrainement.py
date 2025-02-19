import string
import numpy as np

def lire_texte():
    """Lit le texte, enlève la ponctuation et met en minuscule et retourne une matrice de cooccurrence ainsi qu'un dictionnaire."""
    file_path = 'texte.txt'
    texte = []

    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            for line in file:
                line = line.lower().translate(str.maketrans('', '', string.punctuation))
                mots = line.split()
                texte.extend(mots)
    except FileNotFoundError:
        print(f"Le fichier {file_path} est introuvable.")
        return [], None
    
    return creer_matrice_cooccurrence(texte)
    
def creer_matrice_cooccurrence(mots):
    '''Crée une matrice de cooccurrence à partir d'une liste de mots.'''
    taille_fenetre = 2
    vocabulaire = sorted(set(mots)) # Création d'un vocabulaire trié et sans doublons
    mot_a_index = {mot: i for i, mot in enumerate(vocabulaire)} 
    taille_vocabulaire = len(vocabulaire)
    matrice_cooccurrence = np.zeros((taille_vocabulaire, taille_vocabulaire), dtype=int)

    for i, mot in enumerate(mots): # Parcours de la liste de mots
        debut = max(i - taille_fenetre, 0) # Début de la fenêtre
        fin = min(i + taille_fenetre + 1, len(mots)) # Fin de la fenêtre
        row = mot_a_index[mot] # Ligne correspondant au mot
        for j in range(debut, fin):
            if i != j: # On ne veut pas compter le mot lui-même
                mot_voisin = mots[j] # Voisin dans la fenêtre
                col = mot_a_index[mot_voisin] # Colonne correspondant au mot voisin
                matrice_cooccurrence[row, col] += 1 # Incrémentation de la matrice de cooccurrence

    return mot_a_index, matrice_cooccurrence