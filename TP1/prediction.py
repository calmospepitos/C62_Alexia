import numpy as np

def trouver_synonymes(methode, mot, n, mot_a_index, matrice_cooccurrence, stop_words):
    '''Trouve les n synonymes du mot donné en utilisant la méthode de recherche spécifiée.'''
    if mot not in mot_a_index: # Vérification de la présence du mot dans le vocabulaire
        print(f"Le mot '{mot}' n'est pas dans le vocabulaire.")
        return []
    
    index_mot = mot_a_index[mot] # Récupération de l'index du mot dans le vocabulaire
    vect_mot = matrice_cooccurrence[index_mot] # Vecteur 1xN (row) du mot
    scores = [] # Liste des scores de similarité
    
    for autre_mot, index_autre in mot_a_index.items(): # Parcours du vocabulaire
        if autre_mot != mot and autre_mot not in stop_words: # On ne veut pas comparer le mot avec lui-même ou avec un stop-word
            score = None
            vect_autre_mot = matrice_cooccurrence[index_autre] # Vecteur 1xN (row) de l'autre mot

            if methode == 0: # Méthode du produit scalaire
                score = np.dot(vect_mot, vect_autre_mot)
            elif methode == 1: # Méthode des moindres carrés
                score = np.linalg.norm(vect_mot - vect_autre_mot)
            elif methode == 2: # Méthode de la distance de Manhattan
                score = np.sum(np.abs(vect_mot - vect_autre_mot))
            else:
                print("Méthode de recherche invalide.")
                return []
            
            if score is not None:
                scores.append((autre_mot, score))
    
    if methode == 0:
        scores.sort(key=lambda x: x[1], reverse=True) # Tri par score décroissant puisque le plus grand score est le meilleur
    else:
        scores.sort(key=lambda x: x[1]) # Tri par score croissant puisque le plus petit score est le meilleur

    return scores[:n]