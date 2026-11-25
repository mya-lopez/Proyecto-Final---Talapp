# -----------------------------------------------------------
# TALAPP - Planes mensuales personalizados de comida para perros (Colombia)
#
# Qué hace:
#   1. Pide los datos del perro (peso, edad, condición médica)
#   2. Recomienda el plan adecuado y la cantidad por mes
#   3. Permite comprarlo directamente (sin necesidad de catálogo)
#   4. Actualiza el inventario después de cada compra
#   5. Muestra un reporte de ventas
# -----------------------------------------------------------

import csv
import math

# ---------------- DATOS ----------------

# Cada producto es un diccionario. Stock = número de bultos de 5 kg disponibles.
catalogo = [
    {"id": 1, "nombre": "Talapp Cachorro",       "precio": 95000,  "stock": 20},
    {"id": 2, "nombre": "Talapp Adulto",         "precio": 85000,  "stock": 30},
    {"id": 3, "nombre": "Talapp Senior",         "precio": 90000,  "stock": 15},
    {"id": 4, "nombre": "Talapp Light (peso)",   "precio": 92000,  "stock": 12},
    {"id": 5, "nombre": "Talapp Digestivo",      "precio": 98000,  "stock": 10},
    {"id": 6, "nombre": "Talapp Renal",          "precio": 120000, "stock": 8},
    {"id": 7, "nombre": "Talapp Articulaciones", "precio": 110000, "stock": 8},
    {"id": 8, "nombre": "Talapp Hipoalergénico", "precio": 115000, "stock": 10},
]

KG_BULTO = 5  # cada bulto pesa 5 kg

# Lista donde guardamos cada venta (se usa para el reporte)
ventas = []


# ---------------- FUNCIONES AUXILIARES ----------------

def dinero(valor):
    """Muestra un número como pesos colombianos, ejemplo: $95.000"""
    return "$" + format(valor, ",").replace(",", ".")


def buscar_producto(id_producto):
    """Busca un producto por id. Devuelve None si no existe."""
    for producto in catalogo:
        if producto["id"] == id_producto:
            return producto
    return None


def pedir_numero(mensaje, minimo, maximo):
    """Sigue preguntando hasta que el usuario escriba un número válido."""
    while True:
        texto = input(mensaje).replace(",", ".")
        try:
            numero = float(texto)
        except ValueError:
            print("Por favor escribe un número.")
            continue
        if numero < minimo or numero > maximo:
            print("El número debe estar entre", minimo, "y", maximo)
            continue
        return numero


# ---------------- CATÁLOGO (opcional) ----------------

def mostrar_catalogo():
    print("\n=== CATÁLOGO TALAPP (planes mensuales) ===")
    for producto in catalogo:
        print(producto["id"], "-", producto["nombre"],
              "| Precio:", dinero(producto["precio"]),
              "| Bultos disponibles:", producto["stock"])


# ---------------- RECOMENDACIÓN ----------------

def recomendar_plan():
    print("\n=== RECOMENDACIÓN DE PLAN ===")
    nombre = input("Nombre del perro: ")
    peso = pedir_numero("Peso en kg (1 - 90): ", 1, 90)
    edad = pedir_numero("Edad en años (0 - 25, usa 0.5 para 6 meses): ", 0, 25)

    print("\nCondición médica:")
    print("1 - Ninguna")
    print("2 - Sobrepeso")
    print("3 - Estómago sensible")
    print("4 - Problemas renales")
    print("5 - Problemas de articulaciones (artritis)")
    print("6 - Alergias alimentarias")
    condicion = int(pedir_numero("Elige (1-6): ", 1, 6))

    # --- Paso 1: elegir el producto ---
    # La condición médica tiene prioridad sobre la edad.
    if condicion == 2:
        id_producto = 4
        porcentaje = 0.015      # 1.5% del peso corporal por día
    elif condicion == 3:
        id_producto = 5
        porcentaje = 0.022
    elif condicion == 4:
        id_producto = 6
        porcentaje = 0.020
    elif condicion == 5:
        id_producto = 7
        porcentaje = 0.022
    elif condicion == 6:
        id_producto = 8
        porcentaje = 0.022
    else:
        # Sin condición: usamos la edad
        if edad < 1:
            id_producto = 1
            porcentaje = 0.05   # los cachorros comen más por kilo
        elif edad < 7:
            id_producto = 2
            porcentaje = 0.025
        else:
            id_producto = 3
            porcentaje = 0.020

    # --- Paso 2: calcular la cantidad ---
    gramos_dia = peso * 1000 * porcentaje
    kg_mes = gramos_dia * 30 / 1000
    bultos = math.ceil(kg_mes / KG_BULTO)   # redondear hacia arriba

    producto = buscar_producto(id_producto)

    print("\n--- Plan para", nombre, "---")
    print("Comida recomendada:", producto["nombre"])
    print("Cantidad diaria: unos", round(gramos_dia), "g (dividido en 2 comidas)")
    print("Necesidad mensual: unos", round(kg_mes, 1), "kg")
    print("Bultos de", KG_BULTO, "kg al mes:", bultos)
    print("Precio mensual:", dinero(bultos * producto["precio"]))
    print("(Es un estimado. Si tu perro tiene una condición médica,")
    print(" por favor consulta con tu veterinario.)")

    # Ofrecer comprar el plan recomendado de una vez
    if producto["stock"] < bultos:
        print("\nLo sentimos, solo tenemos", producto["stock"], "bultos de",
              producto["nombre"], "por ahora.")
        return

    respuesta = input("\n¿Quieres comprar este plan? (s/n): ")
    if respuesta.lower() == "s":
        comprar(producto, bultos)


