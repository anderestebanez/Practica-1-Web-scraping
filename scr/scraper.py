# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 00:16:50 2019

@author: Administrador
"""

#' @param estado The situation of the auction
#' @param tipo_Bien Type of property
#' @param provincia Province
#' @param fchFin Vector with the two date between the auction must finish 
#' @param fchIni Vector with the two date between the auction must start
#' @return Get a data.frame with the information of all the auctions.

import urllib3
import re
import time
import certifi
from bs4 import BeautifulSoup
from dateutil import parser
from reason_classifier import ReasonClassifier

class SubastaBOEScraper():
    
    
    def __init__(self):
        self.url = ""
        self.data = []
        self.estado=""
        self.tipo_Bien=""
        self.provincia = ""
        self.fchFin = ""
        self.fchIni = ""
        self.listSubastas = []
  
    # estado={"Cualquiera":"", "Prox. apertura":"PU","Celebrándose":"EJ","Suspendida":"SU","Cancelada":"CA","Concluida en Portal de Subastas":"PC","Finalizada por Autoridad Gestora":"FS"}
    # tipo_Bien={"Todos":"", "Vivienda":"501", "Local comercial":"502", "Garaje":"503", "Trastero":"504", "Nave industrial":"505", "Solar":"506", "Finca rústica":"507", "Otros":"599"}
    # provincia={'-- Todas --':"",'Álava':"01",'Albacete':"02",'Alicante':"03",'Almería':"04",'Ávila':"05",'Badajoz':"06",'Baleares':"07",'Barcelona':"08",'Burgos':"09",'Cáceres':"10",'Cádiz':"11",'Castellón':"12",'Ciudad Real':"13",'Córdoba':"14",'La Coruña':"15",'Cuenca':"16",'Gerona':"17",'Granada':"18",'Guadalajara':"19",'Guipúzcoa':"20",'Huelva':"21",'Huesca':"22",'Jaén':"23",'León':"24",'Lérida':"25",'La Rioja':"26",'Lugo':"27",'Madrid':"28",'Málaga':"29",'Murcia':"30",'Navarra':"31",'Orense':"32",'Asturias':"33",'Palencia':"34",'Las Palmas':"35",'Pontevedra':"36",'Salamanca':"37",'Santa Cruz de Tenerife':"38",'Cantabria':"39",'Segovia':"40",'Sevilla':"41",'Soria':"42",'Tarragona':"43",'Teruel':"44",'Toledo':"45",'Valencia':"46",'Valladolid':"47",'Vizcaya':"48",'Zamora':"49",'Zaragoza':"50",'Ceuta':"51",'Melilla':"52",'No consta':"00"}
    def setFilter(self, 
                  resetFilter=False, 
                  estado="", 
                  tipo_Bien="", 
                  provincia="", 
                  fchFin="", 
                  fchIni=""):
        if resetFilter==True:
            self.estado=estado
            self.tipo_Bien=tipo_Bien
            self.provincia=provincia
            self.fchFin=fchFin
            self.fchIni=fchIni
        else:
            if estado != "":
                self.estado=estado
            if tipo_Bien != "":
                self.tipo_Bien=tipo_Bien
            if provincia != "":
                self.provincia=provincia
            if fchFin != "":
                self.fchFin=fchFin
            if fchIni != "":
                self.fchIni=fchIni
        
        self.url = "".join(['https://subastas.boe.es/subastas_ava.php?',
                            'campo%5B0%5D=SUBASTA.ORIGEN&dato%5B0%5D=&',
                            'campo%5B1%5D=SUBASTA.ESTADO&dato%5B1%5D=',self.estado,'&',
                            'campo%5B2%5D=BIEN.TIPO&dato%5B2%5D=&dato%5B3%5D=',self.tipo_Bien,'&',
                            'campo%5B4%5D=BIEN.DIRECCION&dato%5B4%5D=&',
                            'campo%5B5%5D=BIEN.CODPOSTAL&dato%5B5%5D=&',
                            'campo%5B6%5D=BIEN.LOCALIDAD&dato%5B6%5D=&',
                            'campo%5B7%5D=BIEN.COD_PROVINCIA&dato%5B7%5D=',self.provincia,'&',
                            'campo%5B8%5D=SUBASTA.POSTURA_MINIMA_MINIMA_LOTES&dato%5B8%5D=&',
                            'campo%5B9%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_1&dato%5B9%5D=&',
                            'campo%5B10%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_2&dato%5B10%5D=&',
                            'campo%5B11%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_3&dato%5B11%5D=&',
                            'campo%5B12%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_4&dato%5B12%5D=&',
                            'campo%5B13%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_5&dato%5B13%5D=&',
                            'campo%5B14%5D=SUBASTA.ID_SUBASTA_BUSCAR&dato%5B14%5D=&',
                            'campo%5B15%5D=SUBASTA.FECHA_FIN_YMD&dato%5B15%5D%5B0%5D=&dato%5B15%5D%5B1%5D=&',
                            'campo%5B16%5D=SUBASTA.FECHA_INICIO_YMD&dato%5B16%5D%5B0%5D=&dato%5B16%5D%5B1%5D=&',
                            'page_hits=200&sort_field%5B0%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B0%5D=desc&sort_field%5B1%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B1%5D=asc&sort_field%5B2%5D=SUBASTA.HORA_FIN&sort_order%5B2%5D=asc&accion=Buscar'])

    def __download_html(self, url):

        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                           ca_certs=certifi.where())
        response = http.request('GET',url)
        if response.status==200:
            return response.data
        else:
            return None

    def getSubastaLink(self, url = "", listSubastas = None):
        if url == "":
            url=self.url
        
        if listSubastas == None:
            listSubastas=[]
            
        html = self.__download_html(url)
        bs = BeautifulSoup(html, 'html.parser')
        lis = bs.find_all(attrs={"class":"resultado-busqueda"})
        for li in lis:
            p = li.find_all("p")
            subastaLink = {"codSubasta":p[0].text.strip(' \n').encode('utf-8'),
                           "autoridad":p[1].text.strip(' \n').encode('utf-8')}
            
            if p[2].text.strip(' \n')[0:10]=="Expediente":
                subastaLink["expediente"]=p[2].text.strip(' \n')[12:].encode('utf-8')
                subastaLink["estado"]=p[3].text.strip(' \n')[8:].encode('utf-8')
                
            elif p[2].text.strip(' \n')[0:6]=="Estado":
                subastaLink["estado"]=p[2].text.strip(' \n')[8:].encode('utf-8')
            
            subastaLink["descripcion"]=li.find(attrs={"class":"documento"}).text.strip(' \n').encode('utf-8')
            subastaLink["link"]="https://subastas.boe.es"+li.find("a", href=True)["href"][1:]
            
            listSubastas.append(subastaLink)
        
        pagSig = bs.find(attrs={"class":"pagSig"})
    
        if pagSig is not None:
            self.getSubastaLink(url="https://subastas.boe.es/"+pagSig.find_parent("a", href=True)["href"],listSubastas=listSubastas) 
        
        self.listSubastas = listSubastas
        return len(self.listSubastas)
        
    def __evaluate_complexity(self):
        print("There are %d links. The expected time is %d seconds",[len(self.listSubastas),len(self.listSubastas)*3])
        return None

    #Este código scrapear estructuras estandars: InforGeneral, Autoridades, Administrador concursal y Bienes
    def __scrape_StructGeneral(self, urlSubasta):
        html = self.__download_html(urlSubasta)
        bs = BeautifulSoup(html, 'html.parser')
        
        infoGeneral={}
        
        trs=bs.find("table", attrs={"class":"datosSubastas"}).find_all("tr")
        for tr in trs:    
            infoGeneral[tr.find("th").text]=tr.find("td").text.strip("\n")
        
        return infoGeneral
    
    def __scrape_Pujas(self,urlSubasta):
        pujas=[]
        return pujas
        
    def __scrape_Lote(self,urlSubasta):
        lote=[]
        return lote
    
sub = SubastaBOEScraper()
sub.setFilter(resetFilter=True, provincia="48")
sub.getSubastaLink()

sub.__scrape_InfoGeneral(urlSubasta=sub.listSubastas[1]["link"])
sub.scrape_InfoGeneral(urlSubasta="https://subastas.boe.es/detalleSubasta.php?idSub=SUB-JA-2019-122911&ver=2&idBus=_bU05dlRNVnU0U0NtdjBCSzNnQ09DbHhwVzd4ME01bTEzS0IzajY2akRvRSsrQ0ZmQllYU3BUWGhVSWd1NU1NWnZ1bnlxNTFrbVNnTzI3SGlWOENtZkZUVWJ0bVFhY2QwbVh0cG1pdGpGWUYyekRFWmplT0xCS0dQZmhld25wajRVeUlnS21mMTlkdkF5d1Fyano0RG0zLzF3UDVtOG5zL0NveE15NmN0RUdGNlFYN2IwNTlJMlFyMU1odUpmU01UejRmc0VPZTVBMWhmUTRDeTBJY2phZWQzUXNQb1hab1JsdWMrVzVUV05PNjhQV1RPc2J5M2RJVi9Pd0p5NGk1dDRSRmFIRlJBbjk0RHFyVE40VnNTdEF6NUJiams2UHVtekNyOXh0S2xaSWM9&idLote=&numPagBus=")
b = {}
b["aaa"]="bbb"


###Test
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                           ca_certs=certifi.where())
response = http.request('GET',sub.listSubastas[1]["link"])
        
bs = BeautifulSoup(response.data, 'html.parser')

infoGeneral={}

a = bs.find("table", attrs={"class":"datosSubastas"}).find_all("tr")
a.find_all("th")
a.find_all("td")[1].text

