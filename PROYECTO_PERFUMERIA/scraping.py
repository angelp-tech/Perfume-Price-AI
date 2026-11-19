
# ==========================================
# PROYECTO: PREDICCION DE PRECIOS DE PERFUMES
# FASE I: VERIFICACION Y EXTRACCION DE DATOS
# ==========================================

import requests
import pandas as pd
import os
import json
import time
import random
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
from collections import Counter
from urllib.parse import urlparse

# ==========================================
# FUNCION PARA EXTRAER TABLAS HTML
# ==========================================

def extraer_tablas_html(sopa):

    tablas = sopa.find_all("table")
    datos_tablas = []

    for tabla in tablas:

        filas = tabla.find_all("tr")
        datos = []

        for fila in filas:

            celdas = fila.find_all(["th", "td"])

            fila_datos = [
                celda.get_text(strip=True)
                for celda in celdas
            ]

            if fila_datos:
                datos.append(fila_datos)

        if datos:
            datos_tablas.append(datos)

    return datos_tablas

# ==========================================
# 1. CONFIGURACION DEL PROYECTO
# ==========================================

url_catalogo = "https://labodegadelperfume.co/categorias/catalogo-completo/"
robots_url = "https://labodegadelperfume.co/robots.txt"
sitemap_url = "https://labodegadelperfume.co/sitemap.xml"

encabezados = {
    "User-Agent": "ProyectoAcademicoCienciaDeDatos/1.0"
}

limite_productos = 100
productos_extraidos = []


# ==========================================
# 2. VERIFICAR CONDICIONES DE ACCESO
# ==========================================

print("\n========== VERIFICACION DEL PORTAL ==========")

respuesta_robots = requests.get(
    robots_url,
    headers=encabezados,
    timeout=20
)

print("ESTADO DEL ARCHIVO ROBOTS:", respuesta_robots.status_code)

if respuesta_robots.status_code == 200:
    print(respuesta_robots.text[:3000])
else:
    print("No fue posible consultar robots.txt.")



# ==========================================
# 3. CONSULTAR EL CATALOGO
# ==========================================

respuesta_catalogo = requests.get(
    url_catalogo,
    headers=encabezados,
    timeout=20
)

print("\nESTADO DE LA PAGINA:", respuesta_catalogo.status_code)

if respuesta_catalogo.status_code == 200:

    sopa_catalogo = BeautifulSoup(
        respuesta_catalogo.text,
        "html.parser"
    )

    titulo = sopa_catalogo.find("h1")

    if titulo:
        print("TITULO DEL CATALOGO:", titulo.get_text(strip=True))

    # Comprobar si existen tablas HTML
    tablas_html = sopa_catalogo.find_all("table")

    print("\n========== TABLAS HTML ==========")
    print("TOTAL DE TABLAS ENCONTRADAS:", len(tablas_html))

    for numero, tabla in enumerate(tablas_html, start=1):

        encabezados_tabla = [
            th.get_text(strip=True)
            for th in tabla.find_all("th")
        ]

        print(f"\nTABLA NUMERO {numero}")
        print("COLUMNAS:", encabezados_tabla)

    print("\nCONEXION EXITOSA")

else:
    print("No se pudo consultar el catalogo.")
    raise SystemExit("Se detiene el programa por fallo en el catalogo.")


# ==========================================
# 4. EXPLORAR EL SITEMAP
# ==========================================

print("\n========== EXPLORACION DEL SITEMAP ==========")

respuesta_sitemap = requests.get(
    sitemap_url,
    headers=encabezados,
    timeout=20
)

print("ESTADO DEL SITEMAP:", respuesta_sitemap.status_code)

if respuesta_sitemap.status_code == 200:

    raiz = ET.fromstring(respuesta_sitemap.content)

    direcciones = [
        elemento.text
        for elemento in raiz.iter()
        if elemento.tag.endswith("loc") and elemento.text
    ]

    print("TOTAL DE DIRECCIONES:", len(direcciones))

else:
    print("No se pudo consultar el sitemap.")
    raise SystemExit("Se detiene el programa por fallo en el sitemap.")


# ==========================================
# 5. CLASIFICAR LAS DIRECCIONES
# ==========================================

print("\n========== CLASIFICACION DE DIRECCIONES ==========")

rutas = []

for direccion in direcciones:

    ruta = urlparse(direccion).path
    partes = ruta.strip("/").split("/")

    if partes and partes[0]:
        rutas.append(partes[0])
    else:
        rutas.append("inicio")

conteo_rutas = Counter(rutas)

for categoria, cantidad in conteo_rutas.most_common(20):
    print(f"{categoria}: {cantidad}")


# ==========================================
# 6. IDENTIFICAR URLS DE PRODUCTOS
# ==========================================

urls_productos = [
    direccion
    for direccion in direcciones
    if "/perfumes/" in direccion
]

# Eliminar duplicados conservando el orden
urls_productos = list(dict.fromkeys(urls_productos))

print("\n========== ANALISIS DE PRODUCTOS ==========")
print("TOTAL DE URLS DE PERFUMES:", len(urls_productos))

# Seleccionar aleatoriamente hasta 100 productos
random.seed(42)

cantidad_seleccionada = min(
    limite_productos,
    len(urls_productos)
)

