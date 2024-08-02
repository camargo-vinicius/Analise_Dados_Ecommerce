#%% import das libs necessárias
# !pip install kaggle
import kaggle
from os import listdir 
import pandas as pd
import matplotlib.pyplot as plt

#%%
# listando os datasets disponiveis para download
#!kaggle datasets files -d olistbr/brazilian-ecommerce

# faz o download e o unzip de todos os arquivos na pasta do projeto para ter sempre os arquivos mais atualizados
# !kaggle datasets download olistbr/brazilian-ecommerce --unzip

#%%
# setando pandas pra mostrar todas as colunas dos dfs
pd.set_option('display.max_columns', None)

#%%
def eda_df(df_dict: dict):
    '''Função que recebe um dict de dataframes e percorre 
    mostrando algumas infos do df'''

    for nome_df, df in df_dict.items():
        print(f'\n----------------- {nome_df = } ------------------')

        print(f'(Linhas, cols) = {df.shape}\n')

        print('03 primeiras linhas: \n')
        display(df.head(3))

        print(f'\nColunas: {df.columns}\n')

        print('Tipo e contagem de não nulos das colunas:\n')
        df.info()

        print(f'\nEstatísticas das colunas numéricas:')
        display(df.describe())

        print(f'\nContagem de registros duplicados:\n{df.duplicated().sum()}')

        print(f'\nContagem de valores nulos:\n{df.isnull().sum()}')

#%%
def list_columns(dict_df: dict) -> None:
    '''Função para listar as colunas de cada df'''

    for nome_df, df in dict_df.items():

        print(f'{nome_df = }\n')
        print(f'{df.columns}\n\n')

#%%
def drop_columns(df: pd.DataFrame, lista_colunas: list) -> dict:
    '''Função para receber um dicionario contendo o nome dos dataframes e as colunas que serao excluidas 
    em cada um deles no formato de lista'''

    return df.drop(columns=lista_colunas)

#%%
def drop_nulls(df_original: pd.DataFrame) -> pd.DataFrame | None:
    '''Função que avalia se droppando os nulos quantidade de linhas reduz mais de 5%.
    Se sim, retorna None'''
    
    # faz uma copia do df
    df = df_original.copy()

    qtd_linhas_original = df_original.shape[0] # qtd de linhas antes do drop

    df = df.dropna(subset=['order_approved_at', 
                           'order_delivered_carrier_date', 
                           'order_delivered_customer_date'
                        ]
                )
    
    qtd_linhas_depois = df.shape[0] # qtd de linhas após o drop dos null
    
    proporcao_droppada = round((qtd_linhas_depois / qtd_linhas_original - 1), 2)  

    if proporcao_droppada <= .5:
        print(f'Redução do dataset: {proporcao_droppada * 100}% - OK!')
        return df 
    else:
        print(f'Redução do dataset: {proporcao_droppada * 100}% - NOK!')
        return None

#%%
# listando todos os datasets baixados no diretorio atual (.csv)
arquivos = [arquivo for arquivo in listdir() if arquivo.endswith('.csv')]

# criando um dict de dataframes. 
# arquivo.split('_')[1:-1] serve para pegar todas as palavras que compoe o nome do arquivo exceto as palavras
# "olist" e "dataset" (primeira (i = 0) e última palavra (i = -1)
dict_dfs = {'_'.join(nome_arquivo.split('_')[1:-1]): pd.read_csv(nome_arquivo) for nome_arquivo in arquivos}

#%%
# nao vamos usar geoloc pois os dados de cidade ja estao na base de customer e category_name
del dict_dfs['geolocation']
del dict_dfs['category_name']

#%%
# iterando sobre cada df para fazer uma EDA em cada um deles
eda_df(df_dict=dict_dfs)

#%%
# nome dos dataframes
nome_dfs = list(dict_dfs.keys())
nome_dfs

#%%
# droppando algumas colunas da tabela de produtos
df_products = drop_columns(dict_dfs['products'], ['product_name_lenght', 'product_description_lenght', 'product_photos_qty', 'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm'])

#%%
# armazenando cada df numa variavel
df_order_items = dict_dfs['order_items']
df_order_payms = dict_dfs['order_payments']
df_order_rvw = dict_dfs['order_reviews']

#%%
# checando nulls de orders
dict_dfs['orders'].isnull().sum()

#%%
# droppando as linhas com qualquer registro null de orders
df_orders = drop_nulls(dict_dfs['orders'])

# checando após o drop
df_orders.isnull().sum()

# percorrer todos os dataframes, checando suas colunas com valores nulls e fazer o drop todos 
# de uma vez se possível