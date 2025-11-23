import argparse, json, joblib, yaml, os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

import dagshub
import mlflow

# Activa MLflow en DagsHub
dagshub.init(repo_owner='fernandezelias',
             repo_name='Telco_Churn_ML_Pipeline',
             mlflow=True)

USE_MLFLOW = True


def load_params(pfile):
    """Carga los parámetros desde un archivo YAML."""
    with open(pfile) as f:
        return yaml.safe_load(f)


def build_model(model_cfg):
    """
    Construye y devuelve un clasificador de scikit-learn según la configuración recibida.

    El diccionario 'model_cfg' proviene del bloque 'model' de un archivo de parámetros
    ubicado en la carpeta 'params/' (por ejemplo, 'params/logreg.yaml', 'params/decision_tree.yaml', etc.).

    Modelos soportados:
      - LogisticRegression
      - SVC
      - DecisionTreeClassifier
      - RandomForestClassifier
    """
    mtype = model_cfg.get("type", "LogisticRegression")

    if mtype == "LogisticRegression":
        kwargs = {}
        for k in ["penalty", "C", "solver", "max_iter", "fit_intercept", "random_state", "n_jobs"]:
            if k in model_cfg:
                kwargs[k] = model_cfg[k]
        kwargs.setdefault("max_iter", 200)
        kwargs.setdefault("C", 1.0)
        return LogisticRegression(**kwargs)

    if mtype == "SVC":
        kwargs = {}
        for k in ["C", "kernel", "gamma", "degree", "coef0", "random_state"]:
            if k in model_cfg:
                kwargs[k] = model_cfg[k]
        # Habilita probabilidades para métricas como ROC AUC
        kwargs.setdefault("probability", True)
        return SVC(**kwargs)

    if mtype == "DecisionTreeClassifier":
        kwargs = {}
        for k in ["criterion", "max_depth", "min_samples_split", "min_samples_leaf", "random_state"]:
            if k in model_cfg:
                kwargs[k] = model_cfg[k]
        return DecisionTreeClassifier(**kwargs)

    if mtype == "RandomForestClassifier":
        kwargs = {}
        for k in ["n_estimators", "max_depth", "min_samples_split", "min_samples_leaf", "n_jobs", "random_state"]:
            if k in model_cfg:
                kwargs[k] = model_cfg[k]
        return RandomForestClassifier(**kwargs)

    raise ValueError(f"Tipo de modelo no soportado: {mtype}")


def compute_metrics(y_true, y_pred, y_proba=None, metric_list=None):
    """
    Calcula métricas de evaluación.
    Soporta: accuracy, precision, recall, f1, roc_auc (requiere y_proba).
    'metric_list' se define en params.yaml bajo 'metrics'.
    """
    if not metric_list:
        metric_list = ["accuracy"]

    out = {}
    for m in metric_list:
        if m == "accuracy":
            out["accuracy"] = float(accuracy_score(y_true, y_pred))
        elif m == "precision":
            out["precision"] = float(precision_score(y_true, y_pred, zero_division=0))
        elif m == "recall":
            out["recall"] = float(recall_score(y_true, y_pred, zero_division=0))
        elif m == "f1":
            out["f1"] = float(f1_score(y_true, y_pred, zero_division=0))
        elif m == "roc_auc" and y_proba is not None:
            out["roc_auc"] = float(roc_auc_score(y_true, y_proba))
    return out


def train(params, data_path, model_path, metrics_path):
    """
    Entrena el modelo definido en 'params', evalúa y persiste artefactos.
    - Lee datos de 'data_path' (CSV con columna 'churn' como objetivo binario).
    - Normaliza nombres de columnas a minúsculas para evitar errores por casing.
    - Realiza train/test split (opcionalmente estratificado).
    - Registra métricas en JSON y, si procede, en MLflow.
    """
    # 1) Carga de datos
    df = pd.read_csv(data_path)

    # 2) Variables predictoras (X) y variable objetivo (y)
    #    Se normalizan los nombres de columnas a minúsculas para evitar errores por mayúsculas/minúsculas.
    df.columns = df.columns.str.lower()
    target_col = "churn"
    if target_col not in df.columns:
        raise ValueError("No se encontró la columna objetivo 'churn' en el dataset.")
    X = df.drop(columns=[target_col])
    y = df[target_col]

    # 3) División en train/test
    split_cfg = params.get("split", {})
    test_size = split_cfg.get("test_size", 0.2)
    random_state = split_cfg.get("random_state", 42)
    use_stratify = split_cfg.get("stratify", True)

    Xtr, Xte, ytr, yte = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y if use_stratify else None
    )

    # 4) Construcción del modelo
    model = build_model(params.get("model", {"type": "LogisticRegression"}))

    # 5) Entrenamiento y logging
    if USE_MLFLOW:
        mlflow.set_experiment("telco_churn")
        with mlflow.start_run():
            mlflow.log_params(params.get("model", {}))

            model.fit(Xtr, ytr)
            ypred = model.predict(Xte)

            yproba = model.predict_proba(Xte)[:, 1] if hasattr(model, "predict_proba") else None
            metrics_to_compute = params.get("metrics", ["accuracy"])
            metrics = compute_metrics(yte, ypred, yproba, metrics_to_compute)

            for k, v in metrics.items():
                mlflow.log_metric(k, v)

            joblib.dump(model, model_path)
            mlflow.log_artifact(model_path)
    else:
        model.fit(Xtr, ytr)
        ypred = model.predict(Xte)

        yproba = model.predict_proba(Xte)[:, 1] if hasattr(model, "predict_proba") else None
        metrics_to_compute = params.get("metrics", ["accuracy"])
        metrics = compute_metrics(yte, ypred, yproba, metrics_to_compute)

        joblib.dump(model, model_path)

    # 6) Persistencia de métricas
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)

    # 7) Mensaje breve en consola
    main_metric = "accuracy" if "accuracy" in metrics else list(metrics.keys())[0]
    print(f"{main_metric}={metrics[main_metric]:.3f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--params", required=True)
    ap.add_argument("--metrics", required=True)
    a = ap.parse_args()

    p = load_params(a.params)
    train(p, a.data, a.model, a.metrics)