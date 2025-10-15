import argparse
import pandas as pd
import os

def main(input_path, out):
    """
    Etapa de preprocesamiento del pipeline Telco Churn (DVC Stage: preprocess).

    - Lee el dataset limpio generado en la etapa anterior (data/processed/telco_churn.csv).
    - Elimina columnas irrelevantes (en particular, 'customer_id').
    - Convierte variables categóricas en numéricas mediante one-hot encoding.
    - Verifica que todas las columnas resultantes sean numéricas.
    - Guarda el dataset preprocesado en la ruta indicada por '--out'.

    Parámetros
    ----------
    input_path : str
        Ruta del archivo CSV procesado de entrada.
    out : str
        Ruta de salida donde se guardará el dataset preprocesado.

    Ejemplo de uso
    --------------
    python src/preprocess_data.py --input data/processed/telco_churn.csv --out data/prepared/telco_churn_prepared.csv
    """
    # Verificación de archivo de entrada
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"No se encontró el archivo de entrada: {input_path}")

    # Lectura del dataset
    df = pd.read_csv(input_path)
    print("✅ Dataset leído correctamente para preprocesamiento.")
    print(f"   Filas y columnas: {df.shape}")

    # Normalización de nombres de columnas
    df.columns = df.columns.str.lower()

    # Eliminación de columnas irrelevantes o identificadores únicos
    id_cols = [c for c in ["customer_id", "customerid", "id"] if c in df.columns]
    df = df.drop(columns=id_cols, errors="ignore")

    # One-hot encoding para variables categóricas
    df = pd.get_dummies(df, drop_first=True)

    # Validación final: asegurar que todas las columnas sean numéricas
    if any(df.dtypes == "object"):
        bad = list(df.columns[df.dtypes == "object"])
        raise TypeError(f"Quedaron columnas no numéricas después del one-hot: {bad}")

    # Crear carpeta de salida si no existe
    os.makedirs(os.path.dirname(out), exist_ok=True)

    # Guardar dataset preprocesado
    df.to_csv(out, index=False)
    print(f"💾 Archivo preprocesado guardado en: {out}")
    print(f"   Filas y columnas finales: {df.shape}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Preprocesamiento del dataset Telco Churn.")
    ap.add_argument("--input", required=True, help="Ruta del archivo de entrada (procesado).")
    ap.add_argument("--out", required=True, help="Ruta de salida del archivo preprocesado.")
    args = ap.parse_args()
    main(args.input, args.out)