from argparse import ArgumentParser
from os.path import isfile

class Options():
    def __init__(self) -> None:
        self.parser = ArgumentParser()
        
        self.mx = self.parser.add_mutually_exclusive_group(required=True)
        self.mx.add_argument("-b", action="store_true", help="Générer BD")
        self.mx.add_argument("-e", action="store_true", help="Entraînement")
        self.mx.add_argument("-p", action="store_true", help="Prédiction")
        self.mx.add_argument("-c", action="store_true", help="Clustering (K-means)")
        
        self.parser.add_argument("-t", type=int, help="Taille de fenêtre")
        self.parser.add_argument("-k", type=int, help="Nombre de centroïdes")
        self.parser.add_argument("-n", type=int, help="Nombre de mots à afficher par cluster")
        self.parser.add_argument("--normaliser", action="store_true", help="Normaliser les vecteurs avant clustering")
        self.parser.add_argument("--graphe", action="store_true", help="Afficher le graphe des migrations")
        self.parser.add_argument("--conserver", type=int, help="Nombre de features à conserver dans la matrice")

        self.parser.add_argument("--chemin", type=str, help="Chemin du fichier texte pour l'entraînement")
        self.parser.add_argument("--encodage", type=str, help="Encodage du fichier texte pour l'entraînement")
        
        self.parser.add_argument("-v", "--verbose", action="count", default=0, help="Change la quantité de sorties")
        
        self.recuperer_options()
        
    def recuperer_options(self) -> None:
        self.parser.parse_args(namespace=self)
        
        if self.e or self.p:
            if self.t is None or not isinstance(self.t, int) or self.t <= 0 or self.t % 2 != 1:
                raise Exception("Pour entraîner ou prédire, vous devez fournir une taille de fenêtre entière, positive et impaire.")
            if self.e:
                if not self.chemin or not isfile(self.chemin):
                    raise Exception("Veuillez fournir un chemin de fichier texte valide pour l'entraînement.")
                    
                if not self.encodage:
                    raise Exception("Veuillez fournir l'encodage du fichier texte pour l'entraînement.")
                "test".encode(self.encodage, errors="strict")
                
def main() -> int:
    try:
        opts = Options()
        print(vars(opts))
        print(opts.t)
    except Exception as e:
        print(e)
    
    return 0

if __name__ == '__main__':
    quit(main())