# Proyecto Telco Churn – Pipeline DVC y MLflow

## 🎥 Video de presentación del proyecto 
🔗 https://drive.google.com/file/d/193S2B7LXzIZteEYVEh_pgidtS5NrmDru/view?usp=drive_link

## Resumen ejecutivo

Este proyecto implementa un pipeline completo y reproducible de Machine Learning para predecir el churn en una empresa de telecomunicaciones, integrando herramientas de MLOps modernas como **DVC**, **MLflow**, **GitHub Actions** y **DagsHub**. A lo largo de siete etapas progresivas, el trabajo aborda desde la ingesta y limpieza de datos hasta la experimentación controlada, validación automática mediante CI/CD y evaluación avanzada del modelo para su eventual despliegue.  
El pipeline permite versionar datasets, modelos y artefactos, registrar métricas comparables y garantizar la reproducibilidad total mediante `dvc repro`. El mejor modelo alcanzado (Regresión Logística con regularización débil) se integra a un flujo profesional que refleja buenas prácticas de ingeniería y ciencia de datos aplicadas a un caso real de churn.

## Descripción general

Este proyecto se desarrolla en el marco de la materia **Laboratorio de Minería de Datos II (ISTEA)** y tiene como objetivo construir un **pipeline completo, reproducible y trazable de Machine Learning** para predecir la **renuncia de clientes (Churn)** en una empresa de telecomunicaciones.

El enfoque combina varias herramientas clave del ecosistema de Ciencia de Datos y MLOps:

- **DVC** → para el versionado de datos, modelos y artefactos.
- **MLflow** → para registrar métricas, parámetros y experimentos.
- **Git + GitHub** → para control de versiones del código y trabajo colaborativo.
- **DagsHub** → como repositorio centralizado para sincronizar datos, modelos y experimentos.

La integración de estas tecnologías permite:

- Garantizar **reproducibilidad total** del pipeline mediante *dvc repro*.
- Versionar todos los artefactos relevantes (**datasets, modelos, métricas, plots**).
- Registrar la evolución del experimento bajo un flujo profesional de MLOps.
- Ejecutar validación continua del pipeline gracias a **GitHub Actions**.
- Comparar modelos y documentar su desempeño de manera transparente.

En conjunto, este proyecto constituye un ejemplo completo de cómo estructurar, entrenar, evaluar y versionar modelos de Machine Learning dentro de un entorno académico alineado con prácticas profesionales de la industria.

---

## Estructura general del proyecto

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

---

## Resumen de etapas y entregables

| Etapa | Descripción | Entregable principal |
|-------|-------------|----------------------|
| **1 — Setup inicial** | Configuración del entorno, repositorio, estructura base y conexión con DagsHub. | Repo estructurado + dataset crudo versionado en DVC. |
| **2 — Limpieza y features** | Ingesta, limpieza, codificación, escalado y generación de variables derivadas. | Dataset limpio y preparado versionado en DVC. |
| **3 — Entrenamiento de modelo** | Implementación de `train.py`, lectura de parámetros y registro de métricas. | Modelo entrenado + métricas registradas + artefactos versionados. |
| **4 — Experimentos** | Variación controlada del hiperparámetro C y análisis comparativo. | Reporte de experimentos y selección del mejor modelo. |
| **5 — CI/CD con GitHub Actions** | Workflow de validación automática del pipeline (`dvc pull` + `dvc repro`). | Pull Request validado correctamente por CI. |
| **6 — Iteración colaborativa** | Ramas `feat-*`, PRs, experimentos aislados y validación con CI. | Historial de ramas, PRs y merges documentados. |
| **7 — Evaluación avanzada (Producción)** | `evaluate.py`, métricas extendidas, curva ROC y artefactos finales. | Pipeline listo para evaluación avanzada y pre-despliegue. |

---

## Desarrollo del proyecto

### Etapa 1 – Configuración inicial

