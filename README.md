# Reproductibilité 2026 -- 2027

Ce dépôt contient mes travaux pratiques sur la reproductibilité logicielle et l'étude de la variabilité (INSA Rennes, Dept. INFO, 4e année, 2026-2027).

---

## 1. Architecture du dépôt

* `tp1et2/` : mes premiers programmes en C et en Python (associativité et problème du banquier), les conteneurs Docker et les scripts d'exécution.
* `tp3/` : l'étude systématique de la variabilité :
  * `model.uvl` : le modèle de variabilité écrit en UVL.
  * `configs/` : les configurations de mes trois programmes de référence (`.csvconf`).
  * `sample.py` et `sample.csv` : l'échantillonnage reproductible.
  * `assoc.py.jinja` et `generate.py` : la génération de variantes.
  * `cli.py` et `parameterized.py` : les mécanismes de variabilité par CLI et paramètres d'exécution.
  * `experiments/` : le moteur d'exécution (`run_experiments.py`, `runner.c`) et les résultats sérialisés (`results.csv`).
* `.github/workflows/` : les workflows d'intégration continue GitHub Actions.

---

