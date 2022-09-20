#Random solution contruction
from funciones_grasp import constructor_conos, aplanar, valor_total, tonelaje_total, ordenar_conos, comprobar_disponibilidad, seleccionar_solucion, actualizar_conjuntos, guardar_conos, cargar_conos
from funciones_grasp import crear_conjunto_P, crear_conjunto_B, incluir_periodo, actualizar_valor_objetivo, actualizar_soluciones_ventanas, comprobar_solucion, bloques_minados
from MIP_model import solve_MIP, solve_MIP2
from parametros import window_time_limit, activar_log_grasp, gap, dataset
from datos2 import obtener_datos

from time import time
from random import uniform

def ejecutar_grasp(B, T, D, R, P, Profit, Tonelaje, Recursos, P2, i, p, ro, mu, n, w):

    print(f"Iteración {i}\n")

    ###########  RANDOM SOLUTION CONSTRUCTION   ###########
    limite_recursos = Recursos[str(0)]

    soluciones_RSC = list() #Soluciones Random Solution Construction

    t0 = time()
    for periodo in range(T):

        lista_conos = list()
        #Construcción de todos los conos en el modelo en t = periodo
        for bloque in B:
            cono = constructor_conos(bloque, [], P)
            cono = aplanar(cono)
            lista_conos.append([cono, int(valor_total(cono))])
        #Ordenamiento por valor de lista de todos los conos
        lista_conos = ordenar_conos(lista_conos)
        
        #Seleccion aleatoria de conos hasta límite de recursos x mu
        soluciones_periodo = list()
        for i in range(n):
            conos_seleccionados = list()
            recursos_utilizados = 0
            for cono in lista_conos:
                if recursos_utilizados < mu*limite_recursos:
                    if isinstance(cono[0], list):
                        disponible = comprobar_disponibilidad(cono[0][0], conos_seleccionados)
                    else:
                        disponible = comprobar_disponibilidad(cono[0], conos_seleccionados)
                    if disponible:
                        if tonelaje_total(cono[0]) < ro*limite_recursos:
                            n_aleatorio = uniform(0, 1)
                            if n_aleatorio < p:
                                conos_seleccionados.append(cono[0])
                                recursos_utilizados += tonelaje_total(cono[0])
                else:
                    break


            #Resolución de modelo MIP
            variables, obj = solve_MIP(conos_seleccionados, P)
            soluciones_periodo.append([variables, obj])
            
        
        sol = seleccionar_solucion(soluciones_periodo) #sol = [vars, VO]
        B, P = actualizar_conjuntos(sol, B, P)
        soluciones_RSC.append([periodo, incluir_periodo(sol[0], periodo)]) #[[t, varst], [t2, varst2]]

        
    t_rsc = time()
    
    ###########  LOCAL IMPROVEMENT HEURISTIC   ###########

    soluciones_ventanas = soluciones_RSC
    termino = False
    gap_alcanzado = False
    VO = 1
    t_inicio = time()
    pasada = 0
    while not termino:
        primera_ventana = True
        for t in range(T - w + 1):

            periodo = T - t - 1
            Bloques_ventana = crear_conjunto_B(soluciones_ventanas, periodo, w)
            Precedencias_ventana = crear_conjunto_P(Bloques_ventana, P2)
            variables_ventana, valor_ventana = solve_MIP2(Bloques_ventana, Precedencias_ventana, w, periodo, primera_ventana)

            if primera_ventana:
                primera_ventana = False

            soluciones_ventanas = actualizar_soluciones_ventanas(soluciones_ventanas, variables_ventana, w, periodo)


        nuevo_VO = actualizar_valor_objetivo(soluciones_ventanas)
            #print(f"VO: Pasada {pasada}, ventana {periodo} a {periodo-1}: {nuevo_VO}")
        #pasada += 1


        if (100*(nuevo_VO - VO)/VO) < gap:
            termino = True
            gap_alcanzado = True
            t_ventanas = time()
        else:
            VO = nuevo_VO

        if (time() - t_inicio) >= (window_time_limit * 60):
            termino = True

    if activar_log_grasp:
        print(f"Tiempo total de RSC: {round((t_rsc - t0)/60, 2)} minutos")
        if gap_alcanzado:
            print(f"Convergencia de la solución alcanzada (gap: {gap}%)")
            print(f"Tiempo en alcanzar la convergencia (ventanas): {round(t_ventanas - t_inicio, 2)} segundos")
        else:
            print(f"Límite de tiempo alcanzado: {window_time_limit} minutos.")

        print(f"Tiempo total GRASP: {round((time() - t0)/60, 2)} minutos")
        print(f"\nValor objetivo final: {VO}\n")

    return VO, time()-t0, soluciones_ventanas



if __name__ == "__main__":
    B2, T, D, R, P, Profit, Tonelaje, Recursos, P2, t_carga = obtener_datos()

    p = 0.3
    ro = 0.3
    mu = 3.5
    n = 7
    w = 2

    VO, tiempo, soluciones_ventanas = ejecutar_grasp(B2, T, D, R, P, Profit, Tonelaje, Recursos, P2, 0, p, ro, mu, n, w)
    factible = comprobar_solucion(soluciones_ventanas)
    bloques_minados(soluciones_ventanas)


    print(f"Solución factible: {factible}")