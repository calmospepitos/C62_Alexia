import entrainement as ent

def main():
    vocabulaire, matrice_cooccurrence = ent.lire_texte() # Appel de la fonction lire_texte() du module entrainement.py qui retourne le vocabulaire et la matrice de cooccurrence

    while True:
        user_input = input("""Entrez un mot, le nombre de synonymes que vous voulez et la méthode de recherche.
0: produit scalaire, 1: least-squares, 2: city-block.
Tapez Q pour quitter...
> """).strip()

        if user_input.lower() == 'q':
            print("Fin du programme.")
            break

        try:
            mot, n, methode = user_input.split()
            n = int(n)
            methode = int(methode)
            # Affichage des informations pour debug
            print(f"Mot: {mot}, Nombre de synonymes: {n}, Méthode de recherche: {methode}.\n")
            print(f"Vocabulaire: {vocabulaire}\nMatrice:\n{matrice_cooccurrence}\n")

            # TODO: Ajouter la fonction de recherche de synonymes ici
            
        except ValueError:
            print("Erreur: Veuillez entrer un mot suivi d'un nombre et d'une méthode (ex: chat 5 0)")
            continue

if __name__ == "__main__":
    quit(main())