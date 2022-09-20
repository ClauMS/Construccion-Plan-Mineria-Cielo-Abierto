import pandas as pd
from time import time
from parametros import dataset

t_0 = time()

Bloques = pd.read_excel(f"dataset{dataset}.xlsx", sheet_name="Bloques")
Precedencias = pd.read_excel(f"dataset{dataset}.xlsx", sheet_name="Precedencias")
Flujos_Destino = pd.read_excel(f"dataset{dataset}.xlsx", sheet_name="Flujos Destino")
Restricciones_Tipo = pd.read_excel(f"dataset{dataset}.xlsx", sheet_name="Restricciones Tipo")
Restricciones_Coeficientes = pd.read_excel(f"dataset{dataset}.xlsx", sheet_name="Restricciones Coeficientes")
if dataset == 1:
    nombre = "Periodos y Tasa de Descuento"
elif dataset == 2:
    nombre = "Informacion General"
Periodos_y_Tasa_de_Descuento = pd.read_excel(f"dataset{dataset}.xlsx", sheet_name=nombre)

#Conjunto de bloques (IDs)
B1 = Bloques["ID"] #ndarray
B = B1.to_list() #list

#Periodos de tiempo (int)
T = Periodos_y_Tasa_de_Descuento["N_Periodos"][0]

#Destinos: 1 (dump), 2 (planta)
D = [1, 2] #list

#Tipos de restricciones: 0 (Extracción Mina) y 1 (Procesamiento Planta)
R = Restricciones_Tipo["Restriccion"] #ndarray

#Diccionario de precedencias. Ej: P["1"] = [2, 9]
P = dict() #dict
for id in Precedencias["ID"]:
    lista_precedecesores = list()
    for key in Precedencias.keys():
        if key != "ID" and key != "N_Predecesores":
            if Precedencias[key][id] > -1:
                lista_precedecesores.append(int(Precedencias[key][id]))
    P[f"{id}"] = lista_precedecesores

#Diccionario de precedencias2. Ej: P["1"] = [2, 9]
P2 = dict() #dict
for id in Precedencias["ID"]:
    lista_precedecesores = list()
    for key in Precedencias.keys():
        if key != "ID" and key != "N_Predecesores":
            if Precedencias[key][id] > -1:
                lista_precedecesores.append(int(Precedencias[key][id]))
    P2[f"{id}"] = lista_precedecesores

#Diccionario de parámetros p_{bdt}. Ej: Profit["1"]["2"]["0"] = 24829.116
Profit = dict()
tasa_descuento = Periodos_y_Tasa_de_Descuento["Tasa_Descuento"][0]


for id in Flujos_Destino["ID"]:
    Profit[f"{id}"] = dict()
    for destino in D:
        Profit[f"{id}"][str(destino)] = dict()
        for t in range(0, T):
            if destino == 1:
                flujo = Flujos_Destino["Flujo_Destino_1"][id]
            elif destino == 2:
                flujo = Flujos_Destino["Flujo_Destino_2"][id]
            valor = flujo/((1 + tasa_descuento)**t)
            Profit[f"{id}"][str(destino)][str(t)] = valor
        

#Diccionario de Flujos totales. Ej: Flujo["11"]["2"] = 21413.268
Flujos = dict()
for id in Flujos_Destino["ID"]:
    Flujos[f"{id}"] = dict()
    for destino in D:
        Flujos[f"{id}"][str(destino)] = dict()
        if destino == 1:
            flujo = Flujos_Destino["Flujo_Destino_1"][id]
        elif destino == 2:
            flujo = Flujos_Destino["Flujo_Destino_2"][id]

        Flujos[f"{id}"][str(destino)] = flujo

#Toneladas de c/bloque. Ej: Tonelaje[0] = 2192.93
#No se incluyen subíndices d y r, debido a que ambas restricciones y destinos
#utilizan las mismas toneladas como unidad de recurso.
Tonelaje = Bloques["Toneladas"] #ndarray


#Diccionario de límites superiores de restricciones (recursos)
#No se incluye subíndice t debido a que, en estos dataset, recursos no cambian en el tiempo.
Recursos = dict()
for restriccion in R:
    Recursos[f"{restriccion}"] = Restricciones_Tipo["Limite Superior"][restriccion]

    
print("\n")
print(f"Dataset seleccionado: {dataset}")
print(f"Tiempo de carga de datos: {round(time() - t_0, 2)} segundos")