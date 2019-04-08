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
import time
import certifi
from bs4 import BeautifulSoup
#import pandas as pd
import numpy as np
from scr.download_html import download_html
#from dateutil import parser
#from reason_classifier import ReasonClassifier



class SubastaBOEScraper():
    
    def __init__(self, http=None):
        self.url = ""
        self.data = []
        self.estado=""
        self.tipo_Bien=""
        self.provincia = ""
        self.fchFin = ""
        self.fchIni = ""
        self.listSubastas = []
        if http==None:
            self.http=download_html()
        else:
            self.http=http
            
  
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

    def __download_html(self, url, sleep=0):

        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                           ca_certs=certifi.where())
        response = http.request('GET',url)
        if response.status==200:
            return response.data
            time.sleep(sleep)
        else:
            return None

    def getSubastaLink(self, url = "", listSubastas = None):
        if url == "":
            url=self.url
        
        if listSubastas == None:
            listSubastas=[]
        
        self.http.setURL(url)
        self.http.setTiempo(1)
        html = self.http.getHtml()
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
        
    def setListSubasta(self, listSubastas):
        subastas=[]
        
        for subasta in listSubastas:
            if "codSubasta" in subasta and "link" in subasta and "estado" in subasta:
                subastas.append(subasta)
        
        print("Del total de  %d subastas, %d han sido descartados por no disponer de información básica"%(len(listSubastas), len(listSubastas)-len(subastas)))
        self.listSubastas=subastas
    
    def __evaluate_complexity(self):
        sec_tot = len(self.listSubastas)*2.5
        horas = int(sec_tot/(60*60))
        minu = int(sec_tot/60)-horas*60
        sec = sec_tot-minu*60-horas*60*60
        
        print("There are %d links. The expected time is %d:%d:%d"%(len(self.listSubastas),horas,minu,sec))
        return None

    #Este código scrapear estructuras estandars: InforGeneral, Autoridades, Administrador concursal y Bienes
    def __scrape_StructGeneral(self, urlSubasta):
        self.http.setURL(urlSubasta)
        self.http.setTiempo(0)
        html = self.http.getHtml()
        
        if html==None:
            return {"Scrap":False}
        
        bs = BeautifulSoup(html, 'html.parser')
        
        infoGeneral={}
        trs=bs.find("table", attrs={"class":"datosSubastas"}).find_all("tr")
        for tr in trs:    
            infoGeneral[tr.find("th").text]=tr.find("td").text.strip("\n")
        
        return infoGeneral
    
    def __scrape_Pujas(self,urlSubasta):
        self.http.setURL(urlSubasta)
        self.http.setTiempo(0)
        html = self.http.getHtml()
        if html==None:
            return {"Scrap":False}
        
        bs = BeautifulSoup(html, 'html.parser')
        
        pujas=[]        
        
        if bs.find("div", attrs={"class":"bloqueSubasta"}).find("span", attrs={"class":"destaca"}) != None:
            pujas = [{"Lote": "0", "Puja": bs.find("div", attrs={"class":"bloqueSubasta"}).find("span", attrs={"class":"destaca"}).text}]
        elif bs.find("div", attrs={"class":"bloqueSubasta"}).find("p").text == "La subasta no ha recibido pujas.":
            pujas = [{"Lote": "0", "Puja":"0"}]
        elif bs.find("table", attrs={"title":"Lista de pujas"}) != None:
            trs = bs.find("table", attrs={"title":"Lista de pujas"}).find("tbody").find_all("tr")
            for tr in trs:    
                puja = {"Lote":tr.find_all("td")[0].text,"Puja":tr.find_all("td")[1].text}
                pujas.append(puja)    
        return pujas
        
    def __scrape_Lote(self,urlSubasta):
        self.http.setURL(urlSubasta)
        self.http.setTiempo(0.5)
        html = self.http.getHtml()
        if html==None:
            return {"Scrap":False}
        bs = BeautifulSoup(html, 'html.parser')
        
        lotes=[]
        
        lis=bs.find("ul", attrs={"class":"navlistver2"}).find_all("li")
        
        for li in lis:
            url = "https://subastas.boe.es"+li.find("a", href=True)["href"][1:]
            nLote=li.find("a", href=True).text
            lote={"Lote":nLote}
            
            self.http.setURL(url)
            self.http.setTiempo(0)
            html = self.http.getHtml()
            if html==None:
                return {"Scrap":False}
            
            bs = BeautifulSoup(html, 'html.parser')
            
            tables=bs.find_all("table", attrs={"class":"datosSubastas"})
            for table in tables:
                trs = table.find_all("tr")
                for tr in trs:    
                    lote[tr.find("th").text]=tr.find("td").text.strip("\n")
            lotes.append(lote)       
        
        return lotes
    
        
    def __scrape_Interesados(self,urlSubasta):
        self.http.setURL(urlSubasta)
        self.http.setTiempo(0.5)
        html = self.http.getHtml()        
        if html==None:
            return {"Scrap":False}
        bs = BeautifulSoup(html, 'html.parser')
        
        interesados=[]
        
        tables=bs.find_all("table", attrs={"class":"datosSubastas"})
        for table in tables:
            interesado = {}
            trs = table.find_all("tr")
            for tr in trs:    
                interesado[tr.find("th").text]=tr.find("td").text.strip("\n")
            interesados.append(interesado)       
    
        return interesados
    
    def __scrape_execute(self,argument, url):
        
        if argument=="Información general": 
            return self.__scrape_StructGeneral(url)
        elif argument=="Autoridad gestora": 
            return {"autorida":self.__scrape_StructGeneral(url)}
        elif argument=="Bienes": 
            return {"bienes":self.__scrape_StructGeneral(url)}
        elif argument=="Acreedor": 
            return {"acreedor":self.__scrape_StructGeneral(url)}
        elif argument=="Administrador concursal": 
            return {"administrador":self.__scrape_StructGeneral(url)}
        elif argument=="Pujas":
            return {"Pujas": self.__scrape_Pujas(url)}
        elif argument=="Lotes":
            return  {"Lotes": self.__scrape_Lote(url)}
        elif argument=="Interesados":
            return  {"Interesados": self.__scrape_Interesados(url)}
        else:
            return None
    
    def scrape(self):
        if self.listSubastas==None:
            print("No hay ninguna subasta a scrapear. Recuerda ejecutar getListSubasta o setListSubasta")
            return None
        self.__evaluate_complexity()
        url = ""
        
        tot_Scrap = len(self.listSubastas)
        pos_Scrap = 0
        
        print("Completado %d%%"% (0))

        for sub in self.listSubastas:
            rand = np.random.ranf()
            if rand > 0.95:
                time.sleep(rand*5)
            
            self.http.setURL(sub["link"])
            self.http.setTiempo(2)
            html = self.http.getHtml()
            if html==None:
                self.listSubastas[self.listSubastas.index(sub)]["Scrap"]=False
            else:
                bs = BeautifulSoup(html, 'html.parser')
                
                lis = bs.find(attrs={"class":"navlist"}).find_all("li")
                for li in lis:
                    url="https://subastas.boe.es"+li.find("a", href=True)["href"][1:]
                    self.listSubastas[self.listSubastas.index(sub)]["Scrap"]=True
                    self.listSubastas[self.listSubastas.index(sub)].update(self.__scrape_execute(argument=li.text.strip("\n"),url=url))
                                    
            pos_Scrap = pos_Scrap + 1
            if int(100*(pos_Scrap-1)/tot_Scrap) != int(100*pos_Scrap/tot_Scrap):
                print("Completado %d%%"%int(100*pos_Scrap/tot_Scrap))
        