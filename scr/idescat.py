import requests
import pandas as pd
import time

# Get all the municipios in Cataluña
url_municipios = "http://api.idescat.cat/emex/v1/dades.json?lang=es&tipus=mun"
req = requests.get(url_municipios)

# Converto to DataFrame
municipios = pd.DataFrame(req.json()["fitxes"]["cols"]["col"])

# Get data of municipio
indicadores = ["f10","f11","f198","f199","f200","f13","f14","f318",
"f320","f321","f167","f27","f28","f29","f171","f69",
"f72","f73","f378","f379","f377","f291","f225","f284",
"f227","f286","f308","f250","f119","f122"]

data_mun = None
for i,municipio in municipios.iterrows():
    if i not in [563,862]:
        continue
    id = municipio[["id","content"]].values[0]
    content = municipio[["id","content"]].values[1]
    
    url_data = f"https://api.idescat.cat/emex/v1/dades.json?id={id}&i={','.join(indicadores)}&lang=es"
    
    try:
        req = requests.get(url_data)
    except Exception as e:
        print(f"Error en municipio nº {i} con id {id} y nombre {content}")
        print(url_data)
        print(e)

    if req.status_code != 200:
        print(f"Error en municipio con: id {id}, nombre {content}")
    
    temp = pd.DataFrame(req.json()["fitxes"]["indicadors"]["i"])
    temp["value"] = temp.v.apply(lambda x: float(x.split(",")[0]) if isinstance(x,str) else None)
    T_temp = temp.set_index("id").T
    T_temp["id_mun"] = id
    T_temp["mun"] = content
    
    T_temp = T_temp.loc[["value"]].set_index("id_mun")
    
    if i == 0:
        data_mun = T_temp
    else:
        data_mun = data_mun.append(T_temp)
    
    if i%int(len(municipios)/200)==0:
        print(f"Completado el {:.0%}".format(i/len(municipios)))
        time.sleep(2)

data_mun.to_csv(r"C:\Users\Administrador.WIN-K4PA08MDFCA\Documents\UOC\Semestres_Anteriores\Ciclo de vida de los datos\Practica-1-Web-scraping\csv\data_municipio.csv",sep=";",encoding="latin")