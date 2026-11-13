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
  * `experiments/` : le moteur d'exécution (`run_experiments.py`, `runner.c`), les résultats sérialisés (`results.csv`) et le notebook d'analyse (`analysis.ipynb`).
* `.github/workflows/` : les workflows d'intégration continue GitHub Actions.

---

## 2. Documentation détaillée

Des fichiers `README.md` plus détaillés sont disponibles plus loin dans l'arborescence :
* [`tp3/README.md`](tp3/README.md) : **compte-rendu complet du TP3** détaillant l'ensemble des parties (matrice de variabilité, modèle UVL, échantillonnage, sérialisation des variantes, intégration continue GitHub Actions, analyse statistique et déclaration d'usage de l'IA).
* [`tp3/experiments/README.md`](tp3/experiments/README.md) : guide d'exécution du dossier d'expérimentation, explication du `requirements.txt` et lancement du notebook.
* [`tp1et2/README.md`](tp1et2/README.md) : documentation des deux premiers travaux pratiques (associativité, banquier et Docker).


## Déclaration d'utilisation de l'IA 

* **Outils et modèles utilisés** :
  * Gemini 3.6 Flash (High) pour la génération du programme en C du Lab 2.
  * Gemini 4 Hydrogen (High) pour la génération du programme en Python du Lab 3.
  * Antigravity pour l'assistance à la formalisation UVL, la conception du runner et l'analyse statistique.
* **Ce qui a été généré** :
  * Les codes sources `tp1et2/c/associativity_llm.c` et `tp1et2/python/associativity_llm.py`.
  * La matrice de variabilité et les fonctions de calcul statistique du notebook.
* **Ce que j'ai vérifié** :
  * J'ai relu et vérifié chaque ligne de code générée.
  * J'ai exécuté tous les programmes localement et contrôlé la validité numérique des résultats.

