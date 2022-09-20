import os
from relajacion_lineal import modelo, T

resultados_existentes = True

if not resultados_existentes:
    for t in range(T):

        var_names = list()

        for var in modelo.getVars(): 
            if "x" == str(var.VarName[0]) and str(var.VarName[-1]) == f"{t}":
                var_names.append([str(var.Varname), str(var.x)])

        ruta_guardado = os.path.join("Resultados", f"periodo_{t}.csv")
        with open(ruta_guardado, "wt", encoding = "UTF-8") as archivo:
            for lista in var_names:
                archivo.write(",".join(lista) + "\n")