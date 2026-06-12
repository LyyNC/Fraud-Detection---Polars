# - # - # - # - # -
#Etapa 1º Leitura e Schema
# - # - # - # - # -

import polars as pl
import numpy as np

#Carregando os DataSet 'train_transaction' e 'train_identity' utilizando o pl.read_csv
train_transaction = pl.read_csv("Fraud Detection/train_transaction.csv")
train_identity = pl.read_csv("Fraud Detection/train_identity.csv")

#Printando as 5 primeiras linhas de cada dataframe utilizando o .head()
print(train_transaction.head())
print(train_identity.head())

#Coletando os Schema dos dois DataSet
schema_transaction = train_transaction.schema
schema_identity = train_identity.schema

#Contando quantidade de colunas numéricas e categoricas do 'train_transaction' utilizando o loop (for) 
numeric_transaction = sum(dtype.is_numeric() for dtype in schema_transaction.values())
catg_transaciton = len(schema_transaction) - numeric_transaction

#contando quantidade de colunas numéricas e categóricas do 'train_identity' utilizando o loop (for) 
numeric_identity = sum(dtype.is_numeric() for dtype in schema_identity.values())
catg_identity = len(schema_identity) - numeric_identity

print(f"Quantidade de Colunas Numéricas Transaction: {numeric_transaction}\nQuantidade de Colunas Categóricas Transaction: {catg_transaciton}")
print(f'Quantidade de Colunas Númericas Identity: {numeric_identity}\nQuantidade de Colunas Categóricas Identity: {catg_identity}')

# - # - # - # - # -
#Etapa 2º Join de DataSets
# - # - # - # - # -

#Realizando o Join pela coluna 'Transaction ID'(juntando dois dataframe em apenas 1), nomeado de df
df = train_transaction.join(train_identity, on="TransactionID")

print(df.head())

#Verificando se há algum nulo na coluna TransactionID
print(df["TransactionID"].null_count())

# - # - # - # - # -
#Etapa 3º Seleção de colunas relevantes
# - # - # - # - # -

#Separando as colunas relevantes para ter apenas um dataframe com as devidas colunas relevantes utilizando o .selec
col_relevantes = ["TransactionDT", "TransactionAmt", "ProductCD", "card1", "DeviceType", "isFraud"]
df_relevantes = df.select(pl.col(col_relevantes))
print(df_relevantes.head())

# - # - # - # - # -
#Etapa 4º Filtragem de fraudes
# - # - # - # - # -

#Filtrando os casos de fraudes (Fraudes = 1/ Não Fraude = 0) utilizando o .filter 
qnt_fraude = df_relevantes.filter(
    (pl.col("isFraud") == 1)).height

print(f"Quantidade de Fraudes identificadas: {qnt_fraude}")
#Calculando a proporção de casos de fraudes. 
total_trans = df_relevantes["isFraud"].len()
proporc_fraude = (qnt_fraude / total_trans) * 100
print(f"Proporção de casos identificado como Fraude é de {proporc_fraude}%")

isfraud = df_relevantes.filter(
    (pl.col("isFraud") == 1))


produto = (
    df_relevantes.group_by("ProductCD")
    .agg(pl.col("TransactionAmt").mean().alias("Média TransactionAmt"),
         pl.col("isFraud").mean()))

print(produto)