La primera etapa del proyecto tuvo como objetivo preparar el entorno de trabajo y sentar las bases del pipeline completo de Machine Learning. Para ello se realizaron las siguientes tareas:

- **Creación del entorno de trabajo con conda**, instalando todas las dependencias definidas en `requirements.txt` para asegurar un entorno reproducible y aislado.

- **Inicialización del repositorio en GitHub**, configurando el control de versiones del proyecto y manteniendo el historial completo de cambios del pipeline.

- **Conexión del repositorio con DagsHub** mediante la configuración de un remoto adicional en DVC. Esto permitió contar con un almacenamiento externo para los datos versionados y habilitar funciones adicionales como el MLflow remoto.

- **Definición de la estructura base del proyecto**, incluyendo carpetas clave como:
  - `src/` para scripts de procesamiento y entrenamiento  
  - `data/raw/` para el dataset original  
  - `models/` para almacenar artefactos generados  
  - `.github/workflows/` para la configuración de CI  

- **Versionado del dataset crudo con DVC**, subiéndolo al remoto configurado en DagsHub. Esto garantiza trazabilidad sobre futuras transformaciones, limpieza y preparación de datos.

👉 **Entregable de la etapa:**  
Repositorio estructurado, entorno configurado, dataset crudo versionado con DVC y sincronización correcta con GitHub + DagsHub.

---

### Etapa 2 – Limpieza y generación de variables

En esta etapa se implementó el proceso de preparación de datos necesario para que el pipeline pueda operar sobre información consistente, estandarizada y apta para el entrenamiento de modelos.

Las principales tareas realizadas fueron:

- **`make_data.py` — Ingesta del dataset crudo:**  
  Se cargó el dataset original desde `data/raw/` y se verificó su estructura, tipos de datos y presencia de valores faltantes. Este archivo actúa como punto de entrada del pipeline y garantiza que el dataset crudo esté siempre versionado mediante DVC.

- **`preprocess_data.py` — Limpieza y transformación del dataset:**  
  - Imputación y tratamiento de valores ausentes.  
  - Codificación de variables categóricas mediante *One-Hot Encoding* y transformaciones numéricas según corresponda.  
  - Estandarización / normalización de variables relevantes.  
  - Generación de **variables derivadas** necesarias para mejorar el rendimiento del modelo.  
  - Consolidación de todas las transformaciones en un dataset final *prepared*.

- **Versionado del dataset limpio y preparado con DVC:**  
  Tanto el dataset procesado (`data/processed/`) como el dataset final preparado (`data/prepared/`) fueron versionados con DVC, asegurando trazabilidad completa en cada ejecución del pipeline.

👉 **Entregable de la etapa:**  
Pipeline reproducible que incluye dataset crudo, dataset limpio y dataset preparado, todos versionados correctamente mediante DVC.

---

### Etapa 3 – Entrenamiento del modelo

En esta etapa se desarrolló el módulo responsable del entrenamiento del modelo base del proyecto. El objetivo fue construir un componente reproducible que tome los datos preparados, lea los hiperparámetros desde una configuración externa y produzca un modelo versionado.

Las acciones principales fueron:

- **Modelo base: Regresión Logística**  
  Se implementó un modelo de clasificación utilizando `LogisticRegression`, elegido como baseline por su interpretabilidad y comportamiento estable en problemas de churn.

- **Lectura de hiperparámetros desde `params/logreg.yaml`**  
  El script `src/train.py` recupera automáticamente los parámetros (regularización, solver, iteraciones, random_state, etc.) desde un archivo YAML, asegurando reproducibilidad total del entrenamiento.

- **Registro de métricas y parámetros en MLflow**  
  Cada ejecución documenta:  
  - Hiperparámetros utilizados  
  - Accuracy, Precision, Recall, F1 y ROC AUC  
  - Artefactos generados  
  Esto facilita la comparación de experimentos en fases posteriores.

