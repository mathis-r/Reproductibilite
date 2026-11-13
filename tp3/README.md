# TP3 - Reproductibilité et Variabilité

## Partie 1 - Trois programmes et matrice de variabilité

J'ai sélectionné trois programmes pour étudier l'associativité de l'addition `(x + y) + z == x + (y + z)` :

1. **Mon programme fait main en Python (`tp1et2/python/main.py`)** :
   J'ai écrit ce programme lors du premier TP. Il effectue 100 séries de 100 tirages aléatoires. Il donne environ $82.33\%$ de réussite.
2. **Le programme C généré par LLM (`tp1et2/c/associativity_llm.c`)** :
   J'ai demandé à Gemini 3.6 Flash de produire un programme en C lors du Lab 2. Il utilise des flottants simple précision et un générateur maison `xorshift32`. Il donne environ $93.0\%$ de réussite.
3. **Le nouveau programme Python généré par LLM (`tp1et2/python/associativity_llm.py`)** :
   J'ai demandé à Gemini 4 Hydrogen de produire un programme en Python pour ce TP3. Il teste 1 000 000 de répétitions avec une graine fixée. Il donne $82.85\%$ sur une distribution uniforme et $68.12\%$ sur une distribution gaussienne.

### Matrice de comparaison des facteurs

