import random
import os
import time

# ---------------------------
# Leer instancia QAPLIB (.dat)
# ---------------------------
def leer_instancia(path):
    with open(path, 'r') as f:
        lines = [line for line in f.readlines() if line.strip()]
    
    n = int(lines[0])
    A = []
    B = []
    
    matriz = []
    for line in lines[1:]:
        matriz.extend([int(x) for x in line.strip().split()])
    
    total = n * n
    A = [matriz[i * n:(i + 1) * n] for i in range(n)]
    B = [matriz[i * n + total:(i + 1) * n + total] for i in range(n)]
    
    return n, A, B

# ---------------------------
# Evaluación (función objetivo)
# ---------------------------
def fitness(permutacion, A, B):
    n = len(permutacion)
    costo = 0
    for i in range(n):
        for j in range(n):
            costo += A[i][j] * B[permutacion[i]][permutacion[j]]
    return costo

# ---------------------------
# Crear individuo: permutación aleatoria
# ---------------------------
def crear_individuo(n):
    p = list(range(n))
    random.shuffle(p)
    return p

# ---------------------------
# Cruce por posición (PMX simple)
# ---------------------------
def cruzar(p1, p2):
    n = len(p1)
    i, j = sorted(random.sample(range(n), 2))

    hijo = [None] * n
    hijo[i:j] = p1[i:j]

    for k in range(i, j):
        elem = p2[k]
        if elem not in hijo:
            pos = k
            while hijo[pos] is not None:
                pos = p2.index(p1[pos])
            hijo[pos] = elem

    for k in range(n):
        if hijo[k] is None:
            hijo[k] = p2[k]

    return hijo

# ---------------------------
# Mutación por intercambio
# ---------------------------
def mutar(p, tasa=0.1):
    if random.random() < tasa:
        i, j = random.sample(range(len(p)), 2)
        p[i], p[j] = p[j], p[i]
    return p

# ---------------------------
# Selección por torneo
# ---------------------------
def seleccion(poblacion, A, B):
    torneo = random.sample(poblacion, 3)
    torneo.sort(key=lambda x: fitness(x, A, B))
    return torneo[0]

# ---------------------------
# Algoritmo Genético principal
# ---------------------------
def resolver_qap(ruta_archivo, generaciones=100, tam_poblacion=100):
    n, A, B = leer_instancia(ruta_archivo)
    poblacion = [crear_individuo(n) for _ in range(tam_poblacion)]

    for gen in range(generaciones):
        poblacion.sort(key=lambda p: fitness(p, A, B))
        mejor = poblacion[0]

        nueva_poblacion = poblacion[:20]  # elitismo
        while len(nueva_poblacion) < tam_poblacion:
            padre1 = seleccion(poblacion, A, B)
            padre2 = seleccion(poblacion, A, B)
            hijo = cruzar(padre1, padre2)
            hijo = mutar(hijo)
            nueva_poblacion.append(hijo)

        poblacion = nueva_poblacion

    mejor_solucion = poblacion[0]
    mejor_costo = fitness(mejor_solucion, A, B)
    return mejor_solucion, mejor_costo

# ---------------------------
# Leer solución óptima de QAPLIB
# ---------------------------
def leer_solucion_optima(path):
    with open(path, 'r') as f:
        valores = list(map(int, f.read().split()))
    if len(valores) < 2:
        raise ValueError(f"Archivo de solución mal formado: {path}")
    costo_optimo = valores[1]
    solucion = [x - 1 for x in valores[2:]]  # Convertir a base 0
    return solucion, costo_optimo

# ---------------------------
# Función para probar todas las instancias en una carpeta
# ---------------------------
def probar_todas_instancias(data_dir="qapdata", soln_dir="qapsoln", generaciones=100, tam_poblacion=100):
    archivos = sorted([f for f in os.listdir(data_dir) if f.endswith('.dat')])
    resultados = []

    for archivo in archivos:
        print(f"\nProcesando instancia: {archivo}")
        ruta_instancia = os.path.join(data_dir, archivo)
        nombre_base = os.path.splitext(archivo)[0]
        ruta_solucion = os.path.join(soln_dir, nombre_base + ".sln")

        # Medir tiempo de ejecución
        inicio = time.time()
        solucion, costo = resolver_qap(ruta_instancia, generaciones, tam_poblacion)
        fin = time.time()
        tiempo = fin - inicio

        # Leer solución óptima si existe
        if os.path.exists(ruta_solucion):
            try:
                _, costo_optimo = leer_solucion_optima(ruta_solucion)
                if costo_optimo > 0:
                    diferencia = costo - costo_optimo
                    gap = (diferencia / costo_optimo) * 100
                else:
                    diferencia = None
                    gap = None
                    print(f"Advertencia: Costo óptimo inválido (0) en {ruta_solucion}")
            except Exception as e:
                costo_optimo = None
                diferencia = None
                gap = None
                print(f"Error al leer {ruta_solucion}: {e}")
        else:
            costo_optimo = None
            diferencia = None
            gap = None

        print(f"Costo AG: {costo}")
        print(f"Tiempo de ejecución: {tiempo:.2f} segundos")
        if costo_optimo is not None:
            print(f"Costo óptimo (QAPLIB): {costo_optimo}")
            print(f"Diferencia absoluta: {diferencia}")
            print(f"Gap porcentual: {gap:.2f} %" if gap is not None else "Gap no disponible.")
        else:
            print("Solución óptima no disponible.")

        resultados.append({
            "instancia": archivo,
            "costo_ag": costo,
            "costo_optimo": costo_optimo,
            "diferencia": diferencia,
            "gap": gap,
            "tiempo": tiempo
        })

    return resultados

# ---------------------------
# Ejecutar todo
# ---------------------------
if __name__ == "__main__":
    resultados = probar_todas_instancias(generaciones=100, tam_poblacion=100)

    print("\nResumen de resultados:")
    for r in resultados:
        print(f"{r['instancia']}: Costo AG={r['costo_ag']} | "
              f"Costo Óptimo={r['costo_optimo']} | "
              f"Dif={r['diferencia']} | Gap={'{:.2f}%'.format(r['gap']) if r['gap'] is not None else 'N/A'} | "
              f"Tiempo={r['tiempo']:.2f}s")
