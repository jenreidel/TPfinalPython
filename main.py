from utils.helpers import *
from utils import db_manager
import sys

def mostrar_tabla(productos):
    if not productos:
        print("No se encontraron productos")
        return
    else:
        print(f"{'ID':<5} {'NOMBRE':<20} {'CATEGORIA':<15} {'PRECIO:<10'} {'CANTIDAD':<10}")
        print("-" * 65)
        for prod in productos:
            print(f"{prod[0]:<5} {prod[1][:18]:<20} {prod[5][:13]:<15} ${prod[4]:<9.2f} {prod[3]:<10}")
        print("-" * 65)

def menu_registrar():
    imprimir_titulo("Registrar nuevo producto")
    nombre = validar_input_string("Ingresa el nombre del producto: ")
    desc = input("Ingresa la descripcion (opcional): ").strip()
    categ = validar_input_string("Ingresa la categoría: ")
    cantidad = validar_input_int("Ingresar cantidad inicial: ")
    precio = validad_input_float("Ingresar precio unitario: ")

    if db_manager.registrar_producto(nombre,desc,categ,cantidad,precio):
        imprimir_exito("Producto registrado exitosamente.")

def menu_mostrar():
    imprimir_titulo("Listado de productos")
    productos = db_manager.obtener_productos()

def menu_actualizar():
    imprimir_titulo("Actualizar producto")

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
    
