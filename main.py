from utils.helpers import *
from utils import db_manager
import sys

def mostrar_tabla(productos):
    if not productos:
        print("No se encontraron productos")
        return

    print(f"{'ID':<5} {'NOMBRE':<20} {'CATEGORIA':<15} {'PRECIO':<10} {'CANTIDAD':<10}")
    print("-" * 65)

    for prod in productos:
        # Orden real: 0=id, 1=nombre, 2=descripcion, 3=cantidad, 4=precio, 5=categoria
        id_ = prod[0]
        nombre = prod[1][:18] if prod[1] else ""
        categoria = prod[5] if len(prod) > 5 and prod[5] is not None else ""
        precio = prod[4] if len(prod) > 4 and prod[4] is not None else 0.0
        cantidad = prod[3] if len(prod) > 3 and prod[3] is not None else 0

        print(f"{id_:<5} {nombre:<20} {categoria:<15} ${precio:<9.2f} {cantidad:<10}")

    print("-" * 65)

def menu_registrar():
    imprimir_titulo("Registrar nuevo producto")
    nombre = validar_input_string("Ingresa el nombre del producto")
    desc = input("Ingresa la descripcion (opcional): ").strip()
    categ = validar_input_string("Ingresa la categoría")
    cantidad = validar_input_int("Ingresar cantidad inicial")
    precio = validad_input_float("Ingresar precio unitario")

    if db_manager.registrar_producto(nombre, desc, cantidad, precio, categ):
        imprimir_exito("Producto registrado exitosamente.")

def menu_mostrar():
    imprimir_titulo("Listado de productos")
    productos = db_manager.obtener_productos()
    mostrar_tabla(productos)

def menu_actualizar():
    imprimir_titulo("Actualizar producto")
    menu_mostrar()
    id_prod = validar_input_int("Ingrese el id del producto a modificar: ")

    producto_actual = db_manager.buscar_producto_id(id_prod)
    if not producto_actual:
        imprimir_error("Producto no encontrado.")
        return
    
    print(f"Editando: {producto_actual[1]}")
    print("Deja vacío el campo que no quieras modificar")

    nuevo_nombre = input(f"Nombre [{producto_actual[1]}]: ").strip() or producto_actual[1]
    nuevo_desc = input(f"Descripción [{producto_actual[2]}]: ").strip() or producto_actual[2]
    nueva_cat = input(f"Categoría [{producto_actual[5]}]: ").strip() or producto_actual[5]

    cant_str = input(f"Cantidad [{producto_actual[3]}]: ").strip()
    nueva_cant = int(cant_str) if cant_str.isdigit() else producto_actual[3]

    precio_str = input(f"Precio [{producto_actual[4]}]: ").strip()
    nuevo_precio = float(precio_str) if precio_str else producto_actual[4]

    if db_manager.actualizar_producto(id_prod,nuevo_nombre,nuevo_desc,nueva_cant,nuevo_precio,nueva_cat):
        imprimir_exito("Producto actualizado exitosamente.")
    else:
        imprimir_error("El producto no pudo ser actualizado.")

def menu_eliminar():
    imprimir_titulo("Eliminar Producto")
    menu_mostrar()

    id_prod = validar_input_int("Ingrese el ID del producto que desea eliminar: ")

    confirm = input(f"¿Confirma la eliminación del producto con ID {id_prod}? (s/n): ").lower()
    if confirm == 's':
        if db_manager.eliminar_producto(id_prod):
            imprimir_exito("Producto eliminado exitosamente.")
        else:
            imprimir_error("El ID solicitado no fue encontrado.")

def menu_buscar():
    imprimir_titulo("Buscador de productos")
    print("1. Buscar por ID")
    print("2. Buscar por Nombre o Categoría")
    opcion = input("Ingrese la opción de búsqueda elegida: ")

    if opcion == "1":
        id_prod = validar_input_int("Ingrese el ID que desea buscar: ")
        res = db_manager.buscar_producto_id(id_prod)
        if res:
            mostrar_tabla([res])
        else:
            imprimir_error("ID no encontrado.")
    elif opcion == "2":
        termino = validar_input_string("Ingrese el término de búsqueda deseado: ")
        res = db_manager.buscar_producto_texto(termino)
        mostrar_tabla(res)
    else:
        imprimir_error("Opción inválida.")

def main():
    db_manager.inicializar_db()

    while True:
        print("\n" + "="*30)
        print("\n~~~ Sistema de Gestión de Productos ~~~\n")
        print("="*30)
        print("1. Registrar Producto")
        print("2. Mostrar Productos")
        print("3. Actualizar Producto")
        print("4. Eliminar Producto")
        print("5. Buscar Producto")
        print("6. Salir\n")
        print("="*40)

        opcion = input("\nSeleccione la opción deseada: ")

        if opcion == "1":
            menu_registrar()
        elif opcion == "2":
            menu_mostrar()
        elif opcion == "3":
            menu_actualizar()
        elif opcion =="4":
            menu_eliminar()
        elif opcion == "5":
            menu_buscar()
        elif opcion =="6":
            print("Saliendo del sistema...")
            sys.exit()
        else:
            imprimir_error("La opción elegida no es válida, intente nuevamente.")

if __name__ == "__main__":
    main()