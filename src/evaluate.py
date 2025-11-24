import argparse
import json
import joblib
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    RocCurveDisplay
)
import matplotlib.pyplot as plt
import os

def evaluate(model_path, data_path, out_metrics, out_plot):
    # 1) Cargar modelo
    model = joblib.load(model_path)

    # 2) Cargar datos
    df = pd.read_csv(data_path)
    df.columns = df.columns.str.lower()

    target_col = "churn"
    X = df.drop(columns=[target_col])
    y = df[target_col]

    # 3) Predicciones
    y_pred = model.predict(X)
    y_proba = model.predict_proba(X)[:, 1] if hasattr(model, "predict_proba") else None

    # 4) Métricas
    metrics = {
        "accuracy": float(accuracy_score(y, y_pred)),
        "precision": float(precision_score(y, y_pred, zero_division=0)),
        "recall": float(recall_score(y, y_pred, zero_division=0)),
        "f1": float(f1_score(y, y_pred, zero_division=0)),
    }

    # ROC AUC solo si hay probas
    if y_proba is not None:
        metrics["roc_auc"] = float(roc_auc_score(y, y_proba))

        # 5) Curva ROC
        RocCurveDisplay.from_predictions(y, y_proba)
        plt.title("ROC Curve")
        plt.savefig(out_plot)
        plt.close()

    # 6) Guardar métricas
    with open(out_metrics, "w") as f:
        json.dump(metrics, f, indent=2)

    print("Evaluación completada.")
    print(metrics)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--metrics", required=True)
    ap.add_argument("--plot", required=True)
    args = ap.parse_args()

    evaluate(
        model_path=args.model,
        data_path=args.data,
        out_metrics=args.metrics,
        out_plot=args.plot
    )