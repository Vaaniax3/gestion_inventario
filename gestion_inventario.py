from pathlib import Path
import csv
import shutil
from datetime import datetime

RUTA_ARCHIVO = Path("inventario.csv")
BACKUP_DIR = Path("backups")
ENCABEZADOS = ["Nombre", "Precio", "Cantidad", "Talla"]

def inicializar_archivo(ruta_dinamica: Path, campos: list):
    with open(ruta_dinamica, 'w', newline='', encoding='utf-8') as archivo:
        writer = csv.DictWriter(archivo, fieldnames=campos)
        writer.writeheader()
        print("Archivo inicializado")

def agregar_producto(nombre, precio, cantidad, talla):
    with open(RUTA_ARCHIVO, "a", newline="", encoding="utf-8") as archivo:
        escritor_csv = csv.writer(archivo)
        escritor_csv.writerow([nombre, precio, cantidad, talla])
        print("Producto agregado con éxito.")

def mostrar_inventario():
    print("\nMostrando inventario:")
    print("="*30)
    try:
        with open(RUTA_ARCHIVO, 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            encabezados = next(lector)
            print(f"Encabezados: {encabezados}")
            print("Datos:")
            for fila in lector:
                print(fila)
    except FileNotFoundError:
        print("El archivo no existe.")
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")

def buscar_producto():
    nombre_buscar = input("Ingrese el nombre del producto a buscar: ")
    encontrado = False
    try:
        with open(RUTA_ARCHIVO, 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            encabezados = next(lector)
            for fila in lector:
                if fila[0].lower() == nombre_buscar.lower():
                    print(f"Producto encontrado: {dict(zip(encabezados, fila))}")
                    encontrado = True
                    break
    except FileNotFoundError:
        print("El archivo no existe.")
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
    if not encontrado:
        print("Producto no encontrado.")

def editar_producto():
    nombre_buscar = input("Ingrese el nombre del producto a editar: ")
    encontrado = False
    try:
        with open(RUTA_ARCHIVO, 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            encabezados = next(lector)
            filas = list(lector)
            for i, fila in enumerate(filas):
                if fila[0].lower() == nombre_buscar.lower():
                    print(f"Producto encontrado: {dict(zip(encabezados, fila))}")
                    nuevo_nombre = input("Nuevo nombre (enter para dejar igual): ")
                    nuevo_precio = input("Nuevo precio (enter para dejar igual): ")
                    nuevo_cantidad = input("Nueva cantidad (enter para dejar igual): ")
                    nuevo_talla = input("Nueva talla (enter para dejar igual): ")

                    if nuevo_nombre:
                        fila[0] = nuevo_nombre
                    if nuevo_precio:
                        fila[1] = nuevo_precio
                    if nuevo_cantidad:
                        fila[2] = nuevo_cantidad
                    if nuevo_talla:
                        fila[3] = nuevo_talla

                    filas[i] = fila
                    encontrado = True
                    break
    except FileNotFoundError:
        print("El archivo no existe.")
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")

    if encontrado:
        with open(RUTA_ARCHIVO, 'w', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(encabezados)
            escritor.writerows(filas)
            print("Producto editado con éxito.")
    else:
        print("Producto no encontrado.")

def eliminar_producto():
    nombre_buscar = input("Ingrese el nombre del producto a eliminar: ")
    encontrado = False
    try:
        with open(RUTA_ARCHIVO, 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            encabezados = next(lector)
            filas = list(lector)
            for i, fila in enumerate(filas):
                if fila[0].lower() == nombre_buscar.lower():
                    print(f"Producto encontrado y eliminado: {dict(zip(encabezados, fila))}")
                    del filas[i]
                    encontrado = True
                    break
    except FileNotFoundError:
        print("El archivo no existe.")
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")

    if encontrado:
        with open(RUTA_ARCHIVO, 'w', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(encabezados)
            escritor.writerows(filas)
            print("Producto eliminado con éxito.")
    else:
        print("Producto no encontrado.")

def crear_backup():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    destino = BACKUP_DIR / f"inventario_backup_{timestamp}.csv"
    shutil.copy(RUTA_ARCHIVO, destino)
    print(f"Backup creado en: {destino}")

def menu():
    while True:
        print("\nMenú:")
        print("1. Mostrar inventario")
        print("2. Buscar producto")
        print("3. Editar producto")
        print("4. Crear backup")
        print("5. Eliminar producto")
        print("6. Agregar producto") 
        print("7. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            mostrar_inventario()
        elif opcion == "2":
            buscar_producto()
        elif opcion == "3":
            editar_producto()
        elif opcion == "4":
            crear_backup()
        elif opcion == "5":
            eliminar_producto()
        elif opcion == "6":
            nombre = input("Nombre del producto: ")
            precio = input("Precio: ")
            cantidad = input("Cantidad: ")
            talla = input("Talla: ")
            agregar_producto(nombre, precio, cantidad, talla)
        elif opcion == "7":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    if not RUTA_ARCHIVO.exists():
        inicializar_archivo(RUTA_ARCHIVO, ENCABEZADOS)
