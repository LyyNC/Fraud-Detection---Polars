# TUTORIAL PARA INICIAR OS SEUS ESTUDOS

## Instalar o Python:

### Passo a passo para Windows:
Download disponível em: [PYTHON3](https://www.python.org/downloads/)<br>
Baixe o instalador mais recente do python<br>
Execute o instalador e marque a opção: Add Python to PATH<br>

### Passo a passo para Linux:
```bash
sudo apt update
sudo apt install python3 python3-pip -y
```

## Instalar o kaggle, kagglehub, polars
Depois de instalar o python é só rodar: `pip install -r requirements.txt`

## Fazer autenticação no Kaggle
Dataset disponível em: [IEEE Fraud Detection](https://www.kaggle.com/competitions/ieee-fraud-detection/data)<br>
Crie sua conta, é possível também logar com a sua conta Google.<br>
Autenticação é feita via número de celular, não vai funcionar se não fizer.<br>
A inscrição na competição é necessária para ter acesso aos dados, na aba dados vai aparecer um botão indicando que você se inscreva, é só clicar nele.

## Criar um API Token de autenticação
No site, vá em configurações, novo API Token e crie o seu próprio, guarde o bem porque só vai ser possível ver uma vez, copie o comando similar ao abaixo que aparecer nessa hora.<br>
`mkdir -p ~/.kaggle && echo SEU_API_TOKEN > ~/.kaggle/access_token && chmod 600 ~/.kaggle/access_token`<br>
Rodar o comando copiado, para vincular o seu token a sua máquina.

## Baixar a base: 
`kaggle competitions download -c ieee-fraud-detection`

## Extrair a base: 
`unzip ieee-fraud-detection.zip`

## Carregar os datasets e começar a inspecionar os dados
O código base está em `view_data.py`<br>
Para rodar o comando é: `python3 view_data.py --data_path=path_do_dataset

##  Fazer os joinds das bases de dados
O código para fazer o join está em `build_data.py`<br>
Para executar o comando é: `python3 build_data.py --input=path_do_dataset --output=path_onde_deve_ser_salvo_o_joined`<br>
O script aceita tanto o transaction como o identity como input e lida internamente para fazer o join.
Tanto o input quanto o output precisa conter a extensão .csv para ser salvo, o código não tem suporte para outras extensões.