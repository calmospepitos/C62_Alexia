from sys import argv
from traceback import print_exc
from time import perf_counter
from entrainement import Entrainement
from prediction import Prediction

QUITTER = 'q'
MESSAGE = f'''
Entrez un mot, le nombre de synonymes que vous voulez et la méthode de calcul,
i.e. produit scalaire: 0, least-squares: 1, city-block: 2

Tapez {QUITTER} pour quitter.

'''

def extraire_infos(reponse: str) -> tuple[str, int, int]:
    mot, nb_syn, methode = reponse.split()
    nb_syn, methode = int(nb_syn), int(methode)
    if methode < 0 or methode > 2 or nb_syn < 1:
        raise Exception("S.V.P. respectez le format des entrées.")
    return mot, nb_syn, methode

def imprimer_candidats(candidats: list[str, float]) -> None:
    print()
    for mot, score in candidats:
        print(f'{mot} --> {score:.2f}')

def interface_prediction(cerveau: Entrainement, verbose: int = 0) -> None:
    while True:
        reponse = input(MESSAGE)
        if reponse == QUITTER:
            break
        try:
            mot, nb_syn, methode = extraire_infos(reponse)
        except Exception as e:
            print(f'\n{e}')
            continue
        try:
            t = perf_counter()
            candidats = Prediction.predire(cerveau, mot, nb_syn, methode)
            if verbose:
                print(f'\nPrédiction en {perf_counter() - t:.2f} secondes.')
            imprimer_candidats(candidats)
        except Exception as e:
            print(f'\n{e}')

def main() -> int:
    try:
        tfen, enc, chemin, verbose = int(argv[1]), argv[2], argv[3], 0
        if len(argv) > 4:
            verbose = int(argv[4])
        
        t = perf_counter()
        cerveau = Entrainement(tfen)
        cerveau.entrainer(chemin, enc)
        if verbose:
            print(f'\nEntraînement réalisé en {perf_counter() - t:.2f} secondes.')
            # print(cerveau.lexique)
            # print(cerveau.matrice)
            
        interface_prediction(cerveau, verbose)
            
    except:
        if verbose:
            print_exc()
        return 1
    return 0

if __name__ == '__main__':
    quit(main())