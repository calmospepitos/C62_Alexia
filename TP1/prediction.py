import numpy as np
import json

# On charge les stop words
with open("stopwords-fr.json", "r", encoding="utf-8") as file:
    stop_words = set(json.load(file))

class Prediction:
    def trouver_synonymes(methode, mot, n, dictionnaire, matrice_cooccurrence):
        '''Trouve les n synonymes du mot donné en utilisant la méthode de recherche spécifiée et retourne une liste de mots ayant les meilleurs scores.'''
        if mot not in dictionnaire: # Vérification de la présence du mot dans le vocabulaire
            print(f"Le mot '{mot}' n'est pas dans le vocabulaire.")
            return []
        
        index_mot = dictionnaire[mot] # Récupération de l'index du mot dans le vocabulaire
        vect_mot = matrice_cooccurrence[index_mot] # Vecteur 1xN (row) du mot
        scores = [] # Liste des scores de similarité
        
        for autre_mot, index_autre in dictionnaire.items(): # Parcours du vocabulaire
            if autre_mot != mot and autre_mot not in stop_words: # On ne veut pas comparer le mot avec lui-même ou avec un stop-word
                score = None
                vect_autre_mot = matrice_cooccurrence[index_autre] # Vecteur 1xN (row) de l'autre mot

                if methode == 0: # Méthode du produit scalaire
                    score = np.dot(vect_mot, vect_autre_mot)
                elif methode == 1: # Méthode des moindres carrés
                    score = np.sum(pow((vect_mot - vect_autre_mot), 2))
                elif methode == 2: # Méthode de la distance de Manhattan
                    score = np.sum(np.abs(vect_mot - vect_autre_mot))
                else:
                    print("Méthode de recherche invalide.")
                    return []
                
                if score is not None:
                    scores.append((autre_mot, score))
        
        if methode == 0:
            scores = sorted(scores, key=lambda x: x[1], reverse=True) # Tri par score décroissant puisque le plus grand score est le meilleur
        else:
            scores = sorted(scores, key=lambda x: x[1]) # Tri par score croissant puisque le plus petit score est le meilleur

        return scores[:n]