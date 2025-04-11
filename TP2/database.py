import sqlite3

# CONSTANTES
CHEMINBD = 'database.db'

# REQUETES
CLES_ETRANGERES = '''PRAGMA foreign_keys = ON;'''

CREATE_ENTRAINEMENTS = '''
CREATE TABLE IF NOT EXISTS Entrainements (
    id_entrainement INTEGER PRIMARY KEY,
    nom_fichier TEXT NOT NULL,
    taille_fenetre INTEGER NOT NULL
);
'''

CREATE_LEXIQUE = '''
CREATE TABLE IF NOT EXISTS Lexique (
    id_mot INTEGER PRIMARY KEY AUTOINCREMENT,
    mot TEXT NOT NULL,
    id_entrainement INTEGER,
    FOREIGN KEY (id_entrainement) REFERENCES Entrainements(id_entrainement)
);
'''

CREATE_COOCCURRENCES = '''
CREATE TABLE IF NOT EXISTS Cooccurrences (
    id_mot1 INTEGER,
    id_mot2 INTEGER,
    id_entrainement INTEGER,
    nombre_occurrences REAL NOT NULL,
    PRIMARY KEY (id_mot1, id_mot2, id_entrainement),
    FOREIGN KEY (id_mot1) REFERENCES Lexique(id_mot),
    FOREIGN KEY (id_mot2) REFERENCES Lexique(id_mot),
    FOREIGN KEY (id_entrainement) REFERENCES Entrainements(id_entrainement)
);
'''

class Database():
    def __init__(self, chemin = CHEMINBD):
        self.chemin = CHEMINBD
    
    def creer_connexion(self):
        self.connexion = sqlite3.connect(self.chemin)
        self.curseur = self.connexion.cursor()
        self.curseur.execute(CLES_ETRANGERES)
    
    def fermer_connexion(self):
        self.curseur.close()
        self.connexion.close()

    def regenerer_db():
        with sqlite3.connect("cooccurrence.db") as conn:
            cursor = conn.cursor()

            # Drop existing tables if they exist
            cursor.execute("DROP TABLE IF EXISTS cooccurrence")
            cursor.execute("DROP TABLE IF EXISTS lexique")

            # Recreate tables
            cursor.execute("""
                CREATE TABLE lexique (
                    id INTEGER PRIMARY KEY,
                    mot TEXT UNIQUE NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE cooccurrence (
                    id INTEGER PRIMARY KEY,
                    mot1_id INTEGER NOT NULL,
                    mot2_id INTEGER NOT NULL,
                    taille_fenetre INTEGER NOT NULL,
                    frequence INTEGER NOT NULL DEFAULT 1,
                    FOREIGN KEY (mot1_id) REFERENCES lexique(id),
                    FOREIGN KEY (mot2_id) REFERENCES lexique(id)
                )
            """)

            conn.commit()

            print("✅ Base de données régénérée avec succès.")
            
    def generer_bd(self):
        pass

    def get_or_create_word_id(self, word):
        self.cursor.execute('SELECT id FROM Lexique WHERE mot = ?', (word,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        self.cursor.execute('INSERT INTO Lexique (mot) VALUES (?)', (word,))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def inserer_bd(self, mot1, mot2, taille_fenetre, count):
        # Regarder si la valeur est à 0 (pas de cooccurrence)
        if count == 0:
            return
        
        word1_id = self.get_or_create_word_id(mot1)
        word2_id = self.get_or_create_word_id(mot2)

        # Check if this cooccurrence already exists (for this window size)
        self.cursor.execute('''
            SELECT id, count FROM Cooccurrences
            WHERE mot1_id = ? AND mot2_id = ? AND taille_fenetre = ?
        ''', (word1_id, word2_id, taille_fenetre))
        result = self.cursor.fetchone()

        if result:
            # Update existing count
            cooc_id, existant_count = result
            self.cursor.execute('''
                UPDATE Cooccurrences SET count = ?
                WHERE id = ?
            ''', (existant_count + count, cooc_id))
        else:
            # Insert new cooccurrence
            self.cursor.execute('''
                INSERT INTO Cooccurrences (mot1_id, mot2_id, taille_fenetre, count)
                VALUES (?, ?, ?, ?)
            ''', (word1_id, word2_id, taille_fenetre, count))

        self.conn.commit()

    def imprimer_table(self, table, requete):
        print(f"Table {table}")
        self.curseur.execute(requete)
        for ligne in self.curseur.fetchall():
            print(ligne)
        print()
    
    def imprimer(self):
        pass
    