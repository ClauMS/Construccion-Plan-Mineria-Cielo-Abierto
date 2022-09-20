import pandas as pd
from time import time
from parametros import dataset
from datos import B, T, D, R, P, Profit, Tonelaje, Recursos, P2

def obtener_datos():

    t0 = time()
    new_B = list()
    for bloque in B:
        new_B.append(bloque)

    new_P = dict()
    for key in P2.keys():
        precedencias = list()
        for precedente in P2[key]:
            precedencias.append(int(precedente))
        new_P[key] = precedencias
    

    return new_B, T, D, R, new_P, Profit, Tonelaje, Recursos, P2, time() - t0