| Facteur de variabilité | Mon programme Python | LLM en C | LLM en Python | Impact observé |
|---|---|---|---|---|
| **Langage** | Python | C | Python | Faible impact direct. |
| **Précision** | Double précision | Simple précision | Double précision | Fort impact. La simple précision perd ses bits plus vite. |
| **Distribution** | Uniforme $[0, 1[$ | Uniforme $[-1, 1]$ | Uniforme $[0, 1[$ et Gaussienne | Impact majeur. L'écart atteint 15 points. |
| **Tirage aléatoire** | `random.random()` | `xorshift32()` | `random.random()` / `random.gauss()` | Faible impact sur la moyenne. |
| **Graine (`seed`)** | Non fixée | `time(NULL)` | Fixée (`seed(42)`) | Permet la reproductibilité exacte de la run. |
| **Nombre de répétitions** | 10 000 | 10 000 000 | 1 000 000 | Réduit la variance. Stabilise la moyenne. |
| **Optimisation compilateur** | Aucune | `-O2` | Aucune | `-ffast-math` en C force le résultat à 100%. |
| **Résultat obtenu** | $\approx 82.33\%$ | $\approx 93.0\%$ | $82.85\%$ (U) / $68.12\%$ (G) | Forte variabilité selon les choix faits. |

### Ce que le 3e programme m'a appris

Entre mon premier programme Python et le programme C du LLM, trop de paramètres changent en même temps.
On ne peut pas savoir ce qui cause les écarts.

Le 3e programme (LLM en Python) garde le même langage et la même précision :
* **Stabilisation du résultat** : passer de 10 000 à 1 000 000 de tirages stabilise la valeur autour de $82.8\%$.
* **Effet de la distribution** : avec le même code Python, la distribution uniforme donne $82.85\%$, mais la distribution gaussienne donne $68.12\%$. La forme des données a donc un effet massif sur le résultat.
* **Reproductibilité** : fixer la graine aléatoire permet d'obtenir exactement le même pourcentage à chaque exécution.

---

## Partie 2 - Une autre propriété mathématique sur une branche Git

J'ai créé une branche Git nommée `variabilite`.

Sur cette branche, j'ai remplacé l'associativité par la distributivité de la multiplication sur l'addition dans le fichier `tp1et2/c/main.c` :
`x * (y + z) == x * y + x * z`

J'ai poussé cette branche sur GitHub. Le workflow GitHub Actions a exécuté le code. Il a produit un résultat différent de l'associativité. Cela prouve que la propriété mathématique testée est un facteur de variabilité direct.

---

## Partie 3 - Mécanismes de variabilité

Les différents mécanismes explorés sont :
1. **Paramètres d'exécution (`tp3/parameterized.py`)** :
   Une boucle interne fait varier le nombre de répétitions de 100 à 1 000 000 dans une seule exécution.
2. **Interface en ligne de commande (`tp3/cli.py`)** :
   Le script lit ses paramètres depuis la ligne de commande grâce à `argparse` (`--repetitions`, `--minrand`, `--maxrand`). Un script externe peut ainsi l'appeler plusieurs fois.
3. **Génération de code (`tp3/generate.py` et `tp3/assoc.py.jinja`)** :
   Un template Jinja permet de générer des fichiers sources Python. Le script instancie automatiquement plusieurs variantes en combinant les propriétés et les types de précision (`float`, `np.float32`, `np.float16`, `np.float128`).
4. **Environnement et compilation (`tp3/Dockerfile` et GitHub Actions)** :
   Le conteneur Docker et la matrice GitHub Actions permettent de tester différentes versions du moteur d'exécution et différents compilateurs.

---

## Partie 4 - Modélisation de la variabilité (UVL)

J'ai modélisé tous les facteurs de variabilité dans le fichier `tp3/model.uvl`.

Le modèle contient :
* **Propriété** : `AssocAdd`, `AssocMul`, `Distributivity`, `InverseMul` (4 choix).
* **Précision** : `SinglePrecision`, `DoublePrecision` (2 choix).
* **Répétitions** : `N1000`, `N10000`, `N100000`, `N1000000` (4 choix).
* **Distribution** : `Uniform01`, `UniformNeg1Pos1`, `Gaussian` (3 choix).
* **Langage** : `C`, `Python` (2 choix).
* **Environnement** :
  * Architecture : `x86_64`, `arm64` (2 choix).
  * Version du runtime : `RuntimeV1`, `RuntimeV2` (2 choix).
  * Optimisation : `O0`, `O2`, `O3`, `FastMath` (optionnel pour C).

### Contraintes logiques
* `Optimization => !Python` : Python n'utilise pas les options du compilateur C.
* `FastMath => SinglePrecision` : FastMath s'applique sur la simple précision.

### Calcul du nombre de configurations à la main

1. **Configurations Python** :
   $$4 \times 2 \times 4 \times 3 \times 1 \times 2 \times 2 \times 1 = 384$$
2. **Configurations C en simple précision** :
   5 choix d'optimisation possibles (aucune, O0, O2, O3, FastMath).
   $$4 \times 1 \times 4 \times 3 \times 1 \times 2 \times 2 \times 5 = 960$$
3. **Configurations C en double précision** :
   FastMath est interdit, donc 4 choix d'optimisation possibles (aucune, O0, O2, O3).
   $$4 \times 1 \times 4 \times 3 \times 1 \times 2 \times 2 \times 4 = 768$$

**Total calculé à la main** : $384 + 960 + 768 = 2112$ configurations valides.

Même nombre sur l'onglet 'Analysis' sur le site.

---

## Partie 5 - Échantillonnage reproductible

Le nombre total de configurations est trop grand pour tout exécuter.
On produit un échantillon représentatif et reproductible avec `tp3/sample.py`.

1. J'ai créé trois fichiers d'ancrage dans `tp3/configs/` pour représenter mes trois programmes :
   * `prog1_python_manual.csvconf`
   * `prog2_c_llm.csvconf`
   * `prog3_python_llm.csvconf`
2. J'ai généré l'échantillon avec la commande suivante :
   ```bash
   tp3/.venv/bin/python tp3/sample.py tp3/model.uvl --size 30 --seed 1 --include tp3/configs/*.csvconf -o tp3/sample.csv
   ```

Le fichier `tp3/sample.csv` contient 33 configurations au total (les 3 ancres en tête et 30 configurations tirées au sort). Grâce à la graine `--seed 1`, cet échantillon est strictement reproductible.

---

## Partie 6 - Sérialisation des résultats

J'ai automatisé l'exécution de tout l'échantillon avec le script `tp3/experiments/run_experiments.py`.
Le dossier `tp3/experiments/` isole cette chaîne d'exécution.

1. **Extraction du code C** :
   Le template du code C est dans le fichier `tp3/experiments/runner.c`.
   Le script Python appelle `gcc` à la volée. Il applique les options d'optimisation demandées (`-O0`, `-O2`, `-O3`, `-ffast-math`).
2. **Exécution Python** :
   Pour Python, le script évalue les expressions avec NumPy de façon vectorisée. Il gère la simple précision (`float32`) et la double précision (`float64`).
3. **Répétitions et reproductibilité** :
   Chaque configuration tourne 3 fois de suite avec une graine pseudo-aléatoire contrôlée. Cela permet de mesurer la stabilité du résultat.
4. **Sérialisation des résultats** :
   Le script écrit chaque exécution dans `tp3/experiments/results.csv`.
   Chaque ligne contient les facteurs de la configuration, l'identifiant du run, le pourcentage obtenu, la durée en millisecondes et l'architecture de la machine hôte.

Commande pour lancer l'expérimentation :
```bash
tp3/.venv/bin/python tp3/experiments/run_experiments.py --sample tp3/sample.csv --output tp3/experiments/results.csv --runs 3
```

Sur 99 exécutions (33 configurations $\times$ 3 répétitions), le temps total est d'environ 3 secondes.
Un résultat marquant apparaît tout de suite : l'option `-ffast-math` en C force le résultat à $100.0\%$, car le compilateur réécrit l'égalité mathématique lors de la compilation.
