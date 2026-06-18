import polars as pl
import argparse
import os

def join_data(transaction_df, identity_df):
    '''Essa função realiza um join entre os DataFrames de transação e identidade usando a coluna "TransactionID" como chave. O método join() do Polars é utilizado para realizar o join, especificando a coluna de junção, o tipo de junção (left join) e os DataFrames envolvidos. O resultado é um novo DataFrame que contém todas as colunas do DataFrame de transação, juntamente com as colunas correspondentes do DataFrame de identidade, onde os valores de "TransactionID" coincidem. Se não houver correspondência, as colunas do DataFrame de identidade serão preenchidas com valores nulos.
    '''

    return transaction_df.join(identity_df, on="TransactionID", how="left")

if __name__ == "__main__":
    '''Esse é um parser para receber os caminhos dos arquivos de entrada e saída via linha de comando. Com isso você consegue reutilizar o código para diferentes arquivos sem precisar modificar o código-fonte. Basta passar os caminhos corretos ao executar o script.'''

    #As linhas abaixo criam um parser de argumentos usando a biblioteca argparse. Ele define dois argumentos: --input para o caminho do arquivo CSV de entrada e --output para o caminho do arquivo CSV de saída. O parser analisa os argumentos fornecidos na linha de comando e os armazena em args.input e args.output, respectivamente. Isso permite que você especifique os arquivos de entrada e saída ao executar o script, tornando-o mais flexível e reutilizável. A função parse_args() é chamada para processar os argumentos e armazená-los em variáveis para uso posterior no código.
    parser = argparse.ArgumentParser(description="Build data for analysis.")
    parser.add_argument("--input", type=str, help="Path to the input CSV file")
    parser.add_argument("--output", type=str, help="Path to the output CSV file")
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output
    
    # Cria o diretório de saída se ele não existir
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
    except:
        print('O path de saída informado não é um diretório.')
    
    #Verifica se o arquivo de entrada existe. Se não existir, lança um erro FileNotFoundError com uma mensagem indicando que o arquivo de entrada não foi encontrado. Isso é importante para garantir que o script não tente processar um arquivo inexistente, o que causaria erros posteriores.
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    #As linhas abaixo verificam se o caminho do arquivo de entrada contém as palavras 'transaction' ou 'identity'. Dependendo de qual palavra estiver presente, ele define os caminhos para os arquivos de identidade e transação. Se o caminho contiver 'transaction', ele assume que o arquivo de identidade está no mesmo diretório e tem um nome semelhante, substituindo 'transaction' por 'identity'. Se o caminho contiver 'identity', ele faz o oposto. Se nenhum dos casos for atendido, ele lança um ValueError indicando que o caminho de entrada deve conter uma dessas palavras. Isso é importante para garantir que o script possa localizar corretamente os arquivos necessários para o join.

    if 'transaction' in input_path:
        path_identity = input_path.replace('transaction', 'identity')
        path_transaction = input_path
    elif 'identity' in input_path:
        path_transaction = input_path.replace('identity', 'transaction')
        path_identity = input_path
    else:
        raise ValueError("Input path must contain either 'transaction' or 'identity'.")

    if output_path == path_identity or output_path == path_transaction:
        raise ValueError("Output path cannot be the same as input paths.")

    #As linhas abaixo verifica se o arquivo de entrada tem a extensão .csv. Se a extensão for diferente, ele lança um ValueError indicando que o arquivo de entrada deve ter uma extensão .csv. Isso é importante para garantir que o script esteja processando arquivos no formato correto, evitando erros de leitura e processamento posteriores.
    if output_path.split('.')[-1].lower() != 'csv':
        raise ValueError("Output file must have a .csv extension.")

    if input_path.split('.')[-1].lower() != 'csv':
        raise ValueError("Input file must have a .csv extension.")

    #As linhas abaixo leem os arquivos CSV de identidade e transação usando a biblioteca Polars. O método pl.read_csv() é utilizado para carregar os dados dos arquivos CSV em DataFrames do Polars. O DataFrame de identidade é armazenado em identity_df, enquanto o DataFrame de transação é armazenado em transaction_df.
    try:
        identity_df = pl.read_csv(path_identity)
    except Exception as e:
        raise ValueError(f"Error reading CSV file {path_identity}: {e}")

    try:
        transaction_df = pl.read_csv(path_transaction)
    except Exception as e:
        raise ValueError(f"Error reading CSV file {path_transaction}: {e}")

    #As linhas abaixo realizam o join dos DataFrames de transação e identidade.
    full_df = join_data(transaction_df, identity_df)
    full_df.write_csv(output_path)
    