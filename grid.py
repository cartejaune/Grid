import requests
import pandas as pd
import time, json
from time import sleep
import ftx
import numpy as np
import os.path

#####################################################
#           GRID BY MR ROBOTS V5.0 23-01-22
#INSTALLATiON:
#Somme minimale en USD/USDT/BTC a mettre 
#dans votre sous-réperoire FTX : 
#400 X le montant minimal de SELL de la crypto sur FTX
#Ensuite acheter la 1/2 de ce montant en crypto
#
#Adapter les Variables ci dessous
#Installer sous un serveur Linux avec PYTHON3
#Installer une règle crontab
# * * * * * chemindevotrefichier/grid.py
#
# Si vous aimez ce script offrez moi un café
# BNB => 0xc815a83FB34DA7A2d2540D98f3E93e21Ac7bf2c3
#
###################VARIABLES A ADAPTER ##############
accountName = 'NOMSOUSREP'     # Nom Sous repertoire FTX
pairSymbol = 'STEP/USD'  # Paire tradée
fiatSymbol = 'USD'       # FIAT utilisé
cryptoSymbol = 'STEP'     # Crypto Utilisée
pourcent=0.01             # Pourcentage de la Grille 
#####################################################
#liaison avec la plateforme FTX
########## ADAPTER VOS CLES DE SOUS REPERTOIRE ICI  ####################################################
client = ftx.FtxClient(api_key='VOTRE_CLE_API_ICI',
                   api_secret='VOTRE_SECRET_KEY_ICI', subaccount_name=accountName)
#######################################################################################################

"""
Prix haur mois – prix bas mois = X
1% du prix actuel = …/100
X/ par ce résultat = nbr de pourcent
Nombre de token/ nbr de pourcent arrondit au mini demandé
"""

# NE RIEN TOUCHER CI DESSOUS #

creersell=False
creerbuy=False
nomok=accountName+'ok.txt'
nomtexte=accountName+'texte.txt'


#recupération du dataset => partie NON UTILISE POUR FUTUR DEVELOP
data = client.get_historical_data(
    market_name=pairSymbol, 
    resolution=86400, 
    limit=60, 
    start_time=float(round(time.time()))-60*86400, 
    end_time=float(round(time.time())))
df = pd.DataFrame(data)

df = df.set_index(df['time'])
df.index = pd.to_datetime(df.index, unit='ms')
del df['time']
del df['startTime']
df['MAX'] = df['close'].rolling(30).max()
df['MIN'] = df['close'].rolling(30).min()
df['1%'] = df['close']/100
df['DELTA']=(df['MAX']-df['MIN'])/df['1%']

balance = client.get_balances()
print(balance)
coin_total = next((b['total'] for b in balance if b['coin'] == cryptoSymbol))
df['ACHAT']=round(coin_total/df['DELTA'],1)

achat=df['ACHAT'].iloc[-1]
print('quantité a acheter:',achat)
#df


if os.path.isfile(nomok):
    print ("File exist")
    fichier = open(nomok,'rt')
    texte = fichier.read()
    if not texte:
      print('Variable not exist')
      s = str(0)
      fichier = open(nomok,'wt')
      fichier.write(s)
      fichier.close()
      fichier = open(nomok,'rt')
      texte = fichier.read()
      OK = float(texte)    
      print("OK=",OK)
    else: 
      OK = float(texte)    
      print("OK=",OK)
else:
    print ("File not exist")
    OK=0    


if OK==1 and  os.path.isfile(nomtexte):#on recupere les ordres FTX et on vérifie si il existe
  label='https://ftx.com/api/markets/'+pairSymbol
  fichier = open(nomtexte,'rt')
  texte = fichier.read()
  W = float(texte)
  print("Valeur ancienne",W)
  try:
      btc_new = requests.get(label).json()
      print("Valeur actuelle",btc_new['result']['price'])
  except Exception as e:
      print(f'Error obtaining BTC old data: {e}')

  percent = ((float(btc_new['result']['price']) - float(W)) / float(W))*100    

  print("Delta actuel: ",percent,' %')
#analyse des ordres
  try:
    r = client.get_open_orders(pairSymbol)
    print(r)
  except Exception as e:
    print(f'Error obtaining BTC old data: {e}')

  df2 = pd.DataFrame(r)
  print(df2)
  print(len(df2.index))
  """
  for index, row in df2.iterrows():
    if row['side']== 'sell':
      print('exite un avis SELL')
      creersell=True
    if row['side']== 'buy':
      print('exite un avis buy')
      creerbuy=True      
  if creerbuy==False or creersell==False:
    print('IL Y A UN ORDRE EXECUTE')  
    try:
      r = client.cancel_orders(pairSymbol)
      print(r)
      s = str(0)
      fichier = open(nomok,'wt')
      fichier.write(s)
      fichier.close()  
    except Exception as e:
      print(f'Error obtaining BTC old data: {e}')
    """

  if len(df2.index)<10:
    print('IL Y A UN ORDRE EXECUTE')  
    try:
      r = client.cancel_orders(pairSymbol)
      print(r)
      s = str(0)
      fichier = open(nomok,'wt')
      fichier.write(s)
      fichier.close()  
    except Exception as e:
      print(f'Error obtaining BTC old data: {e}')
  else:
    print('Ordres toujours en cours')

if os.path.isfile(nomok):
  fichier = open(nomok,'rt')
  texte = fichier.read()
  OK = float(texte)    
  print("OK=",OK)
  time.sleep(1)

if OK!=1 or not os.path.isfile(nomtexte): # on redémarre une grille
  try:
      label='https://ftx.com/api/markets/'+pairSymbol
      btc_old = requests.get(label).json()
      print("Valeur actuelle",btc_old['result']['price'])
      valeur = btc_old['result']['price']
      print('GENERATION NOUVELLE VALEUR =>Valeur=',valeur)
      s = str(valeur)
      fichier = open(nomtexte,'wt')
      fichier.write(str(valeur))
      fichier.close()
      s = str(1)
      fichier = open(nomok,'wt')
      fichier.write(s)
      fichier.close()
      fichier = open(nomok,'rt')
      texte = fichier.read()
      OK = float(texte)
      print("OK=",OK)
  except Exception as e:
      print(f'Error obtaining BTC old data: {e}') 

  for i in range(1,6):
    pplus = valeur + pourcent*i*valeur  
    pmoins = valeur - pourcent*i*valeur
    try:
      btc_place = requests.get(label).json()
      r = client.place_order(pairSymbol, "buy",pmoins,achat,"limit")
      print(r)
      r = client.place_order(pairSymbol, "sell",pplus,achat,"limit")
      print(r)
      s = str(1)
      fichier = open(nomok,'wt')
      fichier.write(s)
      fichier.close()
    except Exception as e:
      print(f'Error making order request: {e}')    

"""
Notes : 
ce script va creer a la racine serveur des fichiers txt de données, 
qui se nommeront NOMDEVOTRESOUSREPERTOIRE+ok.txt et NOMDEVOTRESOUSREPERTOIRE+texte.txt
Ne les effacer que quand vous n'utiliserez plus le script

LOG
Version 5: passage a un grille pour profiter des filantes + mofification de la vérification des ordres.
version 4: passage des infos en variable + ajout d'une variation du montant Achat vente en fonction des plus haut et bas du mois
Version 3: passage ordre limite dans le carnet et check si ordre by sell existant
Version 2 : Buy Sell limit 2 % en fonction de prix
Version 1 : Il enregistre le prix courant, puis vérifiera si on est supérieur ou inférieur de 1% et passera un ordre

"""
