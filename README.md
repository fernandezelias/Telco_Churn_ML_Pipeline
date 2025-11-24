# Proyecto Telco Churn – Pipeline DVC y MLflow

## 1. Descripción general

El presente proyecto se desarrolla en el marco de la materia **Laboratorio de Minería de Datos II (ISTEA)**. Su objetivo es construir un **pipeline reproducible de Machine Learning** para predecir la **renuncia de clientes (Churn)** en una empresa de telecomunicaciones.

El trabajo integra las herramientas **DVC** (versionado de datos), **MLflow** (seguimiento de experimentos) y **Git** (control de versiones), con repositorios sincronizados en **GitHub** y **DagsHub**.
Esto permite garantizar la trazabilidad completa del proceso, desde la ingesta de datos hasta el entrenamiento y comparación de modelos.

## 2. Estructura general del proyecto

```
Telco_Churn_ML_Pipeline/
│
├── .dvc/
│   └── config
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── prepared/
│
├── models/
│   ├── telco_logreg.pkl
│   ├── telco_tree.pkl
│   └── test_model.pkl
│
├── params/
│   ├── logreg.yaml
│   └── decision_tree.yaml
│
├── src/
│   ├── make_data.py
│   ├── preprocess_data.py
│   └── train.py
│
├── dvc.yaml
├── dvc.lock
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

## 7. Etapa 6 — Iteración colaborativa y experimentación con ramas

La etapa 6 consistió en simular un proceso colaborativo basado en **ramas**, **pull requests** y **validación automática por CI**, siguiendo un flujo profesional de experimentación con modelos.

El objetivo fue:
- Probar una variante del modelo base (Árbol de Decisión).
- Registrar sus parámetros y artefactos mediante DVC.
- Validar su funcionamiento con el pipeline completo en GitHub Actions.
- Integrarlo a `main` mediante **Pull Request** si el experimento era exitoso.

---

### 7.1 Creación de una rama de experimento

Se creó una nueva rama de desarrollo:

```
git checkout -b feat/decision-tree
```

Esta rama aloja exclusivamente el experimento con un **DecisionTreeClassifier**.

---

### 7.2 Nuevo archivo de parámetros

Se añadió un archivo específico:

```
params/decision_tree.yaml
```

Con la siguiente configuración:

- `model.type: DecisionTreeClassifier`
- `criterion: gini`
- `max_depth: 5`
- `min_samples_split: 10`
- `random_state: 42`

Esto permite ejecutar el mismo pipeline DVC con un modelo totalmente diferente al de la rama `main`.

---

### 7.3 Modificación temporal del pipeline (solo en la rama de experimento)

La etapa `train` del `dvc.yaml` fue actualizada para usar:

- `params/decision_tree.yaml`
- `models/telco_tree.pkl`
- `metrics_tree.json`

Ejemplo:

```
cmd: python src/train.py --data data/prepared/telco_churn_prepared.csv                          --model models/telco_tree.pkl                          --params params/decision_tree.yaml                          --metrics metrics_tree.json
```

Esto garantizó que **el experimento no alterara el modelo de la rama principal**.

---

### 7.4 Ejecución del pipeline en local

Desde la misma rama:

```
dvc repro
```

Salida obtenida:

```
accuracy=0.684
```

Esto indica que el **árbol de decisión** logró una performance inicial similar al mejor modelo de regresión logística (C=10.0).

---

### 7.5 Registro del experimento

Tras ejecutarlo, los artefactos fueron enviados al remoto de DVC:

```
dvc push
git add .
git commit -m "Experimento: Decision Tree con nuevo params y artefactos DVC"
git push origin feat/decision-tree
```

---

### 7.6 Pull Request del experimento

Se abrió un PR desde:

```
feat/decision-tree → main
```

GitHub Actions ejecutó automáticamente el workflow completo de CI:

- `dvc pull`
- `dvc repro`
- Validación del pipeline end-to-end

El resultado fue exitoso:

```
✔ All checks have passed
✔ Telco Churn CI / build (pull_request)
```

Esto confirma que el experimento es **reproducible**, **estable** y compatible con todo el pipeline.

---

### 7.7 Métricas del Decision Tree

Se generaron las siguientes métricas (según `metrics_tree.json`):

| Métrica | Valor |
|--------|--------|
| Accuracy | **0.684** |
| Precision | similar al baseline |
| Recall | ligeramente inferior |
| F1-score | estable |
| ROC AUC | comparable al modelo logístico |

**Conclusión técnica:**  
El Decision Tree no mejoró sustancialmente al mejor modelo de Regresión Logística (C=10.0), pero sí mostró estabilidad y compatibilidad total con el pipeline.

---

### 7.8 Merge del experimento a `main`

Aunque el Decision Tree **no superó** al mejor modelo logístico, se procedió al *merge* porque el objetivo de la Etapa 6 es **demostrar el flujo de trabajo colaborativo**:

- Creación de rama
- Ejecución de experimento aislado
- Validación automática por CI
- Fusión de cambios controlada

El merge fue completado con:

```
Merge pull request #3 from fernandezelias/feat/decision-tree
```

Esto deja registrado el historial completo del experimento y la integración en `main`, cumpliendo con el entregable solicitado.

---

### 7.9 Resultado final de la etapa

✔ Se crearon ramas de experimento (`feat-*`).  
✔ Se ejecutaron modelos alternativos.  
✔ Se versionaron parámetros, modelos y métricas con DVC.  
✔ Se validó automáticamente cada PR con CI.  
✔ Se realizó el merge final hacia `main`.  
✔ Se documentó todo el proceso.

**Entregable cumplido:** historial de PRs, ramas y merges correctamente generados y registrados en GitHub.

---

## Integrantes del equipo

- Elías Fernández — elias.fernandez@istea.com.ar
- Fiorela Macheroni — fiorela.macheroni@istea.com.ar
- Sebastián Fuentes — sebastian.fuentes@istea.com.ar

**Institución:** ISTEA

**Carrera:** Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial

**Materia:** Laboratorio de Minería de Datos  

**Repositorios:**
- GitHub: https://github.com/fernandezelias/Telco_Churn_ML_Pipeline
- DagsHub: https://dagshub.com/fernandezelias/Telco_Churn_ML_Pipeline