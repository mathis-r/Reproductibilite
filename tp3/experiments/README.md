# Dossier d'expérimentation (TP3)

Ce dossier regroupe le moteur d'exécution des variantes, les résultats sérialisés et le notebook d'analyse.

---

## 1. Dépendances requises

Toutes les dépendances nécessaires au pipeline (échantillonnage, exécution et analyse) sont listées dans `tp3/requirements.txt` :
* `flamapy==2.6.0` : analyse du modèle UVL et échantillonnage.
* `numpy` : génération aléatoire et évaluation vectorisée des opérations en Python.
* `pandas` : chargement et manipulation des données de résultats.
* `scikit-learn` : modélisation par arbre de décision (`DecisionTreeRegressor`).
* `matplotlib` : génération des graphiques et visualisations.

### Installation :
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt
```

---

## 2. Contenu du dossier

* `runner.c` : code C pur contenant le générateur pseudo-aléatoire (`xorshift64`) et les fonctions d'évaluation des 4 propriétés mathématiques.
* `run_experiments.py` : script procédural qui lit `sample.csv`, compile dynamiquement `runner.c` avec `gcc` (flags `-O0`, `-O2`, `-O3`, `-ffast-math`) ou lance les variantes Python avec NumPy.
* `results.csv` : fichier contenant les 99 runs d'expérimentation (3 répétitions par configuration avec graines fixées).
* `analysis.ipynb` : notebook Jupyter d'analyse statistique, d'arbre de décision et de visualisation.

---

## 3. Lancer les expérimentations et l'analyse

```bash
# 1. Lancer les runs (99 exécutions en ~3s)
python run_experiments.py --sample ../sample.csv --output results.csv --runs 3

# 2. Ouvrir le notebook d'analyse
jupyter lab analysis.ipynb
```
