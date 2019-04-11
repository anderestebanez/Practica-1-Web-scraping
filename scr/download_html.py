# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 14:04:14 2019

@author: Ander Estebanez Centeno
"""
import urllib3
import time
import numpy as np
import certifi
import requests

class download_html():
    ''' Esta clase es un descargador de archivos HTML que permite configurar como 
    se quiere hacer la descarga (tiempos de espera, incognito, ...)     
    '''
    def __init__(self, url="", incognito=False, tiempo=0, rSeed=0, proxys=[], agents=[]):
        ''' Cambia la URL a extraer 
        
        Keyword arguments:
            url -- URL que se quiere descargar.
            incognito -- Indica si se quiere acceder a la url de forma incognita o normal
            tiempo -- Tiempo máximo a esperar después de cada descarga.
            rSeed -- Valor inicial del Seed del random
            proxys -- Listado de proxys a utilizar en caso de acceder en incognito
            agents -- Listado de user-agents a utilizar en caso de acceder en incognito
        '''
        self.url = url
        self.rSeed = rSeed
        self.agents=agents
        self.proxys=proxys
        self.incognito=incognito
        self.tiempo = tiempo
        

    
    def setURL(self, url):
        ''' Cambia la URL a extraer 
        
        Keyword arguments:
            url -- URL que se quiere extraer 
        '''
        self.url=url
    
    def changeIncognito(self):
        ''' Cambia la configuración entre incognito y no incognito '''
        if self.incognito==True:
            self.incognito=False
            print("Has salido de incognito")
        else:
            self.incognito=True
            print("Has cambiado a tipo incognito")
    
    def setTiempo(self,tiempo):
        ''' Cambia el parametro de tiempo, que modifica el tiempo de espera 
        después de cada extracción. '''
        if tiempo>=0:
            self.tiempo=tiempo
        else:
            print("El tiempo introducido no es correcto. Prueba otra vez.")
    
    def getHtml(self):
        ''' Descarga el fichero HTML de la url de la configuración. Si está en incognito se aplicará un usar_agent y proxy aleatorio de la lista configurada, sino usara el user_agent y proxy por defecto.
        '''
        
        
        if self.incognito==False: # Aplica una forma de descarga diferente según si es incognito o no
            response = requests.get(self.url())
            #http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
            #                           ca_certs=certifi.where())
            #response = http.request('GET',self.url)

        else:
            # Se revisa que haya proxys y user_agent configurados
            if len(self.proxys)==0 or type(self.proxys) != list:
                print("No hay listado de proxys asignados")
                return None
            elif len(self.agents)==0 or type(self.agents) != list:
                print("No hay listado de user_agent asignados")
                return None
            
            # Se selecciona un user_agent y proxy aleatorio
            np.random.seed(self.rSeed)
            nProxy = int(np.random.rand()*len(self.proxys))
            np.random.seed(self.rSeed+1)
            nAgent = int(np.random.rand()*len(self.agents))
            
            i=1
            descargado=False            
            while i<10 and descargado==False:
                agent=self.agents[nAgent]
                user_agent = {'user-agent': agent["user_agent"]}
                proxy=self.proxys[nProxy]
                proxy = {'http': 'http://'+proxy['IP Address']+":"+str(proxy['Port']).zfill(4)+"/"}
                #http = urllib3.ProxyManager(proxy, headers=user_agent)
        
                try: #Intentamos descargar, si hay error salimos
                    response = requests.get(self.url, proxies=proxy, headers=user_agent)
                    #http.request('GET',self.url)
                    descargado=True
                except Exception as e:
                    print("Intento: %d - Error de conexión: %s"%(i,type(e).__name__))
                    print("Proxy: %s \n Descripción: %s"%(proxy,e.args[:50]))
                    nProxy+=1
                    if nProxy>=len(self.proxys):
                        nProxy=0                        
                    i+=1

        # En caso de que no haya respuesta 200 entonces se sale
        if response.status_code==200:
            time.sleep(np.random.rand()*self.tiempo)
            self.rSeed+=1
            return response.content
        else:
            print("Error %d! The URL has not been download '%s'"%(response.status_code,self.url))
            return None
    