- **Versionado del modelo entrenado con DVC**  
  El modelo producido (`models/telco_logreg.pkl`) queda registrado como *artifact* del pipeline.  
  Esto permite:  
  - reproducir entrenamientos,  
  - mantener historial de versiones,  
  - y sincronizar los artefactos con DagsHub.

👉 **Entregable de la etapa:**  
Modelo base entrenado, métricas registradas, hiperparámetros centralizados y artefactos versionados mediante DVC, integrados a la ejecución completa del pipeline.

---

### Etapa 4 – Ejecución de experimentos y análisis comparativo

En esta etapa se realizaron múltiples ejecuciones del modelo base modificando el hiperparámetro de regularización **C** de la Regresión Logística. El objetivo fue evaluar cómo influye la fuerza de regularización en el rendimiento del modelo y seleccionar la mejor configuración.

Para gestionar los experimentos se utilizó **MLflow en DagsHub**, lo que permitió registrar automáticamente:
- parámetros utilizados,
- métricas producidas,
- artefactos generados en cada run,
- historial completo de ejecuciones.

---

#### 4.1 Configuración de credenciales para MLflow (DagsHub)

Antes de ejecutar los experimentos, se configuraron las variables de entorno:

```
set MLFLOW_TRACKING_URI=https://dagshub.com/fernandezelias/Telco_Churn_ML_Pipeline.mlflow
set MLFLOW_TRACKING_USERNAME=fernandezelias
set MLFLOW_TRACKING_PASSWORD=<TOKEN_PERSONAL>
```

---

#### 4.2 Ejecución del pipeline para cada experimento

Para cada valor de **C**, se actualizó el archivo `params/logreg.yaml` y luego se ejecutó:

```
dvc repro
```

Esto garantizó una ejecución completamente reproducible del pipeline, regenerando métricas, artefactos y registrando cada run en MLflow.

---

#### 4.3 Versionado de artefactos

Después de cada experimento, se versionaron los cambios con DVC y Git:

```
dvc push
git add .
git commit -m "Entrega Etapa 4 - Experimentos con regularización"
git push
```

---

#### 4.4 Comparación exhaustiva de modelos

Además del análisis general de la etapa, se realizó una comparación más detallada del comportamiento del modelo de Regresión Logística frente a diferentes niveles de regularización (*C*). Esta comparación extendida permite evaluar no solo las métricas finales, sino también la estabilidad, consistencia y sensibilidad del modelo frente a cambios en su configuración.

##### Comportamiento general del modelo
La regularización controla la complejidad del modelo:  
- Valores **pequeños** de *C* → **mayor regularización** → modelo más simple y estable.  
- Valores **grandes** de *C* → **menor regularización** → modelo más flexible, potencialmente más sensible al ruido.

En un problema de churn —donde existe desbalance moderado y múltiples variables categóricas— la estabilidad del modelo es tan importante como la métrica final.

##### Resultados obtenidos
La siguiente tabla resume las métricas registradas para las cinco configuraciones evaluadas:

| Run | C | Accuracy | Precision | Recall | F1 | ROC AUC |
|-----|----|----------|-----------|--------|------|----------|
| **1** | 0.5  | 0.6800 | 0.5751 | 0.4580 | 0.5099 | 0.72195 |
| **2** | 1.0  | 0.6800 | 0.5751 | 0.4580 | 0.5099 | 0.72194 |
| **3** | 2.0  | 0.6800 | 0.5751 | 0.4580 | 0.5099 | 0.72194 |
| **4** | 5.0  | 0.6760 | 0.5642 | 0.4773 | 0.5171 | 0.72011 |
| **5** | 10.0 | **0.6845** | **0.5819** | 0.4691 | **0.5194** | **0.72581** |

##### Interpretación detallada
- **Alta estabilidad en C=0.5, 1.0 y 2.0:**  
  Estas configuraciones producen métricas prácticamente idénticas. Esto indica que la regresión logística, con regularización moderada-fuerte, se comporta de manera muy estable frente a la variabilidad del dataset.

