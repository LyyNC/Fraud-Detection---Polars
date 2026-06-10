import polars as pl
import argparse
import os

def load_data(path):
    df = pl.read_csv(path)
    return df

def inspect_data(path):
    df = pl.read_csv(path)
    print(df.head())
    print(df.shape)
    print(df.columns)
    print(df.schema)

def join_data(trans, identity):
    joined = trans.join(identity, on="TransactionID", how="inner")
    return joined

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Carrega um dataset para processamento")

    parser.add_argument(
        "--data_path",
        type=str,
        required=True,
        help="Caminho para o arquivo CSV do dataset"
    )

    args = parser.parse_args()

    data_path = args.data_path

    if not os.path.exists(args.data_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {data_path}")

    inspect_data(data_path)
    transactions = load_data(data_path)
    identity_path = data_path.replace("transaction", "identity")
    identity = load_data(identity_path)
    joined_data = join_data(transactions, identity)
    joined_path = data_path.replace("transaction", "full")
    joined_data.write_csv(joined_path)