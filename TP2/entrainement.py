import re
import sqlite3
from database import Database

class Entrainement():
    def __init__(self, tfen: int) -> None:
        self.tfen = tfen
        self.__texte = []       
        self.__lexique = {}
        self.__lexique_ids = {}
        self.db = Database()   

    @property
    def lexique(self) -> dict[str, int]:
        """Retourne le mappage du lexique (mot -> index de la matrice) chargé depuis la base de données (via charger_donnees())."""
        return self.__lexique

    def entrainer(self, chemin: str, enc: str) -> None:
        """Entraînez le modèle à l’aide du fichier texte et de l’encodage fournis."""
        self.parser_fichier(chemin, enc)
        self.init_lexique()
        self.maj_lexique()
        self.maj_cooccurrences()

    def parser_fichier(self, chemin: str, enc: str) -> None:
        """Analysez le fichier texte et extrayez les mots, en ignorant la ponctuation et la casse."""
        with open(chemin, encoding=enc) as f:
            self.__texte = re.findall(r'\w+', f.read().lower())

    def init_lexique(self) -> None:
        """Construire un lexique à partir du texte (mot -> un index unique)."""
        self.__lexique = {}
        for mot in self.__texte:
            if mot not in self.__lexique:
                self.__lexique[mot] = len(self.__lexique)

    def maj_lexique(self) -> None:
        """Assurez-vous que chaque mot du lexique existe dans la base de données et stockez son ID de base de données."""
        with sqlite3.connect(self.db.chemin) as conn:
            for mot in self.__lexique:
                mot_id = self.db.get_or_create_mot_id(mot, conn)
                self.__lexique_ids[mot] = mot_id

    def maj_cooccurrences(self) -> None:
        """
        Pour chaque mot du texte, regardez les voisins dans la fenêtre (self.tfen) et mettez à jour leur fréquence de cooccurrence dans la base de données.
        """
        texte = self.__texte
        tfen = self.tfen

        with sqlite3.connect(self.db.chemin) as conn:
            for i in range(len(texte)):
                mot_central = texte[i]
                
                # Vérifiez si le mot central est dans le lexique
                if mot_central not in self.__lexique_ids:
                    continue
                id_central = self.__lexique_ids[mot_central]

                # Mettre à jour la cooccurrence avec le mot central
                for j in range(1, tfen // 2 + 1):
                    # Voisin de gauche
                    if i - j >= 0:
                        mot_gauche = texte[i - j]
                        if mot_gauche in self.__lexique_ids:
                            id_gauche = self.__lexique_ids[mot_gauche]
                            self.db.inserer_ou_mettre_a_jour_cooccurrence(
                                id_central, id_gauche, self.tfen, 1, conn
                            )
                    # Voisin de droite
                    if i + j < len(texte):
                        mot_droite = texte[i + j]
                        if mot_droite in self.__lexique_ids:
                            id_droite = self.__lexique_ids[mot_droite]
                            self.db.inserer_ou_mettre_a_jour_cooccurrence(
                                id_central, id_droite, self.tfen, 1, conn
                            )
            conn.commit()

    def charger_donnees(self) -> None:
        """
        Chargez les données de lexique et de cooccurrence depuis la base de données et reconstruisez une matrice en mémoire.
        Ceci est utilisé en mode prédiction.
        """
        import sqlite3
        import numpy as np

        with sqlite3.connect(self.db.chemin) as conn:
            # Récupérer le lexique
            cursor = conn.cursor()
            cursor.execute("SELECT id, mot FROM lexique")
            rows = cursor.fetchall()

            lex_temp = {}
            mapping = {}

            # Créer un mappage de mot à ID
            for i, (id_val, mot) in enumerate(sorted(rows, key=lambda r: r[0])):
                lex_temp[mot] = i
                mapping[id_val] = i
            self.__lexique = lex_temp
            
            # Récupérer la matrice de cooccurrence
            n = len(rows)
            matrice = np.zeros((n, n))
            
            # Récupérer les cooccurrences
            cursor.execute("SELECT mot1_id, mot2_id, frequence FROM cooccurrence WHERE taille_fenetre = ?", (self.tfen,))
            for mot1_id, mot2_id, frequence in cursor.fetchall():
                # Vérifiez si les mots existent dans le lexique
                if mot1_id in mapping and mot2_id in mapping:
                    i = mapping[mot1_id]
                    j = mapping[mot2_id]
                    matrice[i, j] = frequence

            # Créer la matrice symétrique
            self.__matrice = matrice
            self.matrice = self.__matrice