- **Primer salto relevante en C=5.0:**  
  Aumenta levemente el *recall* (0.4773) y el *F1-score* (0.5171), lo que sugiere una mayor sensibilidad hacia la clase positiva, aunque con un pequeño sacrificio en *accuracy*.

- **Mejor configuración en C=10.0:**  
  Es la única que mejora simultáneamente:
  - **Accuracy**
  - **Precision**
  - **F1-score**
  - **ROC AUC**  

  Logra el equilibrio más sólido entre discriminar correctamente a la clase positiva (churn) y mantener un buen desempeño general.

##### Síntesis técnica
- La regresión logística es poco sensible a valores de regularización entre 0.5 y 2.0, lo que demuestra que el dataset está bien preparado y que el modelo lineal encuentra patrones estables.  
- Las configuraciones de regularización baja (mayor flexibilidad) permiten capturar relaciones adicionales que mejoran levemente el rendimiento sin indicar sobreajuste.  
- El modelo con **C=10** se destaca como mejor candidato para posteriores etapas del pipeline.

Esta comparación extendida complementa la tabla principal y justifica la selección final de hiperparámetros para continuar con el pipeline.

---

### 4.5 Conclusión de la etapa

- Los modelos con regularización más fuerte (C=0.5–2.0) mostraron métricas casi idénticas, reflejando estabilidad del pipeline.  
- El modelo con **C = 5.0** mejoró levemente recall y F1, aunque con menor accuracy.  
- El modelo con **C = 10.0** obtuvo el **mejor desempeño global**, liderando accuracy, precision, F1 y ROC AUC.  
- Todos los experimentos quedaron correctamente registrados en MLflow y versionados con DVC, cumpliendo con las exigencias de reproducibilidad.

👉 **Entregable de la etapa:** Reporte comparativo de las ejecuciones y registro completo de experimentos en **DagsHub MLflow**, con selección fundamentada del mejor modelo.

---

### Etapa 5 — CI/CD con GitHub Actions

La etapa 5 incorpora un proceso de **Integración Continua (CI)** utilizando **GitHub Actions**, con el objetivo de asegurar que el pipeline completo (gestionado con DVC) se ejecute correctamente cada vez que se realiza un *push* o *pull request* hacia el repositorio.

Este mecanismo permite validar automáticamente la reproducibilidad del workflow, evitando rupturas en el código y garantizando que los datos versionados puedan ser descargados y utilizados en un entorno limpio.

---

#### 5.1 Objetivo de la etapa

El workflow de CI debe garantizar que:

- El repositorio puede reconstruirse desde cero en GitHub Actions.
- Las dependencias del proyecto se instalan correctamente.
- Los datos almacenados en DVC Remote (DagsHub) pueden recuperarse mediante `dvc pull`.
- El pipeline completo se ejecuta sin errores con `dvc repro`.
- Las métricas producidas se muestran en el log de ejecución.
- Cada *Push* y *Pull Request* activa automáticamente el workflow para su validación.

---

#### 5.2 Configuración del workflow

El archivo principal del pipeline de CI se encuentra en:

```
.github/workflows/ci.yml
```

Dentro del workflow se implementaron los siguientes pasos:

- **Checkout del repositorio**
- **Instalación de dependencias**
- **Configuración de DVC** y autenticación mediante Secrets (`DAGSHUB_USER`, `DAGSHUB_TOKEN`)
- **Descarga de datos versionados** con `dvc pull`
- **Ejecución del pipeline completo** (`dvc repro`)
- **Impresión de métricas** generadas en la etapa de entrenamiento

Se retiraron dependencias de MLflow en `train.py` para evitar fallos en el entorno de CI.

---

#### 5.3 Validación mediante Pull Request

