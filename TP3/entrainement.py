import re
from time import perf_counter
import numpy as np

class Entrainement():
    def __init__(self, tfen: int) -> None:
        self.tfen = tfen
        
    @property
    def lexique(self) -> dict[str, int]:
        return self.__lexique
    
    @property
    def matrice(self) -> np.ndarray:
        return self.__matrice
        
    def entrainer(self, chemin: str, enc: str) -> None:
        self.parser_fichier(chemin, enc)
        self.init_lexique()
        self.maj_lexique()
        self.init_cooccurrences()
        self.maj_cooccurrences()
        
    def parser_fichier(self, chemin: str, enc: str) -> list[str]:
        with open(chemin, encoding = enc) as f:
            self.__texte = re.findall(r'\w+', f.read().lower())
        
    def init_lexique(self) -> dict[str, int]:
        self.__lexique = {}
    
    def maj_lexique(self) -> None:
        for mot in self.__texte:
            if mot not in self.__lexique:
                self.__lexique[mot] = len(self.__lexique)
                
    def init_cooccurrences(self) -> np.ndarray:
        self.__matrice = np.zeros( (len(self.__lexique), len(self.__lexique)) )
    
    def maj_cooccurrences(self) -> None:
        for i in range(len(self.__texte)):
            rangee = self.__lexique[self.__texte[i]]
            for j in range(1, self.tfen//2 + 1):
                if i - j >= 0:
                    colonne = self.__lexique[self.__texte[i - j]]
                    self.__matrice[rangee, colonne] += 1
                if i + j < len(self.__texte):
                    colonne = self.__lexique[self.__texte[i + j]]
                    self.__matrice[rangee, colonne] += 1