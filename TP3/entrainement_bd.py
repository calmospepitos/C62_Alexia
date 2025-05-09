import numpy as np
from entrainement import Entrainement
from dao import DAO

class Entrainement_BD(Entrainement):
    def __init__(self, tfen: int, bd: DAO):
        super().__init__(tfen)
        self.bd = bd
        
    def init_lexique(self) -> dict[str, int]:
        super().init_lexique()
        for mot, id in self.bd.recuperer_mots():
            self.lexique[mot] = id
            
    def maj_lexique(self) -> None:
        super().maj_lexique()
        self.bd.inserer_mots(self.lexique.items())
        
    def init_cooccurrences(self) -> np.ndarray:
        super().init_cooccurrences()
        for r, c, frequence in self.bd.recuperer_cooccurrences(self.tfen):
            self.matrice[r, c] = frequence
            
    def maj_cooccurrences(self) -> None:
        super().maj_cooccurrences()
        rc = np.transpose(np.array(np.where(self.matrice > 0)))
        cooccurrences = [(int(r), int(c), self.matrice[r, c], self.tfen) for r, c in rc]
        self.bd.inserer_cooccurrences(cooccurrences)
        
    def charger_donnees(self) -> None:
        self.init_lexique()
        self.init_cooccurrences()
        