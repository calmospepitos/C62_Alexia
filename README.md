# C62_Alexia

## Clustering de cooccurrences

Ce projet implémente un pipeline complet de construction de lexique, d’entraînement de modèles de cooccurrence et de clustering (K‑means) selon les exigences du TP3 de votre cours.

---

### 1. Pré-requis

* **Python >= 3.8**
* Bibliothèques Python :

  * `numpy`
  * `matplotlib`

Installez-les via :

```bash
pip install numpy matplotlib
# et votre driver SQL si nécessaire
```

---

### 2. Structure du dépôt

```
TP3/
├── main.py            # point d’entrée principal
├── options.py         # définition des options CLI
├── clustering.py      # implémentation de l’algorithme KMeans
├── dao.py             # gestion de la BD (mots, cooccurrences)
├── entrainement.py    # (TP2) extraction et insertion des cooccurrences
├── entrainement_bd.py # (TP2) version BD directe
├── prediction.py      # module de prédiction (TP2)
├── texts/             # dossiers contenant vos 4 fichiers text1.txt…text4.txt
├── tests/             # traces de vos expériences (à générer)
└── README.md          # ce fichier
```

---

### 3. Remplissage de la base de données

Vous devez exécuter **une seule fois** le prétraitement (fenêtre=5 sur vos 4 textes), **avant** le clustering :

```bash
python main.py -b \
  -e --chemin texts/text1.txt --encodage utf-8 -t 5 \
  -e --chemin texts/text2.txt --encodage utf-8 -t 5 \
  -e --chemin texts/text3.txt --encodage utf-8 -t 5 \
  -e --chemin texts/text4.txt --encodage utf-8 -t 5
```

* `-b` : vide et initialise les tables `mots` et `cooccurrences`.
* `-e` : ajoute un texte (`--chemin`, `--encodage`) avec la taille de fenêtre `-t`.
* La fenêtre `5` correspond à la consigne du professeur.

> **Important :** cette étape charge **tous** les mots et cooccurrences **avant** toute exécution de clustering.

---

### 4. Clustering (K‑means)

Une fois la base initialisée, lancez le clustering :

```bash
python main.py -c -t 5 -k <K> -n <N> [--normaliser] [--conserver M] [--graphe]
```

* `-c`          : active le clustering.
* `-t 5`        : même taille de fenêtre que pour l’entraînement.
* `-k <K>`      : nombre de partitions (centroïdes).
* `-n <N>`      : nombre de mots à afficher par cluster.
* `--normaliser`: normalise chaque vecteur avant clustering.
* `--conserver M`: ne garde que les `M` features les plus fréquentes.
* `--graphe`    : affiche un graphique (`migrations` vs `itérations`).

#### 4.1. Exemples

```bash
# Clustering basique, k=5
python main.py -c -t 5 -k 5 -n 10 > resultats_t5_k5.txt

# Clustering normalisé, k=10, conserve 500 features
python main.py -c -t 5 -k 10 -n 8 --normaliser --conserver 500 > resultats_t5_k10.txt

# Graphe des migrations
python main.py -c -t 5 -k 20 -n 5 --graphe
```

Vous pouvez tester plusieurs valeurs de `K` en boucle :

```bash
for K in 5 10 20 50 100; do
  python main.py -c -t 5 -k $K -n 10 > resultats_t5_k${K}.txt
done
```

---

### 5. Validation et redirection

* **Redirection** : utilisez `> fichier.txt` pour capturer toute la sortie dans un fichier.
* **Contenu de `resultats_*.txt`** :

  1. Trace des itérations : temps, migrations, taille de chaque partition.
  2. Temps total de partitionnement.
  3. Liste des top‑N mots par cluster (avec distance).

---

### 6. Notes finales

* Le reste des fonctionnalités (TP2) demeure inchangé.
* La soumission inclut :

  * les 4 textes originaux (`texts/`).
  * la base de données pré-remplie.
  * tous les fichiers `resultats_*.txt`.
