# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 20:14:27 2019

@author: Ander Estebanez Centeno
"""
#  Cambio de PYTHONPATH para poder importar las clases
import sys
import pandas as pd

path="C:/Users/Administrador.WIN-K4PA08MDFCA/Documents/UOC/Semestres_Anteriores/Ciclo de vida de los datos/Practica-1-Web-scraping"
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

sub.setFilter(provincia="08", fchIni="2019-01-01", fchFin="2021-04-28") #  Barcelona
sub.getSubastaLink()

sub.setFilter(provincia="43", fchIni="2019-01-01", fchFin="2021-04-28") #  Tarragona
sub.getSubastaLink(listSubastas=sub.listSubastas)

sub.setFilter(provincia="17", fchIni="2019-01-01", fchFin="2021-04-28") #  Girona
sub.getSubastaLink(listSubastas=sub.listSubastas)

sub.setFilter(provincia="25", fchIni="2019-01-01", fchFin="2021-04-28") #Lleida
sub.getSubastaLink(listSubastas=sub.listSubastas)

len(sub.listSubastas)
 
pickle.dump(sub.listSubastas,open(path+'/csv/20210428_listSubastas',"wb"))
sub.scrape(True)
save=sub.listSubastas
pickle.dump(sub.listSubastas,open(path+'/csv/20210428_listSubastas_scrape',"wb"))


############
listSubastas = pickle.load(open(path + '/csv/20210428_listSubastas_scrape',"rb"))
listSubastas_v0 = pickle.load(open(path+'/csv/20190414_listSubastas_scrape',"rb"))
lsSubastas = [l["codSubasta"] for l in listSubastas]
listSubastas_v0 = [l for l in listSubastas_v0 if l["codSubasta"] not in lsSubastas]
len(listSubastas_v0)
len(listSubastas)
listSubastas = listSubastas_v0 + listSubastas
sub.setListSubasta(listSubastas)

sub.getErrors()
sub.data2csv(path+"/csv")

[l["codSubasta"] for l in listSubastas if "2017-56597" in l["codSubasta"]]


# data = pickle.load(open(path+'/csv/20210428_listSubastas_scrape',"rb"))
# sub.setListSubasta(data)


#Pruebas: revisar una subasta
#[sub.listSubastas.index(x) for x in sub.listSubastas if x.get('Identificador')=="SUB-AT-2019-19R0886002005"]
#sub.listSubastas[291]
