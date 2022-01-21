import requests
import pandas as pd
import time, json
from time import sleep
import ftx
import numpy as np

accountName = 'NOM_DE_VOTRE_SOUS_REPERTOIRE'
pairSymbol = 'AKRO/USDT'
fiatSymbol = 'AKRO'
cryptoSymbol = 'AKRO'


#liaison avec la plateforme
client = ftx.FtxClient(api_key='VOTRE_CLE_API',
                   api_secret='VOTRE_CLE_SECRET_API', subaccount_name=accountName)

#recupération du dataset
data = client.get_historical_data(
    market_name=pairSymbol, 
    resolution=60, 
    limit=1000, 
    start_time=float(round(time.time()))-1000*60, 
    end_time=float(round(time.time())))
df = pd.DataFrame(data)

df = df.set_index(df['time'])
df.index = pd.to_datetime(df.index, unit='ms')
del df['time']
del df['startTime']
df




fichier = open("ok.txt",'rt')
texte = fichier.read()
if not texte:
  print('Variable not exist')
  s = str(0)
  fichier = open("ok.txt",'wt')
  fichier.write(s)
  fichier.close()
  fichier = open("ok.txt",'rt')
  texte = fichier.read()
  OK = float(texte)    
  print("OK=",OK)
else: 
  OK = float(texte)    
  print("OK=",OK)


if OK==1 :#on a déjà récupérer une valeur on la compare
  fichier = open("texte.txt",'rt')
  texte = fichier.read()
  W = float(texte)
  print("Valeur ancienne",W)
  try:
      btc_new = requests.get('https://ftx.com/api/markets/AKRO/USDT').json()
      print("Valeur actuelle",btc_new['result']['ask'])
  except Exception as e:
      print(f'Error obtaining BTC old data: {e}')

  percent = ((float(btc_new['result']['ask']) - float(W)) / float(W))*100    

  print("Delta actuel: ",percent,' %')

  if percent <-1:
    print(f'The trade requirement was satisfied. Percentage move is at {percent}')
    try:
      btc_place = requests.get('https://ftx.com/api/markets/AKRO/USDT').json()
      r = client.place_order("AKRO/USDT", "buy",btc_place['result']['ask'],1,"limit")
      print(r)
      s = str(0)
      fichier = open("ok.txt",'wt')
      fichier.write(s)
      fichier.close()
    except Exception as e:
      print(f'Error making order request: {e}')  
  elif percent >1:
    print(f'The trade requirement was satisfied. Percentage move is at {percent}')
    try:
      btc_place = requests.get('https://ftx.com/api/markets/AKRO/USDT').json()
      prix=float(float(btc_place['result']['bid']))
      r = client.place_order(
            market="AKRO/USDT", 
            side="sell", 
            price=prix, 
            size=float(1), 
            type='limit',
            post_only= False
            )
      #r = client.place_order("AKRO/USDT", "sell",float(btc_place['result']['bid']),float(1),"limit",'','',bool(false))
      print(r)
      s = str(0)
      fichier = open("ok.txt",'wt')
      fichier.write(s)
      fichier.close()
    except Exception as e:
      print(f'Error making order request: {e}')  
  else:
      print('RIEN A SIGNALER pour INSTANT')

if OK!=1 :
  try:
      btc_old = requests.get('https://ftx.com/api/markets/AKRO/USDT').json()
      print("Valeur actuelle",btc_old['result']['ask'])
      valeur = btc_old['result']['ask']
      print('GENERATION NOUVELLE VALEUR =>Valeur=',valeur)
      s = str(valeur)
      fichier = open("texte.txt",'wt')
      fichier.write(str(valeur))
      fichier.close()
      s = str(1)
      fichier = open("ok.txt",'wt')
      fichier.write(s)
      fichier.close()
      fichier = open("ok.txt",'rt')
      texte = fichier.read()
      OK = float(texte)
      print("OK=",OK)
  except Exception as e:
      print(f'Error obtaining BTC old data: {e}')    
#fichier = open("texte.txt",'rt')
#texte = fichier.read()
#print(texte)
#W = float(texte)
#W=W + 10
#print(W)
#df
