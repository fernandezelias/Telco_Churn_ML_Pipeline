# Proyecto Telco Churn – Pipeline DVC y MLflow

## 1. Descripción general

El presente proyecto se desarrolla en el marco de la materia **Laboratorio de Minería de Datos II (ISTEA)**. Su objetivo es construir un **pipeline reproducible de Machine Learning** para predecir la **renuncia de clientes (Churn)** en una empresa de telecomunicaciones.

El trabajo integra las herramientas **DVC** (versionado de datos), **MLflow** (seguimiento de experimentos) y **Git** (control de versiones), con repositorios sincronizados en **GitHub** y **DagsHub**.
Esto permite garantizar la trazabilidad completa del proceso, desde la ingesta de datos hasta el entrenamiento y comparación de modelos.

## 2. Estructura general del proyecto

```
Telco_Churn_ML_Pipeline/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── prepared/
│
├── models/
├── params/
├── src/
│   ├── make_data.py
│   ├── preprocess_data.py
│   └── train.py
│
├── dvc.yaml
├── requirements.txt
└── README.md
```

## 3. Desarrollo del proyecto

### Etapa 1 – Configuración inicial
- Creación del entorno con conda.
- Inicialización del repositorio y configuración con GitHub.
- Conexión con DagsHub como remoto adicional.
- Versionado del dataset crudo con DVC.

### Etapa 2 – Limpieza y generación de variables
- `make_data.py`: ingesta del dataset crudo.
- `preprocess_data.py`: limpieza, encoding, escalado y variables derivadas.
- Datasets limpios y preparados versionados con DVC.

### Etapa 3 – Entrenamiento del modelo
- Modelo base: **Regresión Logística**.
- Lectura de hiperparámetros desde `params/logreg.yaml`.
- Registro de métricas y parámetros en MLflow.
- Versionado del modelo con DVC.

## 4. Ejecución y registro de la Etapa 3

### 4.1 Configuración de credenciales
```
set MLFLOW_TRACKING_URI=https://dagshub.com/fernandezelias/Telco_Churn_ML_Pipeline.mlflow
set MLFLOW_TRACKING_USERNAME=fernandezelias
set MLFLOW_TRACKING_PASSWORD=<TOKEN_PERSONAL>
```

### 4.2 Ejecución
```
dvc repro
```

### 4.3 Versionado
```
dvc push
git add .
git commit -m "Entrega Etapa 3 - Entrenamiento Telco Churn"
git push
```

## 5. Etapa 4 — Experimentos y análisis comparativo

Se evaluaron cinco corridas variando el hiperparámetro **C** de la Regresión Logística.

### 5.1 Hiperparámetros

| Run | C | Descripción |
|-----|----|-------------|
| 1 | 2.0 | Modelo base |
| 2 | 2.0 | Re-ejecución |
| 3 | 2.0 | Re-ejecución |
| 4 | 5.0 | Menor regularización |
| 5 | 10.0 | Regularización mínima |

### 5.2 Métricas comparativas

| Run | Accuracy | Precision | Recall | F1 | ROC AUC |
|-----|----------|-----------|--------|------|----------|
| 1 | 0.6800 | 0.5751 | 0.4580 | 0.5099 | 0.72194 |
| 2 | 0.6800 | 0.5751 | 0.4580 | 0.5099 | 0.72194 |
| 3 | 0.6800 | 0.5751 | 0.4580 | 0.5099 | 0.72195 |
| 4 | 0.6760 | 0.5642 | 0.4773 | 0.5171 | 0.72011 |
| 5 | 0.6845 | 0.5819 | 0.4691 | 0.5194 | 0.72581 |

### 5.3 Conclusiones

El modelo con **C = 10.0 (Run 5)** obtiene el mejor balance entre precisión, AUC y F1-score.

## 6. Integrantes del equipo

**Autores:**
- Elías Fernández — elias.fernandez@istea.com.ar
- Fiorela Macheroni — fiorela.macheroni@istea.com.ar
- Sebastián Fuentes — sebastian.fuentes@istea.com.ar

**Institución:** ISTEA  
**Carrera:** Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial  
**Materia:** Laboratorio de Minería de Datos  
**Etapa entregada:** Etapa 4 – Experimentos y comparación de modelos

**Repositorios:**
- GitHub: https://github.com/fernandezelias/Telco_Churn_ML_Pipeline
- DagsHub: https://dagshub.com/fernandezelias/Telco_Churn_ML_Pipeline
