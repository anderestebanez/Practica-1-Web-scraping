# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 20:14:27 2019

@author: Administrador
"""
import sys
sys.path.append('C:/Users/Administrador.WIN-K4PA08MDFCA/Documents/UOC/Ciclo de vida de los datos/Practica-1-Web-scraping')

from scr.scraper import SubastaBOEScraper

output_file = "dataset.csv"

sub = SubastaBOEScraper()

sub.setFilter(provincia="08")
sub.getSubastaLink()
lsBcn=sub.listSubastas

sub.setFilter(provincia="43")
sub.getSubastaLink()
lsTar=sub.listSubastas

sub.setFilter(provincia="17")
sub.getSubastaLink()
lsGir=sub.listSubastas

sub.setFilter(provincia="25")
sub.getSubastaLink()
lsLle=sub.listSubastas

lsTot=lsBcn+lsTar+lsGir+lsLle
len(lsTot)
sub.setListSubasta(lsTot)
sub.scrape()

#Ejemplo 20 subastas Tarragona
sub.setListSubasta(lsTar[0:20])
sub.scrape()

import pickle
filehandle = open('C:/Users/Administrador.WIN-K4PA08MDFCA/Documents/UOC/Ciclo de vida de los datos/Practica-1-Web-scraping/csv/output',"wb")
pickle.dump(sub.listSubastas,filehandle)
#filehandle = open('C:/Users/Administrador.WIN-K4PA08MDFCA/Documents/UOC/Ciclo de vida de los datos/Practica-1-Web-scraping/csv/output',"rb")
#pickle.load(filehandle)