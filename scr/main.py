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

len(sub.listSubastas)
 
pickle.dump(sub.listSubastas,open(path+'/csv/20190414_listSubastas',"wb"))
sub.scrape(True)
save=sub.listSubastas
pickle.dump(sub.listSubastas,open(path+'/csv/20190414_listSubastas_scrape',"wb"))

sub.getErrors()
sub.data2csv(path+"/csv")

#data = pickle.load(open(path+'/csv/20191104_listSubastas',"rb"))


#Pruebas: revisar una subasta
#[sub.listSubastas.index(x) for x in sub.listSubastas if x.get('Identificador')=="SUB-AT-2019-19R0886002005"]
#sub.listSubastas[291]
