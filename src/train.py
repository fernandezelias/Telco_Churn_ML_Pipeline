import argparse
import json
import joblib
import yaml
import os
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
)


# ============================================================
# 1. Carga de parámetros
# ============================================================

def load_params(pfile):
    """Carga los parámetros desde un archivo YAML."""
    with open(pfile) as f:
        return yaml.safe_load(f)


# ============================================================
# 2. Construcción dinámica del modelo
# ============================================================

def build_model(model_cfg):
    """
    Construye un clasificador scikit-learn según el diccionario `model_cfg`.
    Soporta:
      - LogisticRegression
      - SVC
      - DecisionTreeClassifier
      - RandomForestClassifier
    """
    mtype = model_cfg.get("type", "LogisticRegression")

    if mtype == "LogisticRegression":
        kwargs = {k: v for k, v in model_cfg.items() if k in
                  ["penalty", "C", "solver", "max_iter", "fit_intercept", "random_state", "n_jobs"]}
        kwargs.setdefault("max_iter", 200)
        return LogisticRegression(**kwargs)

    elif mtype == "SVC":
        kwargs = {k: v for k, v in model_cfg.items() if k in
                  ["C", "kernel", "gamma", "degree", "coef0", "random_state"]}
        kwargs.setdefault("probability", True)  # Necesario para ROC-AUC
        return SVC(**kwargs)

    elif mtype == "DecisionTreeClassifier":
        kwargs = {k: v for k, v in model_cfg.items() if k in
                  ["criterion", "max_depth", "min_samples_split", "min_samples_leaf", "random_state"]}
        return DecisionTreeClassifier(**kwargs)

    elif mtype == "RandomForestClassifier":
        kwargs = {k: v for k, v in model_cfg.items() if k in
                  ["n_estimators", "max_depth", "min_samples_split", "min_samples_leaf", "n_jobs", "random_state"]}
        return RandomForestClassifier(**kwargs)

    else:
        raise ValueError(f"Modelo no soportado: {mtype}")


# ============================================================
# 3. Cálculo de métricas
# ============================================================

def compute_metrics(y_true, y_pred, y_proba=None, metric_list=None):
    """
    Calcula accuracy, precision, recall, f1, roc_auc (si hay probabilidades).
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


# ============================================================
# 4. Entrenamiento principal
# ============================================================

def train(params, data_path, model_path, metrics_path):
    """
    Entrena un modelo según parámetros, calcula métricas
    y persiste el modelo y las métricas.
    """

    # --- Lectura del dataset ---
    df = pd.read_csv(data_path)
    df.columns = df.columns.str.lower()

    if "churn" not in df.columns:
        raise ValueError("La columna objetivo 'churn' no está en el dataset.")

    X = df.drop(columns=["churn"])
    y = df["churn"]

    # --- Train/Test split ---
    split_cfg = params.get("split", {})
    Xtr, Xte, ytr, yte = train_test_split(
        X,
        y,
        test_size=split_cfg.get("test_size", 0.2),
        random_state=split_cfg.get("random_state", 42),
        stratify=y if split_cfg.get("stratify", True) else None
    )

    # --- Construcción y entrenamiento del modelo ---
    model = build_model(params.get("model", {}))
    model.fit(Xtr, ytr)

    # --- Predicciones ---
    ypred = model.predict(Xte)
    yproba = model.predict_proba(Xte)[:, 1] if hasattr(model, "predict_proba") else None

    # --- Métricas ---
    metrics_to_compute = params.get("metrics", ["accuracy"])
    metrics = compute_metrics(yte, ypred, yproba, metrics_to_compute)

    # --- Guardado del modelo ---
    joblib.dump(model, model_path)

    # --- Guardado de métricas ---
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)

    # --- Log corto en consola ---
    main_metric = "accuracy" if "accuracy" in metrics else list(metrics.keys())[0]
    print(f"{main_metric}={metrics[main_metric]:.3f}")


# ============================================================
# 5. CLI
# ============================================================

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--params", required=True)
    ap.add_argument("--metrics", required=True)
    a = ap.parse_args()

    p = load_params(a.params)
    train(p, a.data, a.model, a.metrics)