import numpy as np
import re

class Entrainement:
    def lire_texte(encodage, chemin):
        '''Lit le texte dans le fichier texte.txt et retourne une liste de mots.'''
        texte = []

        try:
            with open(chemin, 'r', encoding = encodage) as file:
                texte = file.read().lower()
                texte = re.findall(r'\w+', texte)
        except FileNotFoundError:
            print(f"Le fichier {chemin} est introuvable.")
            return None

        return texte


    def creer_dictionnaire(texte):
        '''Crée un dictionnaire à partir d'une liste de mots.'''
        dictionnaire = {}
        for mot in texte:
            if mot not in dictionnaire:
                dictionnaire[mot] = len(dictionnaire)

        return dictionnaire
    

    def creer_matrice_cooccurrence(mots, dictionnaire, taille_fenetre):
        '''Crée une matrice de cooccurrence à partir d'une liste de mots et d'un dictionnaire.'''
        taille_vocabulaire = len(dictionnaire)
        matrice_cooccurrence = np.zeros((taille_vocabulaire, taille_vocabulaire))

        for i, mot in enumerate(mots): # Parcours de la liste de mots
            debut = max(i - taille_fenetre, 0) # Début de la fenêtre
            fin = min(i + taille_fenetre + 1, len(mots)) # Fin de la fenêtre
            row = dictionnaire[mot] # Ligne correspondant au mot
            for j in range(debut, fin):
                if i != j: # On ne veut pas compter le mot lui-même
                    mot_voisin = mots[j] # Voisin dans la fenêtre
                    col = dictionnaire[mot_voisin] # Colonne correspondant au mot voisin
                    matrice_cooccurrence[row, col] += 1 # Incrémentation de la matrice de cooccurrence

        return matrice_cooccurrence
    

    def entrainer(taille_fenetre, encodage, chemin):
        '''Entraîne le modèle sur le texte donné et retourne le dictionnaire et la matrice de cooccurrence.'''
        texte = Entrainement.lire_texte(encodage, chemin)
        dictionnaire = Entrainement.creer_dictionnaire(texte)
        matrice_cooccurence = Entrainement.creer_matrice_cooccurrence(texte, dictionnaire, taille_fenetre)

        return dictionnaire, matrice_cooccurence