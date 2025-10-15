import argparse
import pandas as pd
import os

def main(out):
    """
    Etapa inicial del pipeline Telco Churn (DVC Stage: make_data).

    - Carga el dataset original desde 'data/raw/telco_churn.csv'.
    - Verifica su existencia antes de leerlo.
    - Muestra información básica (dimensiones y columnas).
    - Crea la carpeta de salida si no existe.
    - Guarda una copia sin modificaciones en la ruta indicada por '--out'.

    Parámetros
    ----------
    out : str
        Ruta de salida donde se guardará el archivo CSV procesado.

    Ejemplo de uso
    --------------
    python src/make_data.py --out data/processed/telco_churn.csv
    """
    data_path = "data/raw/telco_churn.csv"

    # Verifica que el archivo exista antes de leerlo
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"No se encontró el archivo en la ruta esperada: {data_path}")

    # Carga el dataset
    df = pd.read_csv(data_path)
    print("✅ Dataset cargado correctamente.")
    print(f"   Filas y columnas: {df.shape}")
    print(f"   Columnas: {list(df.columns)}")

    # Crea la carpeta destino si no existe (por ejemplo: data/processed)
    os.makedirs(os.path.dirname(out), exist_ok=True)

    # Guarda el dataset en la ruta especificada por DVC (--out)
    df.to_csv(out, index=False)
    print(f"💾 Archivo guardado en: {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Carga y guarda el dataset Telco Churn.")
    ap.add_argument("--out", required=True, help="Ruta de salida del archivo procesado.")
    args = ap.parse_args()
    main(args.out)