urls_seleccionadas = random.sample(
    urls_productos,
    cantidad_seleccionada
)

print("PRODUCTOS SELECCIONADOS:", len(urls_seleccionadas))


# ==========================================
# 7. EXAMINAR UNA FICHA DE PRODUCTO
# ==========================================

print("\n========== PRUEBA DE FICHA DE PRODUCTO ==========")

url_prueba = (
    "https://labodegadelperfume.co/"
    "pt-br/perfumes/one-million-edt-for-men-1047/"
)

respuesta_producto = requests.get(
    url_prueba,
    headers=encabezados,
    timeout=20
)

print("ESTADO DEL PRODUCTO:", respuesta_producto.status_code)

if respuesta_producto.status_code == 200:

    producto_html = BeautifulSoup(
        respuesta_producto.text,
        "html.parser"
    )

    titulo_producto = producto_html.find("h1")

    if titulo_producto:
        print("NOMBRE:", titulo_producto.get_text(strip=True))

    datos_json = producto_html.find_all(
        "script",
        type="application/ld+json"
    )

    print("BLOQUES JSON-LD ENCONTRADOS:", len(datos_json))

else:
    print("No se pudo consultar el producto.")

# ==========================================
# 8. EXTRAER INFORMACION DE LOS PRODUCTOS
# ==========================================

print("\n========== INICIO DE EXTRACCION ==========")

for posicion, url_producto in enumerate(
    urls_seleccionadas,
    start=1
):

    try:

        print(
            f"\nConsultando producto {posicion} "
            f"de {cantidad_seleccionada}..."
        )

        respuesta = requests.get(
            url_producto,
            headers=encabezados,
            timeout=20
        )

        respuesta.raise_for_status()

        sopa = BeautifulSoup(
            respuesta.text,
            "html.parser"
        )

        # Extraer contenido de las tablas HTML
        tablas_extraidas = extraer_tablas_html(sopa)

        if tablas_extraidas:

            print(
                "TABLAS HTML EN ESTA FICHA:",
                len(tablas_extraidas)
            )

            for numero, tabla in enumerate(
                tablas_extraidas,
                start=1
            ):

                print(f"CONTENIDO DE LA TABLA {numero}:")

                for fila in tabla:
                    print(fila)

        else:
            print("NO SE ENCONTRARON TABLAS HTML")

        # Extraer informacion JSON-LD
        bloques_json = sopa.find_all(
            "script",
            type="application/ld+json"
        )

        producto_encontrado = False

        for bloque in bloques_json:

            try:

                contenido = json.loads(
                    bloque.string or bloque.get_text()
                )

            except (json.JSONDecodeError, TypeError):
                continue

            if isinstance(contenido, list):
                elementos = contenido

            elif isinstance(contenido, dict) and "@graph" in contenido:
                elementos = contenido["@graph"]

            else:
                elementos = [contenido]

            for elemento in elementos:

                if not isinstance(elemento, dict):
                    continue

                tipo = elemento.get("@type")

                if isinstance(tipo, list):
                    es_producto = "Product" in tipo
                else:
                    es_producto = tipo == "Product"

                if not es_producto:
                    continue

                oferta = elemento.get("offers", {})
                marca = elemento.get("brand", {})

                if isinstance(oferta, list):
                    oferta = oferta[0] if oferta else {}

                if isinstance(marca, dict):
                    nombre_marca = marca.get("name")
                else:
                    nombre_marca = marca

                if not isinstance(oferta, dict):
                    oferta = {}

                producto = {
                    "nombre": elemento.get("name"),
                    "marca": nombre_marca,
                    "sku": elemento.get("sku"),
                    "precio": oferta.get("price"),
                    "moneda": oferta.get("priceCurrency"),
                    "categoria": elemento.get("category"),
                    "disponibilidad": oferta.get("availability"),
                    "url": url_producto
                }

                productos_extraidos.append(producto)

                print("PRODUCTO:", producto["nombre"])
                print("MARCA:", producto["marca"])
                print("PRECIO:", producto["precio"])

                producto_encontrado = True
                break

            if producto_encontrado:
                break

        if not producto_encontrado:
            print("No se encontraron datos estructurados.")

    except requests.RequestException as error:

        print("ERROR AL CONSULTAR:", url_producto)
        print("DETALLE:", error)

    except Exception as error:

        print("ERROR PROCESANDO:", url_producto)
        print("DETALLE:", error)

    # Pausa entre solicitudes
    time.sleep(2)


# ==========================================
# 9. CONSTRUCCION DEL DATASET
# ==========================================

print("\n========== CONSTRUCCION DEL DATASET ==========")

df_productos = pd.DataFrame(productos_extraidos)

os.makedirs("datos", exist_ok=True)

ruta_csv = "datos/datos_crudos.csv"

df_productos.to_csv(
    ruta_csv,
    index=False,
    encoding="utf-8-sig"
)

print("\n========== DATASET INICIAL ==========")

print(df_productos.head())

print("\nDIMENSIONES DEL DATASET:")
print(df_productos.shape)

print("\nTOTAL DE PRODUCTOS EXTRAIDOS:")
print(len(df_productos))

print("\nARCHIVO CSV GUARDADO:")
print(ruta_csv)
