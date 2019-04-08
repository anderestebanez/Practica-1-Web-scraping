# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 14:04:14 2019

@author: Administrador
"""
import urllib3
import time
import numpy as np
import certifi

class download_html():
    def __init__(self, url="", incognito=False, tiempo=0, rSeed=0, proxys=[], agents=[]):
        self.url = url
        self.rSeed = rSeed
        self.agents=agents
        self.proxys=proxys
        self.incognito=incognito
        self.tiempo = tiempo
    
    def setURL(self, url):
        self.url=url
    
    def changeIncognito(self):
        if self.incognito==True:
            self.incognito=False
            print("Has salido de incognito")
        else:
            self.incognito=True
            print("Has cambiado a tipo incognito")
    
    def setTiempo(self,tiempo):
        if tiempo>=0:
            self.tiempo=tiempo
        else:
            print("El tiempo introducido no es correcto. Prueba otra vez.")
    
    def getHtml(self):
        
        if self.incognito==False:
            http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                                       ca_certs=certifi.where())

        else:
            if len(self.proxys)==0 or type(self.proxys) != list:
                print("No hay listado de proxys asignados")
                return None
            elif len(self.agents)==0 or type(self.agents) != list:
                print("No hay listado de user_agent asignados")
                return None
            
            np.random.seed(self.rSeed)
            nProxy = int(np.random.rand()*len(self.proxys))
            np.random.seed(self.rSeed+1)
            nAgent = int(np.random.rand()*len(self.agents))
                        
            user_agent = {'user-agent': self.agents[nAgent]}
            http = urllib3.ProxyManager(self.proxys[nProxy], headers=user_agent)
            
        
        try:
            response = http.request('GET',self.url)
        except:
            print("Error the conexión en http.request")
            return None
        
        if response.status==200:
            time.sleep(np.random.rand()*self.tiempo)
            self.rSeed+=1
            return response.data
        else:
            print("Error! The URL has not been download '%s'",self.url)
            return None
        