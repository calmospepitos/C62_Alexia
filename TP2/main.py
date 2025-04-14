import argparse
from entrainement import Entrainement
from prediction import Prediction
from database import Database

def main():
    parser = argparse.ArgumentParser(description="Système de cooccurrences pour prédire des synonymes.")

    # Arguments de ligne de commande
    parser.add_argument("-e", action="store_true", help="Mode entraînement")
    parser.add_argument("-p", action="store_true", help="Mode prédiction")
    parser.add_argument("-b", action="store_true", help="Régénérer la base de données")
    parser.add_argument("-t", type=int, help="Taille de la fenêtre")
    parser.add_argument("--encodage", type=str, help="Encodage du fichier texte")
    parser.add_argument("--chemin", type=str, help="Chemin vers le fichier texte")

    args = parser.parse_args()

    # Mode régénération
    if args.b:
        db = Database()
        db.regenerer_db()
        print("✅ Base de données régénérée avec succès.")

    # Mode entraînement
    elif args.e:
        if args.t and args.encodage and args.chemin:
            entrainement = Entrainement(args.t)
            entrainement.entrainer(chemin=args.chemin, enc=args.encodage)
            print("✅ Entraînement terminé.")
        else:
            print("❌ Erreur : -t, --encodage et --chemin sont requis avec -e.")

    # Mode prédiction
    elif args.p:
        if args.t:
            moteur = Entrainement(args.t)

            while True:
                user_input = input(
"""Entrez un mot, le nombre de synonymes que vous voulez et la méthode de recherche (ex: chien 2 0).
0 : produit scalaire, 1 : moindres carrés, 2 : distance de Manhattan.
Tapez 'Q' pour quitter...
> """
                ).strip()

                if user_input.lower() == 'q':
                    print("👋 Fin du programme.")
                    break

                try:
                    mot, n, methode = user_input.split()
                    n = int(n)
                    methode = int(methode)

                    resultats = Prediction.predire(moteur, mot, n, methode)

                    if resultats:
                        print(f"\n🔍 Les {n} synonymes de '{mot}' sont:")
                        for i, (synonyme, score) in enumerate(resultats, 1):
                            print(f"{i}. {synonyme} -> {score}")
                    else:
                        print("Aucun synonyme trouvé.")

                except ValueError:
                    print("❌ Erreur: format attendu -> mot nombre méthode (ex: chat 5 0)")
                except Exception as e:
                    print(f"❌ Erreur pendant la prédiction : {e}")
        else:
            print("❌ Erreur : -t est requis avec -p.")
    else:
        print("❌ Aucune option valide fournie. Utilisez -e, -p ou -b.")

if __name__ == "__main__":
    main()
