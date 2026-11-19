
# ==========================================
# PROYECTO: PREDICCION DE PRECIOS DE PERFUMES
# FASE II: LIMPIEZA Y TRANSFORMACION DE DATOS
# ==========================================

import pandas as pd
import os

# 1. Cargar el dataset original
ruta = "datos/datos_crudos.csv"

df = pd.read_csv(ruta)

print("========== DATASET ORIGINAL ==========")

print(df.head())

print("\nDIMENSIONES DEL DATASET:")
print(df.shape)

print("\nINFORMACION GENERAL:")
df.info()

print("\nVALORES NULOS POR COLUMNA:")
print(df.isnull().sum())

print("\nREGISTROS DUPLICADOS:")
print(df.duplicated().sum())

# ==========================================
# 2. LIMPIEZA DE DATOS
# ==========================================

print("\n========== INICIO DE LIMPIEZA ==========")

# Crear una copia para conservar el dataset original
df_limpio = df.copy()

# 1. Eliminar registros duplicados
duplicados_antes = df_limpio.duplicated().sum()

df_limpio = df_limpio.drop_duplicates()

print("\nDuplicados encontrados:", duplicados_antes)
print("Duplicados eliminados:",
      duplicados_antes - df_limpio.duplicated().sum())

# 2. Identificar valores nulos
print("\nVALORES NULOS ANTES DEL TRATAMIENTO:")
print(df_limpio.isnull().sum())

# 3. Tratar valores nulos
df_limpio["precio"] = pd.to_numeric(
    df_limpio["precio"],
    errors="coerce"
)

df_limpio["precio"] = df_limpio["precio"].fillna(
    df_limpio["precio"].median()
)

df_limpio = df_limpio.dropna(
    subset=["nombre", "marca", "categoria"]
)

# 4. Convertir explícitamente el precio a número
df_limpio["precio"] = df_limpio["precio"].astype(float)

print("\nTIPOS DE DATOS DESPUES DE LIMPIAR:")
print(df_limpio.dtypes)

# 5. Consolidar los datos usando pd.concat()

# Dividir el dataset en dos fragmentos
parte_1 = df_limpio.iloc[:50]
parte_2 = df_limpio.iloc[50:]

# Unir los fragmentos
df_consolidado = pd.concat(
    [parte_1, parte_2],
    ignore_index=True
)

print("\n========== DATASET CONSOLIDADO ==========")

print(df_consolidado.head())

print("\nDIMENSIONES FINALES:")
print(df_consolidado.shape)

# 6. Guardar dataset limpio
df_consolidado.to_csv(
    "datos/datos_limpios.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nDATASET LIMPIO GUARDADO CORRECTAMENTE")
# ========== FILTRO DE MULTIPLES CONDICIONES ==========

filtro = df_limpio[
    (df_limpio["precio"] > 0) &
    (
        (df_limpio["categoria"] == "Perfumes para mujer") |
        (df_limpio["categoria"] == "Perfumes para hombre")
    ) &
    (df_limpio["disponibilidad"] == "https://schema.org/InStock")
]

print("\n========== FILTRO MULTIPLE ==========")
print("Productos filtrados:", len(filtro))
print(filtro[["nombre", "marca", "precio", "categoria"]].head(10))