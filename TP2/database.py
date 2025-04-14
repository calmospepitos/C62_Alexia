import os
import sqlite3

# CONSTANTES
CHEMINBD = os.path.join(os.path.dirname(__file__), "cooccurrence.db")

# REQUÊTES SQL
CLES_ETRANGERES = 'PRAGMA foreign_keys = ON;'

CREATE_LEXIQUE = """
CREATE TABLE IF NOT EXISTS lexique (
    id INTEGER PRIMARY KEY,
    mot TEXT UNIQUE NOT NULL
);
"""

CREATE_INDEX_LEXIQUE_MOT1 = """
CREATE INDEX IF NOT EXISTS idx_lexique_mot ON lexique(mot);
"""

CREATE_COOCCURRENCES = """
CREATE TABLE IF NOT EXISTS cooccurrence (
    id INTEGER PRIMARY KEY,
    mot1_id INTEGER NOT NULL,
    mot2_id INTEGER NOT NULL,
    taille_fenetre INTEGER NOT NULL,
    frequence INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (mot1_id) REFERENCES lexique(id),
    FOREIGN KEY (mot2_id) REFERENCES lexique(id),
    UNIQUE(mot1_id, mot2_id, taille_fenetre)
);
"""

CREATE_INDEX_COOCCURRENCE = """
CREATE INDEX IF NOT EXISTS idx_cooccurrence_mot1 ON cooccurrence(mot1_id);
"""
CREATE_INDEX_LEXIQUE_MOT2 = """
CREATE INDEX IF NOT EXISTS idx_cooccurrence_mot2 ON cooccurrence(mot2_id);
"""
CREATE_INDEX_COOCCURRENCE_COMPOUND = """
CREATE INDEX IF NOT EXISTS idx_cooccurrence_compound ON cooccurrence(mot1_id, mot2_id, taille_fenetre);
"""
CREATE_INDEX_COOCCURRENCE_FREQUENCE = """
CREATE INDEX IF NOT EXISTS idx_cooccurrence_freq ON cooccurrence(mot1_id, frequence DESC);
"""

DROP_TABLE_LEXIQUE = "DROP TABLE IF EXISTS lexique;"
DROP_TABLE_COOCCURRENCE = "DROP TABLE IF EXISTS cooccurrence;"

class Database:
    def __init__(self, chemin=CHEMINBD):
        self.chemin = chemin

    def creer_connexion(self):
        self.connexion = sqlite3.connect(self.chemin)
        self.curseur = self.connexion.cursor()
        self.curseur.execute(CLES_ETRANGERES)

    def fermer_connexion(self):
        self.curseur.close()
        self.connexion.close()

    def regenerer_db(self):
        with sqlite3.connect(self.chemin) as conn:
            cursor = conn.cursor()
            cursor.execute(CLES_ETRANGERES)
            cursor.execute(DROP_TABLE_COOCCURRENCE)
            cursor.execute(DROP_TABLE_LEXIQUE)
            cursor.execute(CREATE_LEXIQUE)
            cursor.execute(CREATE_INDEX_LEXIQUE_MOT1)
            cursor.execute(CREATE_COOCCURRENCES)
            cursor.execute(CREATE_INDEX_COOCCURRENCE)
            cursor.execute(CREATE_INDEX_COOCCURRENCE_COMPOUND)
            cursor.execute(CREATE_INDEX_COOCCURRENCE_FREQUENCE)
            cursor.execute(CREATE_INDEX_LEXIQUE_MOT2)
            conn.commit()

    def get_or_create_mot_id(self, mot, conn=None):
        close_conn = False
        if conn is None:
            conn = sqlite3.connect(self.chemin)
            close_conn = True
        
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM lexique WHERE mot = ?", (mot,))
        row = cursor.fetchone()
        if row:
            result = row[0]
        else:
            cursor.execute("INSERT INTO lexique (mot) VALUES (?)", (mot,))
            conn.commit()
            result = cursor.lastrowid
        
        if close_conn:
            cursor.close()
            conn.close()
            
        return result

    def inserer_ou_mettre_a_jour_cooccurrence(self, mot1_id, mot2_id, taille_fenetre, frequence, conn=None):
        close_conn = False
        if conn is None:
            conn = sqlite3.connect(self.chemin)
            close_conn = True
        
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE cooccurrence
            SET frequence = frequence + ?
            WHERE mot1_id = ? AND mot2_id = ? AND taille_fenetre = ?
        """, (frequence, mot1_id, mot2_id, taille_fenetre))
        if cursor.rowcount == 0:
            cursor.execute("""
                INSERT INTO cooccurrence (mot1_id, mot2_id, taille_fenetre, frequence)
                VALUES (?, ?, ?, ?)
            """, (mot1_id, mot2_id, taille_fenetre, frequence))
        
        if close_conn:
            conn.commit()
            cursor.close()
            conn.close()
        
        return cursor.rowcount

    def imprimer_table(self, table, requete):
        self.creer_connexion()
        print(f"Table {table}")
        self.curseur.execute(requete)
        for ligne in self.curseur.fetchall():
            print(ligne)
        print()
        self.fermer_connexion()
