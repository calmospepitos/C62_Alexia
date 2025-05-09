from sys import argv
from traceback import print_exc
from time import perf_counter
#from entrainement import Entrainement
from entrainement_bd import Entrainement_BD
from prediction import Prediction
from options import Options
from dao import DAO
from clustering import KMeans
import numpy as np
import time
import matplotlib.pyplot as plt

QUITTER = 'q'
MESSAGE = f'''
Entrez un mot, le nombre de synonymes que vous voulez et la méthode de calcul,
i.e. produit scalaire: 0, least-squares: 1, city-block: 2

Tapez {QUITTER} pour quitter.

'''
AFFICHER_TEMPS = 1
AFFICHER_TOUT = 2

def interface_prediction(cerveau: Entrainement_BD, verbose: int = 0) -> None:
    reponse = input(MESSAGE)
    while reponse != QUITTER:
        try:
            t = perf_counter()
            mot, nb_syn, methode = reponse.split()
            candidats = Prediction.predire(cerveau, mot, int(nb_syn), int(methode))
            
            if verbose >= AFFICHER_TEMPS:
                print(f'\nPrédiction en {perf_counter() - t:.2f} secondes.')
            
            print()
            for mot, score in candidats:
                print(f'{mot} --> {score:.2f}')
        except Exception as e:
            print(f'\n{e}')
            
        reponse = input(MESSAGE)

def main() -> int:
    try:
        opts = Options()
        t = perf_counter()
        
        with DAO() as bd:
            if opts.b:
                bd.regenerer_tables()
                if opts.verbose >= AFFICHER_TEMPS:
                    print(f'\nRegénération réalisée en {perf_counter() - t:.2f} secondes.')
                    
            else:
                cerveau = Entrainement_BD(opts.t, bd)
                if opts.e:
                    t = perf_counter()
                    cerveau.entrainer(opts.chemin, opts.encodage)
                    if opts.verbose >= AFFICHER_TEMPS:
                        print(f'\nEntraînement réalisé en {perf_counter() - t:.2f} secondes.')
                    if opts.verbose >= AFFICHER_TOUT:
                        print(cerveau.lexique)
                        print(cerveau.matrice)
                
                elif opts.p:
                    cerveau.charger_donnees()
                    if opts.verbose >= AFFICHER_TEMPS:
                        print(f'\nDonnées chargées en {perf_counter() - t:.2f} secondes.')
                    interface_prediction(cerveau, opts.verbose)

                elif opts.c:
                    with DAO() as dao:
                        mots = dao.recuperer_mots()  # liste de (id, mot)
                        id_to_word = {id: mot for mot, id in mots}
                        coocs = dao.recuperer_cooccurrences(opts.t)
                    
                    V = len(mots)
                    id_to_idx = {id: idx for idx, (mot, id) in enumerate(mots)}
                    data = {id: np.zeros(V, dtype=float) for mot, id in mots}
                    for i, j, count in coocs:
                        data[i][id_to_idx[j]] = count
                        data[j][id_to_idx[i]] = count

                    if opts.conserver:
                        freqs = np.sum(np.stack(list(data.values())), axis=0)
                        top_feats = np.argsort(freqs)[-opts.conserver:]
                        for mid in data:
                            data[mid] = data[mid][top_feats]
                    
                    if opts.normaliser:
                        for mid in data:
                            norm = np.linalg.norm(data[mid])
                            if norm > 0:
                                data[mid] /= norm
                    
                    start_total = time.time()
                    km = KMeans(opts.k)
                    km.fit(data)
                    total_time = time.time() - start_total
                    print(f"Partitionnement en {total_time:.2f} secondes.\n")

                    clusters = km.top_n(opts.n)
                    for c, items in clusters.items():
                        print(f"Partition {c}\t:")
                        for mid, dist in items:
                            print(f"\t{id_to_word[mid]} -> {dist:.6f}")
                        print()
                    
                    if opts.graphe:
                        plt.plot(range(1, len(km.migrations) + 1), km.migrations, label=f"k = {opts.k}")
                        plt.title("Migrations par itération")
                        plt.xlabel("Itérations")
                        plt.ylabel("Migrations")
                        plt.legend()
                        plt.grid(True)
                        plt.show()
                    return 0
            
    except:
        print_exc()
        return 1
    return 0

if __name__ == '__main__':
    quit(main())