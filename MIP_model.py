from gurobipy import GRB, quicksum, Model
from datos import R, D, Recursos, Flujos, Tonelaje, Profit
from parametros import activar_log_gurobi

def solve_MIP(conos_seleccionados, P):
    #Construcción del conjunto B para el modelo MIP
    B_mip = list()
    for cono in conos_seleccionados:
        if isinstance(cono, list):
            for bloque in cono:
                if bloque not in B_mip:
                    B_mip.append(bloque)
        else:
            if cono not in B_mip:
                B_mip.append(cono)

    #Construcción del conjunto P para el modelo MIP, a partir de conjunto P original.
    P_mip = dict()
    for key in P.keys():
        if int(key) in B_mip:
            P_mip[key] = list()
            for bloque_precedente in P[key]:
                P_mip[key].append(bloque_precedente)

    #Creación del modelo:
    modelo = Model()

    #Variables
    x = {}
    y = {}

    for bloque in B_mip:
        x[bloque] = modelo.addVar(vtype = GRB.BINARY, name = f"x_{bloque}")
        for destino in D:
            y[bloque, destino] = modelo.addVar(vtype = GRB.CONTINUOUS, name = f"y_{bloque}_{destino}")

    #Restricciones

    #Tipo 1, (8) en formulación reducida, paper "Towards Solving ..."
    for bloque in B_mip:
        for bloque_precedente in P_mip[f"{bloque}"]:
            modelo.addConstr(x[bloque] <= x[bloque_precedente], 
            f"{bloque_precedente} precedente de {bloque}")

    #Tipo 2, (9) en formulación reducida, paper "Towards Solving ..."
    for bloque in B_mip:
        modelo.addConstr(quicksum(y[bloque, destino] for destino in D)
        == (x[bloque]))

    #Tipo 3, (10) en formulación reducida, paper "Towards Solving ..."
    for restriccion in R:
        modelo.addConstr(quicksum(quicksum(Tonelaje[bloque] * y[bloque, destino] for destino in D) for bloque in B_mip)
        <= Recursos[f"{restriccion}"])

    #Restricciones Naturaleza de Variables
    for destino in D:
        for bloque in B_mip:
            modelo.addConstr(y[bloque, destino] >= 0)

        for bloque in B_mip:
            modelo.addConstr(x[bloque] <= 1)
            modelo.addConstr(x[bloque] >= 0)

    #Función Objetivo
    FO = quicksum(quicksum(
         Flujos[f"{bloque}"][f"{destino}"] * y[bloque, destino]
         for destino in D) for bloque in B_mip)

    #Desactivar Log a Consola
    if not activar_log_gurobi:
        modelo.Params.LogToConsole = 0

    modelo.update()
    modelo.setObjective(FO, GRB.MAXIMIZE)
    modelo.optimize()

    solucion = list()
    for variable in modelo.getVars():
        solucion.append([variable.varName, variable.x])

    return solucion, modelo.objVal


def solve_MIP2(B, P, w, t, primera_ventana):

    T = range(t - w + 1, t + 1)

    #Creación del modelo:
    modelo = Model()

    #Variables
    x = {}
    y = {}

    for bloque in B:
        for periodo in T:
            x[bloque, periodo] = modelo.addVar(vtype = GRB.BINARY, name = f"x_{bloque}_{periodo}")
            for destino in D:
                y[bloque, destino, periodo] = modelo.addVar(vtype = GRB.CONTINUOUS, name = f"y_{bloque}_{destino}_{periodo}")

    #Restricciones

    #Tipo 1, (2) en paper "Towards Solving ..."
    for periodo in T:
        for bloque in B:
            for bloque_precedente in P[f"{bloque}"]:
                modelo.addConstr(x[bloque, periodo] <= x[bloque_precedente, periodo], 
                f"{bloque_precedente} precedente de {bloque}")


    #Tipo 2, (3) en paper "Towards Solving ..."
    for periodo in range(periodo - w + 1, periodo):
        for bloque in B:
            modelo.addConstr(x[bloque, periodo] <= x[bloque, periodo + 1])

    #Tipo 3, (4) en paper "Towards Solving ..."
    for periodo in T:
        for bloque in B:
            if periodo > (t - w + 1):
                modelo.addConstr(quicksum(y[bloque, destino, periodo] for destino in D)
                == (x[bloque, periodo] - x[bloque, periodo - 1]))
            else:
                modelo.addConstr(quicksum(y[bloque, destino, periodo] for destino in D)
                == (x[bloque, periodo]))

    #tipo 4, (5) en paper "Towards Solving ..."
    for periodo in T:
        for restriccion in R:
            modelo.addConstr(quicksum(quicksum(Tonelaje[bloque] * y[bloque, destino, periodo] for destino in D) for bloque in B)
            <= Recursos[f"{restriccion}"])

    #Restricción de minado
    if not primera_ventana:
        for bloque in B:
            modelo.addConstr(quicksum(x[bloque, periodo] for periodo in T) >= 1)

    #Restricciones Naturaleza de Variables
    for periodo in T:
        for destino in D:
            for bloque in B:
                modelo.addConstr(y[bloque, destino, periodo] >= 0)

    for periodo in T:
        for bloque in B:
            modelo.addConstr(x[bloque, periodo] <= 1)
            modelo.addConstr(x[bloque, periodo] >= 0)

    #Función Objetivo
    FO = quicksum(quicksum(quicksum(
        Profit[f"{bloque}"][f"{destino}"][f"{periodo}"] * y[bloque, destino, periodo] for periodo in T)
        for destino in D) for bloque in B)

    #Desactivar Log a Consola
    if not activar_log_gurobi:
        modelo.Params.LogToConsole = 0

    modelo.update()
    modelo.setObjective(FO, GRB.MAXIMIZE)
    modelo.optimize()

    solucion = list()
    for variable in modelo.getVars():
        solucion.append([variable.varName, variable.x])

    return solucion, modelo.objVal