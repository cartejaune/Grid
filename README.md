# Grid ![Latest Stable Version](https://img.shields.io/badge/Version-5.0-yellow)



## Python FTX Grid BOT

Requis :

unbutu >= 18.04

>pip install pandas

>pip install requests

>pip install ftx

>pip install dill



## Version 5.0

Grid Bot basic en Python

A lancer en tache cron toute les minutes

Il enregistre le prix courant, puis vérifiera si on un ou des ordres ont été exécuté. 

Si oui il regarde le prix courant et regénèe un grid

A tester sur un coin par cher avec un petit montant et ensuite à vous de voir



##           GRID BY MR ROBOTS V5.0 23-01-22
INSTALLATiON:

Somme minimale en USD/USDT/BTC a mettre 
dans votre sous-réperoire FTX : 
mettre 400 X le montant minimal de SELL de la crypto sur FTX
Ensuite acheter la 1/2 de ce montant en crypto

Adapter les Variables du script python

Installer sous un serveur Linux avec PYTHON3
Installer une règle crontab pour chaque minute




```php

* * * * * chemindevotrefichier/grid.py

```

:+1: 


![FTX GRID](https://raw.githubusercontent.com/cartejaune/Grid/main/Capture.JPG)



# MAJ

version 6: EN DEVELOP 

Version 5: passage a un grille pour profiter des filantes + mofification de la vérification des ordres.

version 4: passage des infos en variable + ajout d'une variation du montant Achat vente en fonction des plus haut et bas du mois

Version 3: passage ordre limite dans le carnet et check si ordre by sell existant

Version 2 : Buy Sell limit 2 % en fonction de prix

Version 1 : Il enregistre le prix courant, puis vérifiera si on est supérieur ou inférieur de 1% et passera un ordre


++ Mr Robot
