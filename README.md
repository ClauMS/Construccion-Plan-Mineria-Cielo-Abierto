# CAPSTONE-GRUPO3
Proyecto Capstone: Taller de Investigación Operativa. Grupo 3 2021-2 PUC Chile.

## Ejecución
```grasp.py``` es el archivo principal que ejecuta la heurística y entrega el valor objetivo y tiempo total de la solución. Para obtener los resultados en formato ```.csv``` se debe ejecutar el archivo ```grasp_a_csv.py```. Para la selección del dataset (1 o 2) a utilizar se debe modificar la variable ```dataset``` en ```parametros.py```.


## Consideraciones
Actualmente el código construye todos los conos de cada yacimiento cada vez que es ejecutado. Para utilizar las construcciones de conos ya guardadas de cada yacimiento y disminuir el tiempo de cómputo en futuras ejecuciones se encuentran disponibles las funciones ```cargar_conos()``` y ```guardar_conos()``` en el archivo ```funciones_grasp.py```. La última función no es necesaria para los dataser 1 y 2,  pues ya se encuentran subidas las construcciones de conos de cada una de estas instancias (```conos_dataset1``` y ```conos_dataset1```).
