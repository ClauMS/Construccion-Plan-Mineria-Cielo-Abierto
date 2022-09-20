import os
import numpy as np

from grasp import ejecutar_grasp
from datos2 import obtener_datos
from funciones_grasp import comprobar_solucion
from parametros import dataset

ruta_guardado = os.path.join("Resultados Estudio Parametros", f"resultados.txt")
filesize = os.path.getsize(ruta_guardado)

if filesize == 0:
    with open(ruta_guardado, "wt", encoding = "UTF-8") as archivo:
        archivo.write("Iteración,Dataset,p,ro,mu,n,w,Valor Objetivo,Tiempo,Factibilidad\n")

def run(iteraciones, p, ro, mu, n, w):

    for i in range(iteraciones):
        B, T, D, R, P, Profit, Tonelaje, Recursos, P2, t_carga = obtener_datos()
        try:
            VO, tiempo, solucion = ejecutar_grasp(B, T, D, R, P, Profit, Tonelaje, Recursos, P2, i, p, ro, mu, n, w)
            factible = True

            with open(ruta_guardado, "a", encoding = "UTF-8") as archivo:
                archivo.write(f"{i},{dataset},{p},{ro},{mu},{n},{w},{VO},{tiempo - t_carga},{factible}\n")
        except Exception as e:
            try:
                VO, tiempo, solucion = ejecutar_grasp(B, T, D, R, P, Profit, Tonelaje, Recursos, P2, i, p, ro, mu, n, w)
                factible = True

                with open(ruta_guardado, "a", encoding = "UTF-8") as archivo:
                    archivo.write(f"{i},{dataset},{p},{ro},{mu},{n},{w},{VO},{tiempo - t_carga},{factible}\n")
            except Exception as e:
                #si se equivoca x segunda vez seguida:
                factible = True
                with open(ruta_guardado, "a", encoding = "UTF-8") as archivo:
                    archivo.write(f"{i},{dataset},{p},{ro},{mu},{n},{w},VO,tiempo,{factible}\n")
                pass

#Rangos de parámetros a estudiar:
#p: [0.4, 0.6]
#ro: [0.3, 0.7]
#mu: [1, 3.5]