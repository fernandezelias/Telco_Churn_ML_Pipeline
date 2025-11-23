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

Se evaluaron cinco corridas variando el hiperparámetro **C** de la Regresión Logística para analizar cómo influye la regularización en el rendimiento del modelo.

---

### 5.1 Hiperparámetros evaluados

| Run | C | Descripción |
|-----|----|-------------|
| **1** | 0.5  | Regularización fuerte |
| **2** | 1.0  | Regularización media |
| **3** | 2.0  | Regularización más débil |
| **4** | 5.0  | Baja regularización |
| **5** | 10.0 | Regularización mínima (modelo más flexible) |

---

### 5.2 Métricas comparativas

| Run | Accuracy | Precision | Recall | F1 | ROC AUC |
|-----|----------|-----------|--------|------|----------|
| **1 (C=0.5)**  | 0.6800 | 0.5751 | 0.4580 | 0.5099 | 0.72195 |
| **2 (C=1.0)**  | 0.6800 | 0.5751 | 0.4580 | 0.5099 | 0.72194 |
| **3 (C=2.0)**  | 0.6800 | 0.5751 | 0.4580 | 0.5099 | 0.72194 |
| **4 (C=5.0)**  | 0.6760 | 0.5642 | 0.4773 | 0.5171 | 0.72011 |
| **5 (C=10.0)** | **0.6845** | **0.5819** | 0.4691 | **0.5194** | **0.72581** |

---

### 5.3 Conclusiones

- Los valores pequeños de **C (0.5–2.0)** generan métricas prácticamente idénticas, lo que demuestra que el pipeline es **estable, reproducible y consistente** ante múltiples ejecuciones.
- El modelo con **C = 5.0** muestra un leve aumento del *recall* y del *F1-score*, lo que sugiere un mejor equilibrio entre falsos positivos y falsos negativos, aunque a costa de una ligera caída en *accuracy*.
- El modelo con **C = 10.0** ofrece el **mejor desempeño global**, alcanzando:
  - la **mayor accuracy (0.6845)**  
  - la **mayor precision (0.5819)**  
  - el **mejor F1-score (0.5194)**  
  - y el **mayor ROC AUC (0.72581)**  

💡 En conjunto, los resultados indican que **una regularización más débil (valores altos de C) permite que el modelo capture mejor las relaciones relevantes del dataset**, obteniendo un mejor poder predictivo sin generar signos evidentes de sobreajuste en esta etapa del proyecto.

---

CI Pipeline validated ✔

---

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
