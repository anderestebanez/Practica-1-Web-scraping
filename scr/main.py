# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 20:14:27 2019

@author: Ander Estebanez Centeno
"""
#  Cambio de PYTHONPATH para poder importar las clases
import sys
import pandas as pd

path="C:/Users/Administrador.WIN-K4PA08MDFCA/Documents/UOC/Ciclo de vida de los datos/Practica-1-Web-scraping"
sys.path.append(path)
from scr.scraper import SubastaBOEScraper
from scr.download_html import download_html
import pickle

#  Importar las listas de user-agent y proxys
agents = pd.read_excel(path+"/input/user_agent.xlsx")
agents = agents.to_dict(orient="records")

proxys = pd.read_excel(path+"/input/proxys.xlsx")
proxys = proxys.to_dict(orient="records")

#  Se deine el dataset de salidaa
output_file = "dataset.csv"

#  Se iniciala  clase
http = download_html(incognito=True, proxys=proxys, agents=agents,rSeed=120)
sub = SubastaBOEScraper(http=http)

#  Se crea el filtro de la provincia y luego se descarga el listado de subastas.
#  A partir del primero se ejecuta con el anterior listSubasta de forma que se agreguen
sub.setFilter(provincia="08") #  Barcelona
sub.getSubastaLink()

sub.setFilter(provincia="43") #  Tarragona
sub.getSubastaLink(listSubastas=sub.listSubastas)

sub.setFilter(provincia="17") #  Girona
sub.getSubastaLink(listSubastas=sub.listSubastas)

sub.setFilter(provincia="25") #Lleida
sub.getSubastaLink(listSubastas=sub.listSubastas)

lsCat = sub.listSubastas
len(sub.listSubastas)
 
pickle.dump(sub.listSubastas,open(path+'/csv/20191104_listSubastas',"wb"))
sub.setListSubasta(sub.listSubastas[0:200])
sub.scrape()
pickle.dump(sub.listSubastas,open(path+'/csv/20191104_listSubastas_scrape',"wb"))

data = pickle.load(open(path+'/csv/20191104_listSubastas',"rb"))


save=sub.listSubastas
len(save)
sub.data2csv(path+"/csv")
sub.setListSubasta(sub.listSubastas)
sub.scrape()
sub.listSubastas[18:19]

a='Datos registrales: Finca 3024 de ALP, insctita en el registro propiedad Puigcerdà, Tomo 601, libro 39, folio 29. Finca urbana: entidad nº64 de edificio "Orbis Holidays" compuesto de dos cuerpos, letras A y B sito en Super Molina municipio de Alp: cuarto trasero en planta 2ª alta, cuerpo B; de unos 13 metros cuadrados aprox. Linda Norte, entidad nº65 de la misma planta;  Suy y Este vuelo de terreno común; y Oeste, escalera y pasillo de la planta en que està situado, cuota:  10 centèsimes por ciento (0.10%), respecto del total del inmueble que es finca nº2123, al folio 37 del libro 38º de Alp, tomo 600 del archivo. La finca no està coordinada gráficamente en el catastro'
a[:a.find("\n")]
a.strip("\n")
a.replace(";",",")