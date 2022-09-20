from gurobipy import GRB, quicksum, Model

from datos import B, T, D, R, P, Profit, Tonelaje, Recursos

#Modelo
modelo = Model("RL")
relajacion_lineal = True

#Variables
x = {}
y = {}

for bloque in B:
    for periodo in range(T):
        if relajacion_lineal:
            x[bloque, periodo] = modelo.addVar(vtype = GRB.CONTINUOUS, name = f"x_{bloque}_{periodo}") #Variable Relajada
        else:
            x[bloque, periodo] = modelo.addVar(vtype = GRB.BINARY, name = f"x_{bloque}_{periodo}") #Variable Binaria
        for destino in D:
            y[bloque, destino, periodo] = modelo.addVar(vtype = GRB.CONTINUOUS, name = f"y_{bloque}_{destino}_{periodo}")

#Restricciones

#Tipo 1, (2) en paper "Towards Solving ..."
for periodo in range(T):
    for bloque in B:
        for bloque_precedente in P[f"{bloque}"]:
            modelo.addConstr(x[bloque, periodo] <= x[bloque_precedente, periodo], 
            f"{bloque_precedente} precedente de {bloque}")


#Tipo 2, (3) en paper "Towards Solving ..."
for periodo in range(T-1):
    for bloque in B:
        modelo.addConstr(x[bloque, periodo] <= x[bloque, periodo + 1])

#Tipo 3, (4) en paper "Towards Solving ..."
for periodo in range(T):
    for bloque in B:
        if periodo > 0:
            modelo.addConstr(quicksum(y[bloque, destino, periodo] for destino in D)
            == (x[bloque, periodo] - x[bloque, periodo - 1]))
        else:
            modelo.addConstr(quicksum(y[bloque, destino, periodo] for destino in D)
            == (x[bloque, periodo]))

#tipo 4, (5) en paper "Towards Solving ..."
for periodo in range(T):
    for restriccion in R:
        modelo.addConstr(quicksum(quicksum(Tonelaje[bloque] * y[bloque, destino, periodo] for destino in D) for bloque in B)
        <= Recursos[f"{restriccion}"])


#Restricciones Naturaleza de Variables
for periodo in range(T):
    for destino in D:
        for bloque in B:
            modelo.addConstr(y[bloque, destino, periodo] >= 0)

for periodo in range(T):
        for bloque in B:
            modelo.addConstr(x[bloque, periodo] <= 1)
            modelo.addConstr(x[bloque, periodo] >= 0)


#Función Objetivo

FO = quicksum(quicksum(quicksum(
     Profit[f"{bloque}"][f"{destino}"][f"{periodo}"] * y[bloque, destino, periodo] for periodo in range(T))
     for destino in D) for bloque in B)

modelo.update()

minutos_ejecucion = 600
modelo.setParam('TimeLimit', 60 * minutos_ejecucion)
modelo.update()


# Optimizar
modelo.setObjective(FO, GRB.MAXIMIZE)
modelo.optimize()
#modelo.printAttr("X")
print("\nObj: %g" % modelo.objVal)

#Resultados
#Valor sol. óptima problema original: 2.222626362436e+07 en 211.3 segundos (tolerance 1.00e-04) 
#Valor sol. óptima problema relajado: 2.273408908e+07 en 10.08 segundos
#Valor sol. óptima problema con heurística: 2.21564385940+07 en 26.17 segundos (Diferencia: 69825.03034495562)


# Modelo para problema de PCPSP: Towards Solving Large-Scale Precedence Constrained Production Scheduling Problems in Mining
# Kenny et.al (2017)