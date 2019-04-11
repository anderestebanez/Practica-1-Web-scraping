# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 00:16:50 2019

@author: Ander Estebanez Centeno
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
import numpy as np
from scr.download_html import download_html

class SubastaBOEScraper():
    
    
    def __init__(self, http=None):
        ''' Inicializa la clase SubastaBOEScraper.
        
        Keyword arguments:
            http -- Clase download_html configurada a utilizar.
        '''
        
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
                  resetFilter=True, 
                  estado="", 
                  tipo_Bien="", 
                  provincia="", 
                  fchFin="", 
                  fchIni=""):
        ''' Crea la URL a scrapear a través de los filtros especificados
        
        (Pendiente)
        Keyword arguments:
            resetFilter -- Indica si se quiere añadir un filtro a los ya indicados o si se inicializan todos
            estado -- Estado del la subasta.
            tipo_Bien -- Tipo de bien que se está subastando
            provincia -- Código de la provincia de las subastas.
            fchFin -- Fecha inicio de la subasta
            fchIni -- Fecha fin de la subasta            
            '''
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
        ''' Descarga el html de forma simple 
        
        Keyword arguments:
            url -- Url que se va a descargar 
            sleep -- Número de segundos que se va a esperar como máximo una vez hecha la descarga            
            '''
        
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                           ca_certs=certifi.where())
        response = http.request('GET',url)
        if response.status==200:
            return response.data
            time.sleep(sleep)
        else:
            return None
        
    def getSubastaLink(self, url = "", listSubastas = None):
        ''' Extrae todas las subastas existentes en en la url 
        
        Keyword arguments:
            url -- Url con los filtros aplicados. Si no se indica nada se usará el parametro url del objeto.
            listSubastas -- Listado de subastas ya generados. Las subastas se incluirán a esta lista. 
        '''
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
            subastaLink = {"codSubasta":p[0].text.strip(' \n'),
                           "autoridad":p[1].text.strip(' \n')}
            subastaLink["codSubasta"]=subastaLink["codSubasta"][:subastaLink["codSubasta"].find("\n")]
            
            if p[2].text.strip(' \n')[0:10]=="Expediente":
                subastaLink["expediente"]=p[2].text.strip(' \n')[12:]
                subastaLink["estado"]=p[3].text.strip(' \n')[8:]
                
            elif p[2].text.strip(' \n')[0:6]=="Estado":
                subastaLink["estado"]=p[2].text.strip(' \n')[8:]
            
            subastaLink["estado"]=subastaLink["estado"][:subastaLink["estado"].find("\n")]
            descr=li.find(attrs={"class":"documento"}).text.strip(' \n')
            subastaLink["descripcion"]=descr[:descr.find("\n")].replace(";",",")
            subastaLink["link"]="https://subastas.boe.es"+li.find("a", href=True)["href"][1:]
            
            listSubastas.append(subastaLink)
        
        pagSig = bs.find(attrs={"class":"pagSig"})
        
        if pagSig is not None:
            self.getSubastaLink(url="https://subastas.boe.es/"+pagSig.find_parent("a", href=True)["href"],listSubastas=listSubastas) 
        
        self.listSubastas = listSubastas
        return len(self.listSubastas)
        
    def setListSubasta(self, listSubastas):
        ''' Carga una lista de subastas para luego poder ser scrapeadas. 
        Antes comprueba que no haya ningún elemento en la lista sin todos los campos imprescindibles informado y descarta los registros erroneos.
        
        Keyword arguments:
            listSubastas -- Lista de subastas. Cada subasta será un diccionario con al menos los campos __codSubasta__,  __link__ y __estado__. 
        '''
        subastas=[]
        
        for subasta in listSubastas:
            if "codSubasta" in subasta and "link" in subasta and "estado" in subasta:
                subastas.append(subasta)
        
        print("Del total de  %d subastas, %d han sido descartados por no disponer de información básica"%(len(listSubastas), len(listSubastas)-len(subastas)))
        self.listSubastas=subastas
    
    def __evaluate_complexity(self):
        ''' Evalua la complejidad del scrapeo '''
        sec_tot = len(self.listSubastas)*4
        horas = int(sec_tot/(60*60))
        minu = int(sec_tot/60)-horas*60
        sec = sec_tot-minu*60-horas*60*60
        
        print("There are %d links. The expected time is %d:%d:%d"%(len(self.listSubastas),horas,minu,sec))
        return None

    #Este código scrapear estructuras estandars: InforGeneral, Autoridades, Administrador concursal y Bienes
    def __scrape_StructGeneral(self, urlSubasta, prefij="", sufij=""):
        ''' Código que permite scrapear las pestañas que tienen una estructura 
        genera de tabla. 
        
        Keyword arguments:
            urlSubasta -- URL que a scrapear
            prefij -- Prefiero en cada uno de los keys generados
            sufij -- Sufijo en cada uno de los keys generados
        '''
            
        self.http.setURL(urlSubasta)
        self.http.setTiempo(0)
        html = self.http.getHtml()
        
        if html==None: # Si devuelve no se sale del proceso marcando la subasta como no scrapeada
            return {"Scrap":False}
        
        bs = BeautifulSoup(html, 'html.parser')
        
        infoGeneral={}
        trs=bs.find("table", attrs={"class":"datosSubastas"}).find_all("tr")
        for tr in trs:    
            infoGeneral[prefij + tr.find("th").text + sufij]=tr.find("td").text.strip("\n").replace(";",",").replace('\n',' ')
        
        return infoGeneral
    
    def __scrape_Pujas(self,urlSubasta):
        ''' Código que permite scrapear la pestaña de pujas. 
        
        Keyword arguments:
            urlSubasta -- URL que a scrapear           
        '''
            
        self.http.setURL(urlSubasta)
        self.http.setTiempo(0)
        html = self.http.getHtml()
        if html==None: #  Si devuelve no se sale del proceso marcando la subasta como no scrapeada
            return {"Scrap":False}
        
        bs = BeautifulSoup(html, 'html.parser')
        
        pujas=[]        
        
        # Se pueden dar 3 casos: con puja máxima, con pujas máximas por lote o sin pujas.
        if bs.find("div", attrs={"class":"bloqueSubasta"})==None:
            pujas = [{"Lote": "0", "Puja":"0"}]
        elif bs.find("div", attrs={"class":"bloqueSubasta"}).find("span", attrs={"class":"destaca"}) != None:
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
        ''' Código que permite scrapear la pestaña de lotes. 
        
        Keyword arguments:
            urlSubasta -- URL que a scrapear           
        '''
        
        self.http.setURL(urlSubasta)
        self.http.setTiempo(0.5)
        html = self.http.getHtml()
        if html==None:  #  Si devuelve no se sale del proceso marcando la subasta como no scrapeada
            return {"Scrap":False}
        bs = BeautifulSoup(html, 'html.parser')
        
        lotes=[]
        
        # Cada subasta puede tener más de un lote, cada uno en una url diferente.
        lis=bs.find("ul", attrs={"class":"navlistver2"}).find_all("li")
        
        for li in lis:
            url = "https://subastas.boe.es"+li.find("a", href=True)["href"][1:]
            nLote=li.find("a", href=True).text
            lote={"Lote":nLote}
            
            self.http.setURL(url)
            self.http.setTiempo(0)
            html = self.http.getHtml()
            if html==None:  #  Si devuelve no se sale del proceso marcando la subasta como no scrapeada
                return {"Scrap":False}
            
            bs = BeautifulSoup(html, 'html.parser')
            
            # Cada lote tiene la información distribuida en al menos dos tablas
            tables=bs.find_all("table", attrs={"class":"datosSubastas"})
            lote["numBienes"]=len(bs.find_all("div", attrs={"class":"bloqueSubastaBien"}))
            for table in tables:
                trs = table.find_all("tr")
                for tr in trs:    
                    lote[tr.find("th").text]=tr.find("td").text.strip("\n").replace(";",",").replace("\n"," ")
            lotes.append(lote)       
        
        return lotes
    
        
    def __scrape_Interesados(self,urlSubasta):
        ''' Código que permite scrapear la pestaña de interesados. 
        
        Keyword arguments:
            urlSubasta -- URL que a scrapear           
        '''
        self.http.setURL(urlSubasta)
        self.http.setTiempo(0.5)
        html = self.http.getHtml()        
        if html==None:  #  Si devuelve no se sale del proceso marcando la subasta como no scrapeada
            return {"Scrap":False}
        bs = BeautifulSoup(html, 'html.parser')
        
        interesados=[]
        
        # Cada subasta puede tener más de un interesado.
        tables=bs.find_all("table", attrs={"class":"datosSubastas"})
        for table in tables:
            interesado = {}
            trs = table.find_all("tr")
            for tr in trs:    
                interesado[tr.find("th").text]=tr.find("td").text.strip("\n")
            interesados.append(interesado)       
    
        return interesados
        
    def __scrape_Acreedores(self,urlSubasta):
        ''' Código que permite scrapear la pestaña de acredores. 
        
        Keyword arguments:
            urlSubasta -- URL que a scrapear           
        '''
        self.http.setURL(urlSubasta)
        self.http.setTiempo(0.5)
        html = self.http.getHtml()        
        if html==None:  #  Si devuelve no se sale del proceso marcando la subasta como no scrapeada
            return {"Scrap":False}
        bs = BeautifulSoup(html, 'html.parser')
        
        acreedores=[]
        
        # Cada subasta puede tener más de un interesado.
        tables=bs.find_all("table", attrs={"class":"datosSubastas"})
        for table in tables:
            acreedor = {}
            trs = table.find_all("tr")
            for tr in trs:    
                acreedor[tr.find("th").text]=tr.find("td").text.strip("\n").replace(";",",")
            acreedores.append(acreedor)       
    
        return acreedores
        
    def __scrape_execute(self,argument, url):
        ''' Código que permite parametrizar el tratamiento que se tiene que hacer
        según el nombre de la pestaña de la url principal. 
        
        Keyword arguments:
            argument -- Nombre de la pestaña. Según el nombre se aplicará un method u otro.           
            url -- URL para acceder a la pestaña
        '''
        
        if argument=="Información general": 
            return self.__scrape_StructGeneral(url)
        elif argument=="Autoridad gestora": 
            return self.__scrape_StructGeneral(url,prefij="aut_")
        elif argument=="Bienes": 
            bienes={"Lote":"Lote 1"}
            bienes.update(self.__scrape_StructGeneral(url))
            return {"lotes":[bienes]}
        elif argument in ["Acreedores","Acreedor","Acreedor privilegiado", "Acreedores privilegiados"]: 
            acreedores=self.__scrape_Acreedores(url)
            for acreedor in acreedores:
                if argument in ["Acreedor privilegiado","Acreedores privilegiados"]:
                    acreedor.update({"tipoPrivilegiado":True})
                else:
                    acreedor.update({"tipoPrivilegiado":False})
            return {"acreedores":acreedores}
        elif argument=="Administrador concursal": 
            return self.__scrape_StructGeneral(url,prefij="adm_")
        elif argument=="Pujas":
            return {"pujas": self.__scrape_Pujas(url)}
        elif argument=="Lotes":
            return  {"lotes": self.__scrape_Lote(url)}
        elif argument in ["Interesados","Interesado"]:
            return  {"interesados": self.__scrape_Interesados(url)}
        else:
            return {"Error":"Not found argumento:"+argument, "Scrap":False}
    
    def scrape(self):
        ''' Scrapea todas las subastas de la lista de subastas. 
        '''
        if self.listSubastas==None:
            print("No hay ninguna subasta a scrapear. Recuerda ejecutar getListSubasta o setListSubasta")
            return None
        self.__evaluate_complexity()
        url = ""
        iniTime=time.time()
        
        tot_Scrap = len(self.listSubastas)
        pos_Scrap = 0
        
        print("%s: Completado %d%%"% (time.strftime("%H:%M:%S",time.localtime()) 0))

        for sub in self.listSubastas:
            self.listSubastas[self.listSubastas.index(sub)]["Scrap"]=True
                    
            rand = np.random.ranf()
            if rand > 0.95:
                time.sleep(rand*5)
            
            self.http.setURL(sub["link"])
            self.http.setTiempo(2)
            html = self.http.getHtml()
            if html==None:  #  Si devuelve no se sale del proceso marcando la subasta como no scrapeada
                self.listSubastas[self.listSubastas.index(sub)]["Scrap"]=False
            else:
                bs = BeautifulSoup(html, 'html.parser')
                
                lis = bs.find(attrs={"class":"navlist"}).find_all("li")
                for li in lis:
                    url="https://subastas.boe.es"+li.find("a", href=True)["href"][1:]
                    self.listSubastas[self.listSubastas.index(sub)].update(self.__scrape_execute(argument=li.text.strip("\n"),url=url))
                                    
            pos_Scrap = pos_Scrap + 1
            if int(100*(pos_Scrap-1)/tot_Scrap) != int(100*pos_Scrap/tot_Scrap):
                print("%s: Completado %d%%"%(time.strftime("%H:%M:%S",time.localtime()),int(100*pos_Scrap/tot_Scrap)))
            
        self.getErrors()
        difTime=time.time()-iniTime
        print("La ejecución a tomado %d %d:%d:%d. %f por minuto"%(int(difTime/(60*60*24)),
                                                                  int(difTime/(60*60))-int(difTime/(60*60*24))*24,
                                                                  int(difTime/(60))-int(difTime/(60*60))*60,
                                                                  int(difTime)-int(difTime/(60))*60,
                                                                  len(self.listSubastas)*60/difTime))
    
    def getErrors(self):
        ''' Contar el número de subastas con error o pendientes de scrapear '''
        i=0
        j=1
        index=[]
        ii=0
        for ls in self.listSubastas:
            if "Scrap" in ls.keys() and ls["Scrap"]==False:
                i+=1
                index=index+[ii]
            elif "Scrap" not in ls.keys():
                j+=1
            ii=ii+1
            
        print("Num errors: %d - Num pendiente scrap: %d \n Los index a revisar son: %s"%(i, j, index.__str__()))

    def data2csv(self, path, dictFilename={}):        
        
        filenames={"fileGeneral":"infoSubastas.csv",
                   "fileLotes":"lotesSubastas.csv",
                   "fileInteresados":"interesadosSubastas.csv",
                   "fileAcreedores":"acreedoresSubastas.csv",
                   "filePujas":"pujasSubastas.csv"}
        if type(dictFilename) != dict:
            stay=True
            while stay==True:
                resp=input("dictFilename no es un dictionary. ¿Quieres continuar con los nombre por defecto?(S/N)")
                if resp.upper()=="N":
                    return None
                elif resp.upper()=="S":
                    stay=False
        elif len(dictFilename.keys()-filenames.keys()) > 0:
            stay=True
            while stay==True:
                resp=input("Los siguientes keys no son correctos %s. \n El diccionario solo puede tener los keys: %s\n ¿Quieres continuar sin modificar los keys erroneos?(S/N)"%((dictFilename.keys()-filenames.keys()).__str__(),list(filenames.keys()).__str__()))
                if resp.upper()=="N":
                    return None
                elif resp.upper()=="S":
                    filenames.update(dictFilename)
                    stay=False
        
        keyGeneral=[]
        keyLotes=["codSubasta"]
        keyInteresados=["codSubasta"]
        keyAcreedores=["codSubasta"]
        keyPujas=["codSubasta"]
        
        for it in self.listSubastas:
            keyGeneral.extend(it.keys())    
            keyGeneral=list(set(keyGeneral))
            if "lotes" in it.keys() and it['lotes'] != "Sin lotes":
                for lote in it['lotes']:
                    keyLotes.extend(lote.keys())
                    keyLotes=list(set(keyLotes))
            if "interesados" in it.keys():
                for interesado in it['interesados']:
                    keyInteresados.extend(interesado.keys())
                    keyInteresados=list(set(keyInteresados))
            if "pujas" in it.keys():
                for puja in it['pujas']:
                    keyPujas.extend(puja.keys())
                    keyPujas=list(set(keyPujas))
            if "acreedores" in it.keys():
                for acreedor in it['acreedores']:
                    keyAcreedores.extend(acreedor.keys())
                    keyAcreedores=list(set(keyAcreedores))
                  
                    
        fileGeneral = open(path + "/" + filenames["fileGeneral"], "w+")
        fileLotes = open(path + "/" + filenames["fileLotes"], "w+")
        fileInteresados = open(path + "/" + filenames["fileInteresados"], "w+")
        fileAcreedores = open(path + "/" + filenames["fileAcreedores"], "w+")
        filePujas = open(path + "/" + filenames["filePujas"], "w+")

        # Escribimos las cabeceras
        fileGeneral.write("codSubasta;")
        for key in [x for x in keyGeneral if x not in ['codSubasta', 'lotes', 'interesados', 'acreedores', 'pujas']]:
            fileGeneral.write(key + ";")
        fileGeneral.write("\n")

        fileLotes.write("codSubasta;")
        fileLotes.write("lote;")
        for key in [x for x in keyLotes if x not in ['codSubasta', 'Lote']]:
            fileLotes.write(key + ";")
        fileLotes.write("\n")
        
        fileInteresados.write('codSubasta;')
        for key in [x for x in keyInteresados if x not in ['codSubasta']]:
            fileInteresados.write(key + ";")
        fileInteresados.write("\n")
                        
        filePujas.write('codSubasta;')
        filePujas.write('lote;')
        for key in [x for x in keyPujas if x not in ['codSubasta','Lotes']]:
            filePujas.write(key + ";")
        filePujas.write("\n")
        
        
        fileAcreedores.write('codSubasta;')
        for key in [x for x in keyAcreedores if x not in ['codSubasta']]:
            fileAcreedores.write(key + ";")
        fileAcreedores.write("\n")
                    
        #  Se escriben los valores al CSV
        for it in self.listSubastas:
            fileGeneral.write(it['codSubasta'] + ";")            
            for key in [x for x in keyGeneral if x not in ['codSubasta', 'lotes', 'interesados', 'acreedores', 'pujas']]:
                if key in it.keys():
                    fileGeneral.write(str(it[key]) + ";")    
                else:
                    fileGeneral.write(";")    
            fileGeneral.write("\n")
            
            if "lotes" in it.keys():
                for lote in it['lotes']:
                    fileLotes.write(it['codSubasta'] + ";")
                    fileLotes.write(lote['Lote'] + ";")
                    for key in [x for x in keyLotes if x not in ['codSubasta', 'Lote']]:
                        if key in lote.keys():
                            fileLotes.write(str(lote[key]) + ";")
                        else:
                            fileLotes.write(";")
                    fileLotes.write("\n")
                        
            if "interesados" in it.keys():
                for interesado in it['interesados']:
                    fileInteresados.write(it['codSubasta'] + ";")
                    for key in [x for x in keyInteresados if x not in ['codSubasta']]:
                        if key in interesado.keys():
                            fileInteresados.write(str(interesado[key]) + ";")
                        else:
                            fileInteresados.write(";")
                    fileInteresados.write("\n")
                        
            if "pujas" in it.keys():
                for puja in it['pujas']:
                    filePujas.write(it['codSubasta'] + ";")
                    filePujas.write(puja['Lote'] + ";")
                    for key in [x for x in keyPujas if x not in ['codSubasta','Lotes']]:
                        if key in puja.keys():
                            filePujas.write(str(puja[key]) + ";")
                        else:
                            filePujas.write(";")
                    filePujas.write("\n")
            
            if "acreedores" in it.keys():
                for acreedor in it['acreedores']:
                    fileAcreedores.write(it['codSubasta'] + ";")
                    for key in [x for x in keyAcreedores if x not in ['codSubasta']]:
                        if key in acreedor.keys():                            
                            fileAcreedores.write(str(acreedor[key]) + ";")
                        else:
                            fileAcreedores.write(";")
                    fileAcreedores.write("\n")
        fileGeneral.close
        fileLotes.close
        fileInteresados.close
        fileAcreedores.close
        filePujas.close