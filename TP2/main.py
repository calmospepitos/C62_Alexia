import argparse
from entrainement import Entrainement
from prediction import Prediction
from database import Database

def main():
    parser = argparse.ArgumentParser(description="Système de cooccurrences pour prédire des synonymes.")

    # Options possibles
    parser.add_argument("-e", action="store_true", help="Mode entraînement")
    parser.add_argument("-p", action="store_true", help="Mode prédiction")
    parser.add_argument("-b", action="store_true", help="Régénérer la base de données")
    parser.add_argument("-t", type=int, help="Taille de la fenêtre")
    parser.add_argument("--encodage", type=str, help="Encodage du fichier texte")
    parser.add_argument("--chemin", type=str, help="Chemin vers le fichier texte")

    args = parser.parse_args()

    if args.b:
        db = Database()
        db.regenerer_db()

    elif args.e:
        if args.t and args.encodage and args.chemin:
            entrainement = Entrainement(args.t)
            entrainement.entrainer(chemin=args.chemin, enc=args.encodage)
        else:
            print("Erreur : Les options -t, --encodage et --chemin sont obligatoires avec -e")
    elif args.p:
        if args.t:
            cerveau = Entrainement(args.t)

            mot = input("Entrez un mot à rechercher: ")
            nb_syn = int(input("Nombre de synonymes à afficher: "))
            methode = int(input("Choisissez une méthode de calcul (0 = produit scalaire, 1 = moindres carrés, 2 = distance de Manhattan): "))
            
            try:
                resultats = Prediction.predire(cerveau, mot, nb_syn, methode)
                print(f"\nSynonymes de '{mot}':")
                for syn_mot, score in resultats:
                    print(f"{syn_mot}: {score}")
            except Exception as e:
                print(f"Erreur: {e}")
        else:
            print("Erreur : L'option -t est obligatoire avec -p")
    else:
        print("Aucune option valide fournie. Utilisez -e, -p ou -b.")

if __name__ == "__main__":
    main()