# ---------------- COMPRA ----------------

def comprar(producto, cantidad):
    """Compra el plan que fue recomendado (producto + número de bultos)."""
    print("\n=== COMPRA ===")
    cliente = input("Nombre del cliente: ")

    total = cantidad * producto["precio"]
    print(cantidad, "bulto(s) de", producto["nombre"])
    print("Total a pagar:", dinero(total))
    respuesta = input("¿Confirmas la compra? (s/n): ")
    if respuesta.lower() != "s":
        print("Compra cancelada.")
        return

    # Actualizar inventario
    producto["stock"] = producto["stock"] - cantidad

    # Guardar la venta
    venta = {
        "cliente": cliente,
        "producto": producto["nombre"],
        "cantidad": cantidad,
        "total": total,
    }
    ventas.append(venta)

    print("¡Gracias,", cliente, "! Compra realizada.")
    if producto["stock"] <= 3:
        print("** Alerta: poco stock de", producto["nombre"], "**")


# ---------------- REPORTE DE VENTAS ----------------

def reporte_ventas():
    print("\n=== REPORTE DE VENTAS ===")

    if len(ventas) == 0:
        print("Todavía no hay ventas.")
        return

    total_dinero = 0
    total_bultos = 0
    por_producto = {}   # nombre del producto -> [bultos, dinero]

    for venta in ventas:
        total_dinero = total_dinero + venta["total"]
        total_bultos = total_bultos + venta["cantidad"]

        nombre = venta["producto"]
        if nombre not in por_producto:
            por_producto[nombre] = [0, 0]
        por_producto[nombre][0] += venta["cantidad"]
        por_producto[nombre][1] += venta["total"]

    print("Número de ventas:", len(ventas))
    print("Bultos vendidos:", total_bultos)
    print("Ingresos totales:", dinero(total_dinero))

    print("\nVentas por producto:")
    mejor_nombre = ""
    mejores_bultos = 0
    for nombre in por_producto:
        bultos = por_producto[nombre][0]
        ingreso = por_producto[nombre][1]
        print("-", nombre, ":", bultos, "bultos,", dinero(ingreso))
        if bultos > mejores_bultos:
            mejores_bultos = bultos
            mejor_nombre = nombre
    print("\nMás vendido:", mejor_nombre)

    print("\nInventario actual:")
    for producto in catalogo:
        print("-", producto["nombre"], ":", producto["stock"], "bultos")

    # Guardar las ventas en un archivo que se abre en Excel
    with open("reporte_ventas.csv", "w", newline="", encoding="utf-8-sig") as f:
        escritor = csv.writer(f)
        escritor.writerow(["cliente", "producto", "cantidad", "total"])
        for venta in ventas:
            escritor.writerow([venta["cliente"], venta["producto"],
                               venta["cantidad"], venta["total"]])
    print("\nReporte guardado en reporte_ventas.csv")


# ---------------- MENÚ PRINCIPAL ----------------

def main():
    print("Bienvenido a TALAPP - comida personalizada para tu perro")

    while True:
        print("\n===== MENÚ =====")
        print("1 - Obtener el plan de mi perro (y comprarlo)")
        print("2 - Ver catálogo (opcional)")
        print("3 - Reporte de ventas")
        print("4 - Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            recomendar_plan()
        elif opcion == "2":
            mostrar_catalogo()
        elif opcion == "3":
            reporte_ventas()
        elif opcion == "4":
            print("¡Hasta pronto!")
            break
        else:
            print("Opción inválida, intenta de nuevo.")


main()
