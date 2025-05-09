import sqlite3
from typing import Self, Optional, Type
from types import TracebackType
from traceback import print_tb

CHEMIN_BD = "cooccurrence.db"
FK = "PRAGMA foreign_keys = 1"

CREER_MOT = '''
CREATE TABLE IF NOT EXISTS mot
(
    id      INTEGER PRIMARY KEY NOT NULL,
    chaine  CHAR(25) NOT NULL UNIQUE
)
'''
DROP_MOT = 'DROP TABLE IF EXISTS mot'
INSERT_MOT = 'INSERT OR IGNORE INTO mot(chaine, id) VALUES(?, ?)'
SELECT_MOT = 'SELECT chaine, id FROM mot'

CREER_COOCCURRENCE = '''
CREATE TABLE IF NOT EXISTS cooccurrence
(
    rangee      INTEGER NOT NULL REFERENCES mot(id),
    colonne     INTEGER NOT NULL REFERENCES mot(id),
    frequence   INTEGER NOT NULL,
    taille      INTEGER NOT NULL,
    PRIMARY KEY(rangee, colonne, taille)
)
'''
DROP_COOCCURRENCE = 'DROP TABLE IF EXISTS cooccurrence'
INSERT_COOCCURRENCE = 'INSERT OR REPLACE INTO cooccurrence VALUES(?, ?, ?, ?)'
SELECT_COOCCURRENCE = 'SELECT rangee, colonne, frequence FROM cooccurrence WHERE taille = ?'


# context manager?
class DAO():
    def __init__(self, chemin_bd: str = CHEMIN_BD) -> None:
        self.chemin_bd = chemin_bd
        
    def __enter__(self) -> Self:
        self.connexion = sqlite3.connect(self.chemin_bd)
        self.curseur = self.connexion.cursor()
        self.curseur.execute(FK)
        return self
        
    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException], traceback: Optional[TracebackType]) -> bool:
        self.curseur.close()
        self.connexion.close()
        if exc_type:
            print(f'{type(exc_type)}: {exc_type}')
            print(f'{type(exc_value)}: {exc_value}')
            print(f'{type(traceback)}: {traceback}')
            print_tb(traceback)
            
            #true arrête la propagation de l'erreur
            #false ou None la propage
            return True
        
    def regenerer_tables(self) -> None:
        self.curseur.execute(DROP_COOCCURRENCE)
        self.curseur.execute(DROP_MOT)
        self.curseur.execute(CREER_MOT)
        self.curseur.execute(CREER_COOCCURRENCE)
        
    def recuperer_mots(self) -> list[tuple[str, int]]:
        self.curseur.execute(SELECT_MOT)
        return self.curseur.fetchall()
        
    def inserer_mots(self, mots: list[tuple[str, int]]):
        self.curseur.executemany(INSERT_MOT, mots)
        self.connexion.commit()
        
    def recuperer_cooccurrences(self, taille_fenetre: int) -> list[tuple[int, int, int]]:
        self.curseur.execute(SELECT_COOCCURRENCE, (taille_fenetre,))
        return self.curseur.fetchall()
    
    def inserer_cooccurrences(self, cooccurrences: list[tuple[int, int, int, int]]):
        self.curseur.executemany(INSERT_COOCCURRENCE, cooccurrences)
        self.connexion.commit()
        