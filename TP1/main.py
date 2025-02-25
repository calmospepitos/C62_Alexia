import entrainement as ent
import prediction as pred
from sys import argv

class Main:
    def __init__(self):
        if len(argv) < 4:
            print("Usage: python main.py <taille_fenetre> <encodage> <chemin>")
            exit(1)
        self.taille_fenetre = int(argv[1])
        self.encodage = argv[2]
        self.chemin = argv[3]
        self.dictionnaire, self.matrice_cooccurrence = ent.Entrainement.entrainer(self.taille_fenetre, self.encodage, self.chemin)
        
    def main(self):
        while True:
            user_input = input(
"""Entrez un mot, le nombre de synonymes que vous voulez et la méthode de recherche (ex: chien 2 0).
0 : produit scalaire, 1 : least-squares, 2 : city-block.
Tapez 'Q' pour quitter...
> """
).strip()

            if user_input.lower() == 'q':
                print("Fin du programme.")
                break

            try:
                mot, n, methode = user_input.split()
                n = int(n)
                methode = int(methode)
                synonymes = pred.Prediction.trouver_synonymes(methode, mot, n, self.dictionnaire, self.matrice_cooccurrence)

                if synonymes:
                    print(f"Les {n} synonymes de '{mot}' sont:")
                    for i, (synonyme, score) in enumerate(synonymes, 1):
                        print(f"{i}. {synonyme} -> {score}")
                else:
                    print("Aucun synonyme trouvé.")
            except ValueError:
                print("Erreur: Veuillez entrer un mot suivi d'un nombre et d'une méthode (ex: chat 5 0)")
                continue

if __name__ == "__main__":
    main_instance = Main()
    quit(main_instance.main())