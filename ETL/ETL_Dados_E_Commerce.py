#%% import das libs necessárias
# !pip install kaggle
import kaggle
from os import listdir 
import pandas as pd

#%%
# listando os datasets disponiveis para download
#!kaggle datasets files -d olistbr/brazilian-ecommerce

# faz o download e o unzip de todos os arquivos na pasta do projeto
# !kaggle datasets download olistbr/brazilian-ecommerce --unzip

#%%

def eda_df(df_dict: dict):
    '''Função que recebe um dict de dataframes e percorre 
    mostrando algumas infos do df'''

    for nome_df, df in df_dict.items():
        print(f'\n----------------- {nome_df = } ------------------')

        print(f'(Linhas, cols) = {df.shape}\n')

        print('05 primeiras linhas: \n')
        display(df.head())

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
def drop_columns(dict_dataframes: dict) -> dict:
    '''Função para receber um dicionario contendo
    o nome dos dataframes e as colunas que serao excluidas 
    em cada um deles no formato de lista'''

    pass

#%%

# listando todos os datasets baixados no diretorio atual (.csv)
arquivos = [arquivo for arquivo in listdir() if arquivo.endswith('.csv')]

# criando um dict de dataframes. 
# arquivo.split('_')[1:-1] serve para pegar todas as palavras que compoe o nome do arquivo exceto as palavras
# "olist" e "dataset" (primeira (i = 0) e última palavra (i = -1)
dict_dfs = {'_'.join(nome_arquivo.split('_')[1:-1]): pd.read_csv(nome_arquivo) for nome_arquivo in arquivos}
dict_dfs

# nao vamos usar geoloc pois os dados de cidade ja estao na base de customer
del dict_dfs['geolocation']

#%%
# iterando sobre cada df para fazer uma EDA em cada um deles
eda_df(df_dict=dict_dfs)

#%%
# nome dos dataframes
nome_dfs = list(dict_dfs.keys())
nome_dfs
#%%
# lista as colunas existentes no df
list_columns(dict_dfs)
#%%
# lista de colunas para droppar em cada df
dict_drop_columns = {
                    'customers': ['customer_unique_id'],
                    'order_payments': ['payment_sequential', 'payment_installments']

}

#%%
#%%
df_customer = dict_dfs['customers']
df_customer.head()
#%%

# df_customer.query('customer_id != customer_unique_id')

#%%
df_orders = dict_dfs['orders']
condicao = df_orders['order_delivered_customer_date'].isnull()
df_orders[condicao]

# #%%
# # merge
# df_merge = df_orders.merge(right=df_customer, how='inner', on='customer_id')

#%%

df_items = dict_dfs['order_items']
condicao = df_items['order_id'].duplicated()

df_items[condicao]

#%%
df_items.query("order_id == '683bf306149bb869980b68d48a1bd6ab'")

#%%
df_payment = dict_dfs['order_payments']
condicao = df_payment['order_id'].duplicated()
df_payment.query("order_id == '683bf306149bb869980b68d48a1bd6ab'")