1. Se creó la rama:
   ```
   feat/ci-validation
   ```
2. Se modificó el archivo `README.md`.
3. Se abrió un Pull Request hacia `main`.
4. GitHub Actions ejecutó el workflow automáticamente.
5. El pipeline finalizó correctamente:

```
✔ All checks have passed
✔ Telco Churn CI / build (pull_request)
```

---

#### 5.4 Estado final de la etapa

✔ Workflow CI funcionando  
✔ Validación automática vía Pull Request  
✔ DVC Remote operativo desde GitHub Actions  
✔ Pipeline reproducible en entorno externo  
✔ Revisión limpia antes del merge  

**Entregable cumplido:** Pull Request validado por CI.

---

### Etapa 6 — Iteración colaborativa y experimentación con ramas

La etapa 6 consistió en simular un proceso colaborativo basado en **ramas**, **pull requests** y **validación automática por CI**, siguiendo un flujo profesional de experimentación con modelos.

El objetivo fue:
- Probar una variante del modelo base (Árbol de Decisión).
- Registrar sus parámetros y artefactos mediante DVC.
- Validar su funcionamiento con el pipeline completo en GitHub Actions.
- Integrarlo a `main` mediante **Pull Request** si el experimento era exitoso.

---

#### 6.1 Creación de una rama de experimento

Se creó una nueva rama de desarrollo:

```
git checkout -b feat/decision-tree
```

Esta rama aloja exclusivamente el experimento con un **DecisionTreeClassifier**.

---

#### 6.2 Nuevo archivo de parámetros

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

#### 6.3 Modificación temporal del pipeline

La etapa `train` del `dvc.yaml` fue ajustada para utilizar:

- `params/decision_tree.yaml`
- `models/telco_tree.pkl`
- `metrics_tree.json`

Con un comando equivalente a:

```
cmd: python src/train.py --data data/prepared/telco_churn_prepared.csv \
      --model models/telco_tree.pkl \
      --params params/decision_tree.yaml \
      --metrics metrics_tree.json
```

Esto garantizó que el experimento no afectara la rama principal.

---

#### 6.4 Ejecución del pipeline en local

```
dvc repro
```

Resultado principal:

```
accuracy = 0.684
```

El Decision Tree mostró un rendimiento similar al mejor modelo logístico.

---

#### 6.5 Registro del experimento

```
dvc push
git add .
git commit -m "Experimento: Decision Tree con nuevo params y artefactos DVC"
git push origin feat/decision-tree
```

---

#### 6.6 Pull Request del experimento

Se abrió un PR:

```
feat/decision-tree → main
```

GitHub Actions ejecutó:

- `dvc pull`
- `dvc repro`
- Verificación del pipeline completo

Resultado:

```
✔ All checks have passed
✔ Telco Churn CI / build (pull_request)
```

---

#### 6.7 Métricas del Decision Tree

| Métrica | Valor |
|--------|--------|
| Accuracy | **0.684** |
| Precision | similar al baseline |
| Recall | ligeramente inferior |
| F1-score | estable |
| ROC AUC | comparable al logístico |

---

#### 6.8 Merge del experimento a `main`

Aunque el modelo no superó al logístico, se realizó el merge porque:

- Demuestra flujo colaborativo
- CI validó completamente el pipeline
- Se preserva histórico de experimentos

Merge registrado:

```
Merge pull request #3 from fernandezelias/feat/decision-tree
```

---

#### 6.9 Resultado final de la etapa

✔ Ramas de experimento creadas  
✔ Modelos alternativos ejecutados  
✔ Artefactos versionados con DVC  
✔ CI validando automáticamente cada PR  
✔ Integración final en `main`  
✔ Documentación completa del proceso

**Entregable cumplido.**

---

## Etapa 7 — Evaluación avanzada y artefactos de producción (Bonus)

En la etapa 7 se añadió un módulo de **evaluación avanzada del modelo**, generando artefactos propios de un entorno de producción: métricas completas y curva ROC.

