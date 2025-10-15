# Proyecto Telco Churn – Pipeline DVC y MLflow

## 1. Descripción general

El presente proyecto se desarrolla en el marco de la materia **Laboratorio de Minería de Datos II (ISTEA)**.  
Su objetivo es construir un **pipeline reproducible de Machine Learning** para predecir la **renuncia de clientes (Churn)** en una empresa de telecomunicaciones.

El trabajo integra las herramientas **DVC** (versionado de datos), **MLflow** (seguimiento de experimentos) y **Git** (control de versiones), con repositorios sincronizados en **GitHub** y **DagsHub**.  
De esta manera, se garantiza la trazabilidad completa del proceso, desde la ingesta de datos hasta el entrenamiento del modelo base.

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

## 3. Desarrollo del proyecto

### **Etapa 1 – Configuración inicial**
- Creación del entorno de trabajo con **conda** y archivo `requirements.txt`.
- Inicialización del repositorio local y configuración con **GitHub**.
- Sincronización con **DagsHub** para el seguimiento de experimentos.  
- Definición de la estructura de carpetas y carga del dataset crudo (`data/raw/telco_churn.csv`).
- Versionado inicial del dataset mediante **DVC**.

**Resultado:** repositorio estructurado y dataset crudo versionado en ambos remotos.


### **Etapa 2 – Limpieza y generación de variables**
- Implementación de los procesos de preparación de datos.

> **Nota técnica:** en lugar de un único archivo `data_prep.py`, se optó por una estructura modular que mejora la legibilidad del código y la trazabilidad del pipeline:
> - `make_data.py`: lectura e ingesta del dataset crudo.  
> - `preprocess_data.py`: limpieza, transformación y creación de variables derivadas.

- Creación del dataset limpio (`data/processed`) y preparado (`data/prepared`).
- Actualización del archivo `dvc.yaml` con los *stages* correspondientes a esta etapa.

**Resultado:** pipeline reproducible con datasets crudo, limpio y preparado versionados con DVC.


### **Etapa 3 – Entrenamiento del modelo**
- Implementación del script `train.py` con un modelo base de **Regresión Logística**.  
- Lectura de hiperparámetros desde `params/logreg.yaml`.
- Registro automático de métricas, parámetros y artefactos mediante **MLflow**.  
- Versionado del modelo entrenado y del archivo de métricas (`metrics.json`) con **DVC**.
- Sincronización completa del repositorio local con **GitHub** y **DagsHub**.

**Resultado:** modelo entrenado, métricas registradas y pipeline completo hasta la etapa de entrenamiento, con seguimiento de experimentos y versionado de artefactos.

---

## 4. Ejecución y registro de la Etapa 3

La siguiente guía describe los comandos necesarios para reproducir el pipeline y registrar los resultados correspondientes a la **Etapa 3**.  

### 4.1 Configuración de credenciales (solo una vez por sesión)
```bash
set MLFLOW_TRACKING_URI=https://dagshub.com/fernandezelias/Telco_Churn_ML_Pipeline.mlflow
set MLFLOW_TRACKING_USERNAME=fernandezelias
set MLFLOW_TRACKING_PASSWORD=<TOKEN_PERSONAL>
```

### 4.2 Ejecución del pipeline completo
```bash
dvc repro
```

### 4.3 Versionado y registro de resultados
```bash
dvc push
git add .
git commit -m "Entrega Etapa 3 - Entrenamiento Telco Churn"
git push
```

Estos comandos actualizan los artefactos y los repositorios remotos, garantizando la trazabilidad del experimento tanto en GitHub como en DagsHub.

---

## 5. Autoría

- **Autor:** Elías Fernández
- **Contacto:** fernandezelias86@gmail.com
- **Institución:** Instituto Superior Tecnológico Empresarial Argentino (ISTEA)
- **Carrera:** Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial
- **Etapa entregada:** Etapa 3 – Entrenamiento del modelo
- **Repositorios:** 
    [GitHub](https://github.com/fernandezelias/Telco_Churn_ML_Pipeline) 
    [DagsHub](https://dagshub.com/fernandezelias/Telco_Churn_ML_Pipeline)