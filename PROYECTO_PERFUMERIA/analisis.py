
# ==========================================
# PROYECTO: PREDICCION DE PRECIOS DE PERFUMES
# FASE III: ANALISIS EXPLORATORIO DE DATOS
# ==========================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar dataset limpio
df = pd.read_csv("datos/datos_limpios.csv")

# Configurar visualizaciones
sns.set_theme(style="whitegrid")

# ==========================================
# 1. ANALISIS ESTADISTICO DE LOS PRECIOS
# ==========================================

print("========== ANALISIS ESTADISTICO ==========")

print(df["precio"].describe())

print("\nPRECIO PROMEDIO:")
print(df["precio"].mean())

print("\nPRECIO MAXIMO:")
print(df["precio"].max())

print("\nPRECIO MINIMO:")
print(df["precio"].min())

# ==========================================
# 2. DISTRIBUCION DE PRECIOS
# ==========================================

plt.figure(figsize=(10, 5))

sns.histplot(
    data=df,
    x="precio",
    bins=15,
    kde=True
)

plt.title("Distribucion de precios de perfumes")
plt.xlabel("Precio (COP)")
plt.ylabel("Cantidad de perfumes")

plt.tight_layout()
plt.show()

# ==========================================
# 3. PRECIO PROMEDIO POR MARCA
# ==========================================

precio_por_marca = (
    df.groupby("marca")["precio"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12, 6))

sns.barplot(
    x=precio_por_marca.values,
    y=precio_por_marca.index
)

plt.title("Top 10 marcas con mayor precio promedio")
plt.xlabel("Precio promedio (COP)")
plt.ylabel("Marca")

plt.tight_layout()
plt.show()

# ==========================================
# 4. COMPARACION DE PRECIOS POR MARCA
# ==========================================

# Seleccionar las 10 marcas con más productos
marcas_frecuentes = df["marca"].value_counts().head(10).index

df_marcas = df[df["marca"].isin(marcas_frecuentes)]

plt.figure(figsize=(12, 6))

sns.boxplot(
    data=df_marcas,
    x="marca",
    y="precio"
)

plt.title("Variacion de precios por marca")
plt.xlabel("Marca")
plt.ylabel("Precio (COP)")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# ==========================================
# 5. ANALISIS DE VARIABLES PARA EL MODELO
# ==========================================

print("\n========== ANALISIS DE VARIABLES ==========")

print("\nPRODUCTOS POR MARCA:")
print(df["marca"].value_counts().head(15))

print("\nPRODUCTOS POR CATEGORIA:")
print(df["categoria"].value_counts())

print("\nPRECIOS PROMEDIO POR MARCA:")
print(
    df.groupby("marca")["precio"]
    .agg(["count", "mean"])
    .sort_values("mean", ascending=False)
    .head(15)
)
