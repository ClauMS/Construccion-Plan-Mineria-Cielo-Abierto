import os
from grasp import ejecutar_grasp
from datos import B
from datos2 import obtener_datos
from parametros import p, ro, mu, n, w

B2, T, D, R, P, Profit, Tonelaje, Recursos, P2, t_carga = obtener_datos()
VO, tiempo, soluciones_ventanas = ejecutar_grasp(B2, T, D, R, P, Profit, Tonelaje, Recursos, P2, 1, p, ro, mu, n, w)

soluciones = dict()
for bloque in B:
    soluciones[str(bloque)] = list()


for t in range(T):
    for bloque in B:
        minado = False
        for var in soluciones_ventanas[t][1]:
            indice = var[0].split("_")
            if "x" == indice[0]:
                if indice[1] == str(bloque) and indice[2] == str(t):
                    minado = True
        if minado or str(1) in soluciones[str(bloque)]:
            soluciones[str(bloque)].append(str(1))
        else:
            soluciones[str(bloque)].append(str(0))


ruta_guardado = os.path.join("Resultados_Grasp", f"resultado_calibrado_DS2_GRASP.csv")
with open(ruta_guardado, "wt", encoding = "UTF-8") as archivo:
    for bloque in soluciones.keys():
        archivo.write(f"{bloque},"+",".join(soluciones[bloque]) + "\n")