import os
import tarfile

# ------------------------------
# Paso 1: Descomprimir los archivos .tar.gz
# ------------------------------
def extract_tar_gz(filename, extract_path):
    print(f"Descomprimiendo {filename} en {extract_path}...")
    os.makedirs(extract_path, exist_ok=True)
    with tarfile.open(filename, "r:gz") as tar:
        tar.extractall(path=extract_path)
    print(f"{filename} extraído.\n")

# ------------------------------
# Paso 2: Leer instancia QAP (.dat)
# ------------------------------
def read_qap_instance(file_path):
    with open(file_path, 'r') as f:
        lines = f.read().split()
    
    idx = 0
    n = int(lines[idx])
    idx += 1

    # Leer matriz de flujo
    flow = [[int(lines[idx + i * n + j]) for j in range(n)] for i in range(n)]
    idx += n * n

    # Leer matriz de distancia
    dist = [[int(lines[idx + i * n + j]) for j in range(n)] for i in range(n)]

    return flow, dist

# ------------------------------
# Paso 3: Leer solución QAP (.sln)
# ------------------------------
def read_solution(file_path):
    with open(file_path, 'r') as f:
        return list(map(int, f.read().split()))

# ------------------------------
# MAIN
# ------------------------------
def main():
    # Archivos comprimidos
    data_tar = "qapdata.tar.gz"
    soln_tar = "qapsoln.tar.gz"

    # Carpetas de destino
    data_dir = "qapdata"
    soln_dir = "qapsoln"

    # 1. Extraer archivos
    extract_tar_gz(data_tar, data_dir)
    extract_tar_gz(soln_tar, soln_dir)

    # 2. Ver archivos extraídos
    data_files = sorted(os.listdir(data_dir))
    soln_files = sorted(os.listdir(soln_dir))

    print(f"{len(data_files)} archivos de datos encontrados.")
    print(f"{len(soln_files)} archivos de soluciones encontrados.")
    
    # 3. Elegir un archivo ejemplo (chr12a.dat)
    instance_file = os.path.join(data_dir, "chr12a.dat")
    solution_file = os.path.join(soln_dir, "chr12a.sln")

    # 4. Leer instancia
    flow, dist = read_qap_instance(instance_file)
    print("\nEjemplo: chr12a.dat")
    print(f"Dimensión del problema: {len(flow)}")
    print("Primera fila de matriz de flujo:", flow[0])
    print("Primera fila de matriz de distancia:", dist[0])

    # 5. Leer solución
    if os.path.exists(solution_file):
        solution = read_solution(solution_file)
        print("\nSolución cargada:", solution)
    else:
        print("\nNo se encontró solución para esta instancia.")

if __name__ == "__main__":
    main()