---

### 7.1 Nuevo módulo: `evaluate.py`

Se incorporó el archivo:

```
src/evaluate.py
```

Este script permite:

- Cargar un modelo entrenado (`.pkl`).
- Evaluar métricas avanzadas:  
  `accuracy`, `precision`, `recall`, `f1`, `roc_auc`.
- Generar y guardar una **curva ROC**.
- Guardar las métricas en un archivo JSON versionado.

---

### 7.2 Integración al pipeline DVC

Se añadió la etapa `evaluate` al `dvc.yaml`:

```yaml
evaluate:
  cmd: python src/evaluate.py --model models/telco_tree.pkl --data data/prepared/telco_churn_prepared.csv --metrics reports/metrics_tree_eval.json --plot reports/roc_tree.png
  deps:
    - src/evaluate.py
    - models/telco_tree.pkl
    - data/prepared/telco_churn_prepared.csv
  outs:
    - reports/metrics_tree_eval.json
    - reports/roc_tree.png
```

---

### 7.3 Ejecución del módulo

```
dvc repro
```

Resultado obtenido:

```
Evaluación completada.
{
  "accuracy": 0.6943,
  "precision": 0.6533,
  "recall": 0.3377,
  "f1": 0.4452,
  "roc_auc": 0.7415
}
```

---

### 7.4 Artefactos generados

| Artefacto | Descripción |
|----------|-------------|
| `reports/metrics_tree_eval.json` | Métricas completas del árbol de decisión |
| `reports/roc_tree.png` | Curva ROC generada |

Ambos fueron versionados con:

```
dvc push
```

---

### 7.5 Preparación para producción

Este módulo permite:

- Evaluar cualquier modelo versionado.
- Integrarse a APIs con **FastAPI** o dashboards en **Streamlit**.
- Servir como paso final del pipeline antes del deploy.

**Etapa 7 completada con éxito.**

---

## Conclusiones

El desarrollo del **pipeline Telco Churn** permitió integrar, de manera articulada, técnicas de Machine Learning con prácticas modernas de ingeniería de datos. A lo largo de sus distintas etapas, el proyecto avanzó desde la ingesta y limpieza inicial del dataset hasta la evaluación avanzada y la generación de artefactos aptos para un entorno de producción.

El uso de **DVC** garantizó la trazabilidad completa: cada dataset, modelo, métrica y gráfico quedó versionado, lo que asegura reproducibilidad total. Por su parte, **GitHub Actions** habilitó validaciones automáticas mediante CI, agregando robustez y control de calidad en cada *push* y *pull request*. La integración con **DagsHub** facilitó el seguimiento histórico de experimentos y métricas, permitiendo comparar modelos de manera transparente.

En cuanto a los resultados modelísticos, la **Regresión Logística** con regularización débil (C=10) ofreció el mejor equilibrio entre precisión, recall, F1 y AUC. El experimento con **Árbol de Decisión** mostró estabilidad y compatibilidad con el pipeline, aunque sin superar al modelo base, evidenciando la importancia de los experimentos controlados en escenarios de churn.

Finalmente, la incorporación del módulo `evaluate.py` permitió extender el pipeline hacia una fase previa al despliegue, generando métricas avanzadas y visualizaciones propias de un entorno productivo.

En conjunto, el proyecto demuestra:

- un flujo de trabajo profesional basado en control de versiones, datos reproducibles y CI/CD;  
- la capacidad de evaluar y comparar modelos bajo un mismo pipeline;  
- la preparación técnica para extender el proyecto hacia APIs (FastAPI) o dashboards (Streamlit);  
- y la consolidación de buenas prácticas de ingeniería y ciencia de datos aplicadas a un caso real de churn.

**El pipeline queda así completamente documentado, versionado y preparado para escalar hacia entornos de producción o nuevas iteraciones experimentales.**

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