
# ==========================================
# PROYECTO: PREDICCION DE PRECIOS DE PERFUMES
# FASE IV: MODELO DE MACHINE LEARNING
# ==========================================
import os
import pandas as pd

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.dummy import DummyRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# ==========================================
# 1. CARGAR DATASET
# ==========================================

df = pd.read_csv("datos/datos_limpios.csv")

print("========== DATASET ==========")
print("Dimensiones:", df.shape)


# ==========================================
# 2. DEFINIR VARIABLES
# ==========================================

# Variables predictoras
X = df[["marca", "categoria"]]

# Variable objetivo
y = df["precio"]


# ==========================================
# 3. DIVIDIR LOS DATOS
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\nENTRENAMIENTO:", X_train.shape)
print("PRUEBA:", X_test.shape)


# ==========================================
# 4. PREPARAR VARIABLES CATEGORICAS
# ==========================================

preprocesador = ColumnTransformer(
    transformers=[
        (
            "categoricas",
            OneHotEncoder(handle_unknown="ignore"),
            ["marca", "categoria"]
        )
    ]
)


# ==========================================
# 5. MODELO DE REFERENCIA
# ==========================================

modelo_referencia = DummyRegressor(strategy="mean")

modelo_referencia.fit(X_train, y_train)

predicciones_referencia = modelo_referencia.predict(X_test)

mae_referencia = mean_absolute_error(
    y_test,
    predicciones_referencia
)

rmse_referencia = mean_squared_error(
    y_test,
    predicciones_referencia
) ** 0.5

r2_referencia = r2_score(
    y_test,
    predicciones_referencia
)

print("\n========== MODELO DE REFERENCIA ==========")
print("MAE:", mae_referencia)
print("RMSE:", rmse_referencia)
print("R2:", r2_referencia)


# ==========================================
# 6. RANDOM FOREST BASE
# ==========================================

modelo_base = Pipeline(
    steps=[
        ("preparacion", preprocesador),
        ("modelo", RandomForestRegressor(random_state=42))
    ]
)

modelo_base.fit(X_train, y_train)

predicciones_base = modelo_base.predict(X_test)

mae_base = mean_absolute_error(y_test, predicciones_base)
rmse_base = mean_squared_error(y_test, predicciones_base) ** 0.5
r2_base = r2_score(y_test, predicciones_base)

print("\n========== RANDOM FOREST BASE ==========")
print("MAE:", mae_base)
print("RMSE:", rmse_base)
print("R2:", r2_base)


# ==========================================
# 7. OPTIMIZACION CON GRIDSEARCHCV
# ==========================================

parametros = {
    "modelo__n_estimators": [50, 100, 200],
    "modelo__max_depth": [None, 5, 10],
    "modelo__min_samples_split": [2, 5]
}

busqueda = GridSearchCV(
    estimator=modelo_base,
    param_grid=parametros,
    cv=5,
    scoring="neg_mean_absolute_error",
    n_jobs=-1
)

busqueda.fit(X_train, y_train)

mejor_modelo = busqueda.best_estimator_

print("\n========== OPTIMIZACION ==========")
print("MEJORES PARAMETROS:")
print(busqueda.best_params_)


# ==========================================
# 8. EVALUAR MODELO OPTIMIZADO
# ==========================================

predicciones_optimizadas = mejor_modelo.predict(X_test)

mae_optimizado = mean_absolute_error(
    y_test,
    predicciones_optimizadas
)

rmse_optimizado = mean_squared_error(
    y_test,
    predicciones_optimizadas
) ** 0.5

r2_optimizado = r2_score(
    y_test,
    predicciones_optimizadas
)

print("\n========== MODELO OPTIMIZADO ==========")
print("MAE:", mae_optimizado)
print("RMSE:", rmse_optimizado)
print("R2:", r2_optimizado)


# ==========================================
# 9. COMPARAR LOS MODELOS
# ==========================================

comparacion = pd.DataFrame({
    "Modelo": [
        "Referencia",
        "Random Forest Base",
        "Random Forest Optimizado"
    ],
    "MAE": [
        mae_referencia,
        mae_base,
        mae_optimizado
    ],
    "RMSE": [
        rmse_referencia,
        rmse_base,
        rmse_optimizado
    ],
    "R2": [
        r2_referencia,
        r2_base,
        r2_optimizado
    ]
})

print("\n========== COMPARACION FINAL ==========")
print(comparacion.to_string(index=False))


# ==========================================
# 10. RESULTADO FINAL
# ==========================================

print("\n========== PROCESO FINALIZADO ==========")

# ==========================================
# 11. GUARDAR RESULTADOS DEL MODELO
# ==========================================

os.makedirs("resultados", exist_ok=True)

comparacion.to_csv(
    "resultados/comparacion_modelos.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nCOMPARACION GUARDADA CORRECTAMENTE")

# ==========================================
# 12. VALIDACION CRUZADA REPETIDA
# ==========================================

from sklearn.model_selection import RepeatedKFold, cross_validate
import numpy as np

print("\n========== VALIDACION CRUZADA REPETIDA ==========")

# Crear el modelo con los mismos datos y variables
modelo_validacion = Pipeline(
    steps=[
        ("preparacion", preprocesador),
        ("modelo", RandomForestRegressor(random_state=42))
    ]
)

# Configurar 5 particiones repetidas 3 veces
validacion = RepeatedKFold(
    n_splits=5,
    n_repeats=3,
    random_state=42
)

# Evaluar el modelo
resultados = cross_validate(
    modelo_validacion,
    X,
    y,
    cv=validacion,
    scoring={
        "mae": "neg_mean_absolute_error",
        "rmse": "neg_root_mean_squared_error",
        "r2": "r2"
    },
    n_jobs=-1
)

# Convertir errores a valores positivos
mae_promedio = -resultados["test_mae"].mean()
rmse_promedio = -resultados["test_rmse"].mean()
r2_promedio = resultados["test_r2"].mean()

print("\nRESULTADOS PROMEDIO:")
print("MAE:", mae_promedio)
print("RMSE:", rmse_promedio)
print("R2:", r2_promedio)

print("\nDESVIACION ESTANDAR DEL R2:")
print(np.std(resultados["test_r2"]))

print("\nVALIDACION FINALIZADA")
# ==========================================
# 13. GUARDAR EL MODELO
# ==========================================

import joblib
import os

os.makedirs("resultados", exist_ok=True)

modelo_final = Pipeline(
    steps=[
        ("preparacion", preprocesador),
        ("modelo", RandomForestRegressor(random_state=42))
    ]
)

modelo_final.fit(X, y)

joblib.dump(
    modelo_final,
    "resultados/modelo_perfumes.pkl"
)

print("\nMODELO GUARDADO CORRECTAMENTE")
