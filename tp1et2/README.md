# Associativité :
Résultat attendu après l'exécution du fichier "main" :
- en C : ~75 % ;
- en Python : ~80 %.

# Problème du banquier :
Résultat attendu après l'exécution du fichier "banking" :
- en C : -4396803930182068517325088235103664583272782888960.000000 ;
- en Python : -4.3968039301820685e+48.


# Exécution avec Docker :
## En Python :
- aller dans le sous dossier `python/`.
## En C :
- aller dans le sous dossier `c/`.
## Puis :
- build : `docker build -t rep-lab2 .` ;
- run : `docker run --rm -v "$(pwd)/out":/app/out:z rep-lab2` (à noter que cette commande marche avec Fedora, le `:z` dit à SELinux d'autoriser l'accès aux fichiers ;
- les fichiers sont à présent dans `out/`.
