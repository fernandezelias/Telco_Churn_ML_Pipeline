# Proyecto Telco Churn – Pipeline DVC y MLflow

## 1. Descripción general

El presente proyecto forma parte de la materia **Laboratorio de Minería de Datos II (ISTEA)** y tiene por objetivo desarrollar un pipeline reproducible de Machine Learning orientado a predecir la **renuncia de clientes (Churn)** en un servicio de telecomunicaciones.

El trabajo se organiza en etapas progresivas que integran herramientas de versionado de datos (**DVC**), seguimiento de experimentos (**MLflow**) y control de versiones (**Git/DagsHub**).

---

## 2. Estructura general del proyecto

```
Telco_Churn_ML_Pipeline/
│
├── data/
│   ├── raw/                # Datos originales
│   ├── processed/          # Datos limpios y transformados
│   └── prepared/           # Datos listos para modelado
│
├── models/                 # Modelos entrenados
├── params/                 # Parámetros e hiperparámetros
├── src/                    # Scripts principales
│   ├── make_data.py
│   ├── preprocess_data.py
│   └── train.py
│
├── dvc.yaml                # Definición del pipeline DVC
├── requirements.txt        # Dependencias del entorno
└── README.md
```

---

## 3. Etapas del proyecto

### **Etapa 1 — Setup inicial**
- Creación del entorno local con **conda** y archivo `requirements.txt`.
- Configuración del repositorio Git y conexión con **DagsHub**.
- Estructuración de carpetas y carga del dataset crudo (`data/raw/telco_churn.csv`).
- Versionado inicial del dataset con **DVC**.

**Entregable:** repositorio con estructura base y dataset versionado.


### **Etapa 2 — Limpieza y features**
- Implementación de los procesos de preparación de datos.

> **Nota:** en lugar de un único archivo `data_prep.py`, se desdobló la etapa de preparación de datos en dos scripts para seguir una estructura más modular:
> - `make_data.py`: lectura e ingesta del dataset crudo.
> - `preprocess_data.py`: limpieza y generación de variables derivadas.

- Generación del dataset limpio (`data/processed`) y del dataset preparado (`data/prepared`).
- Actualización del archivo `dvc.yaml` con los nuevos *stages* correspondientes.

**Entregable:** pipeline reproducible con datasets crudo, limpio y preparado versionados.


### **Etapa 3 — Entrenamiento de modelo**
- Implementación del script `train.py` con un modelo base de **Regresión Logística**.
- Lectura de hiperparámetros desde `params/logreg.yaml`.
- Registro automático de métricas y artefactos con **MLflow**.
- Integración de **DVC** para versionar el modelo y el archivo de métricas (`metrics.json`).

**Entregable:** modelo entrenado, métricas registradas y pipeline completo hasta la etapa de entrenamiento.

---

## 4. Ejecución del pipeline

### 4.1 Configuración de credenciales (solo una vez por sesión)
```bash
set MLFLOW_TRACKING_URI=https://dagshub.com/fernandezelias/Telco_Churn_ML_Pipeline.mlflow
set MLFLOW_TRACKING_USERNAME=fernandezelias
set MLFLOW_TRACKING_PASSWORD=<TOKEN_PERSONAL>
```

### 4.2 Ejecución completa del pipeline
```bash
dvc repro
```

### 4.3 Versionado y registro de cambios
```bash
dvc push
git add .
git commit -m "Entrega Etapa 3 - Entrenamiento Telco Churn"
git push
```

---

## 6. Autor

**Autor:** Elías Fernández  
**Contacto:** elias.fernandez@istea.com.ar
 **Carrera:** Tecnicatura en Ciencia de Datos e Inteligencia Artificial (ISTEA)
 **Materia**: Laboratorio de Minería de Datos II 
 **Docente**: Diego Mosquera
 **Etapa entregada:** Etapa 3 – Entrenamiento del modelo