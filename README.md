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

## 6. Etapa 5 — CI/CD con GitHub Actions

La etapa 5 incorpora **Integración Continua (CI)** mediante **GitHub Actions**, permitiendo verificar automáticamente que el pipeline funciona correctamente ante cada *push* o *pull request*.

### 6.1 Objetivo de la etapa
Garantizar que:
- El pipeline DVC (`dvc repro`) se ejecuta correctamente en un entorno limpio.
- Los datos versionados pueden ser obtenidos (`dvc pull`) desde el remoto.
- No existen rupturas en el código del proyecto.
- Cada *Pull Request* activa el workflow automáticamente.

### 6.2 Configuración utilizada
El workflow principal se encuentra en:

```
.github/workflows/ci.yml
```

Incluye:
- Checkout del repositorio.
- Instalación de dependencias.
- Ejecución de `dvc pull`.
- Ejecución completa del pipeline: `dvc repro`.
- Visualización de métricas generadas.

Se eliminaron dependencias a MLflow y DagsHub dentro del archivo `train.py` para asegurar compatibilidad con el entorno de CI.

### 6.3 Validación mediante Pull Request
Para validar el funcionamiento:
1. Se creó una rama de trabajo:  
   `feat/ci-validation`
2. Se modificó el archivo `README.md`.
3. Se ejecutó un *Pull Request* hacia `main`.
4. GitHub Actions ejecutó el workflow automáticamente.
5. El workflow finalizó correctamente:

```
✔ All checks have passed
✔ Telco Churn CI / build (pull_request)
```

**Resultado:** La etapa 5 queda correctamente implementada y validada.

---

## CI Status

✔️ **CI Pipeline validated** — La integración continua con GitHub Actions reproduce el pipeline completo sin errores.

---

## Integrantes del equipo

- Elías Fernández — elias.fernandez@istea.com.ar
- Fiorela Macheroni — fiorela.macheroni@istea.com.ar
- Sebastián Fuentes — sebastian.fuentes@istea.com.ar

**Institución:** ISTEA  
**Carrera:** Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial  
**Materia:** Laboratorio de Minería de Datos  
**Etapa entregada:** Etapa 4–5 – Experimentos, comparación de modelos y CI/CD

**Repositorios:**
- GitHub: https://github.com/fernandezelias/Telco_Churn_ML_Pipeline
- DagsHub: https://dagshub.com/fernandezelias/Telco_Churn_ML_Pipeline