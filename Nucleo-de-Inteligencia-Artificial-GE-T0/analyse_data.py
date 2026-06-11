import polars as pl
import polars.selectors as cs
import argparse

def analyze_csv(path):
    df = pl.read_csv(path)
    schema = df.schema

    #As linhas abaixo realizam uma análise exploratória dos dados contidos no DataFrame df. O método describe() é utilizado para obter estatísticas descritivas básicas, como contagem, média, desvio padrão, valores mínimos e máximos para as colunas numéricas. O método estimated_size() retorna uma estimativa do tamanho do DataFrame em bytes. O conjunto de tipos de dados presentes no DataFrame é obtido usando set(df.dtypes). Em seguida, as colunas numéricas e de string são identificadas usando os seletores cs.numeric() e cs.string(), respectivamente. Por fim, para cada coluna de string, o número de valores únicos é calculado usando o método n_unique() e impresso na tela.
    #print(df.describe())
    #print(df.estimated_size())
    #print(set(df.dtypes))
    numeric_cols = df.select(cs.numeric()).columns
    cat_cols = [col for col in numeric_cols if (df[col].n_unique() < 50 and df[col].dtype in [pl.Int64, pl.Int32])]
    num_cols = [col for col in numeric_cols if col not in cat_cols]
    string_cols = df.select(cs.string()).columns
    for col in string_cols:
        if df[col].n_unique() < 50:
            cat_cols.append(col)
    str_cols = [col for col in string_cols if col not in cat_cols]
    others = [col for col in df.columns if col not in cat_cols and col not in num_cols and col not in str_cols]
    print(f'Total columns: {len(df.columns)}')
    print(f'Cardinality columns: {len(cat_cols)}')
    print(f'Numerical columns: {len(num_cols)}')
    print(f'String columns: {len(str_cols)}')
    print(f'String columns: {str_cols}')
    print(f'Other columns: {len(others)}')
    print(f'Other columns: {others}')
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze a CSV file using Polars.")
    parser.add_argument("--path", type=str, help="Path to the CSV file")
    args = parser.parse_args()

    path = args.path
    analyze_csv(path)
