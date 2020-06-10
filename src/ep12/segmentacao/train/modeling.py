import os
import pandas as pd
import sqlalchemy
from sklearn import cluster
import seaborn
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn import preprocessing
from yellowbrick.cluster import KElbowVisualizer

TRAIN_DIR = os.path.join( os.path.abspath("."), "segmentacao","train" )
TRAIN_DIR = os.path.dirname( os.path.abspath(__file__) )
SGMT_DIR = os.path.dirname(TRAIN_DIR)

# Abrindo a conexão com banco de dados
con = sqlalchemy.create_engine( "sqlite:///" + "/home/teo/Documentos/pessoais/projetos/ensino/projetos_twitch/maratona_ds/data/olist.db" )

# Carregando um arquivo em memória
with open(os.path.join(TRAIN_DIR, "get_abt.sql"), "r") as open_file:
    query = open_file.read()

df = pd.read_sql( query, con )

columns = df.columns.tolist()
for i in columns:
    print(i)

#############################
### CLUSTER DE CATEGORIAS ###
#############################
categorias = ["qtde_cama_mesa_banho",
              "qtde_beleza_saude",
              "qtde_esporte_lazer",
              "qtde_moveis_decoracao",
              "qtde_informatica_acessorios",
              "qtde_utilidades_domesticas",
              "qtde_relogios_presentes",
              "qtde_telefonia",
              "qtde_ferramentas_jardim",
              "qtde_automotivo",
              "qtde_brinquedos",
              "qtde_cool_stuff",
              "qtde_perfumaria",
              "qtde_bebes",
              "qtde_eletronicos",
              "qtde_papelaria",
              "qtde_fashion_bolsas_e_acessorios",
              "qtde_pet_shop",
              "qtde_moveis_escritorio",
              "qtde_consoles_games",
              "qtde_malas_acessorios",
              "qtde_construcao_ferramentas_construcao",
              "qtde_eletrodomesticos",
              "qtde_instrumentos_musicais",
              "qtde_eletroportateis",
              "qtde_casa_construcao",
              "qtde_livros_interesse_geral",
              "qtde_alimentos",
              "qtde_moveis_sala",
              "qtde_casa_conforto",
              "qtde_bebidas",
              "qtde_audio",
              "qtde_market_place",
              "qtde_construcao_ferramentas_iluminacao",
              "qtde_climatizacao",
              "qtde_moveis_cozinha_area_de_servico_jantar_e_jardim",
              "qtde_alimentos_bebidas",
              "qtde_industria_comercio_e_negocios",
              "qtde_livros_tecnicos",
              "qtde_telefonia_fixa",
              "qtde_fashion_calcados",
              "qtde_eletrodomesticos_2",
              "qtde_construcao_ferramentas_jardim",
              "qtde_agro_industria_e_comercio",
              "qtde_artes",
              "qtde_pcs",
              "qtde_sinalizacao_e_seguranca",
              "qtde_construcao_ferramentas_seguranca",
              "qtde_artigos_de_natal" ]

df_prop = pd.DataFrame()
for f in categorias:
    df_prop[ f + "_prop" ] = df[f] / df["qtde_produto"]

features = df_prop.columns.tolist() # lista das variáveis que serão usadas no modelo
model = cluster.AgglomerativeClustering(n_clusters=10) # Define configuração do algoritmo
model.fit(df_prop) # Fit ajuste do modelo, passando os dados
df_prop['cluster_id'] = model.labels_
df['cluster_id_cat'] = model.labels_

clf = tree.DecisionTreeClassifier() # Algoritmo de arvore
clf.fit( df_prop[ df_prop.columns.tolist()[:-1] ], df_prop['cluster_id'] )  # Fit arvore

features_importance = pd.Series( clf.feature_importances_, index=df_prop.columns.tolist()[:-1] ) # Pega a importancia das variáveis e ordena
features_importance = features_importance.sort_values(ascending=False)

seaborn.heatmap(df_prop.groupby("cluster_id")[features_importance.index[:10]].mean())
plt.show()

# Método de Elbow
"""
model = cluster.AgglomerativeClustering()
visualizer = KElbowVisualizer(model, k=(5,20))
visualizer.fit(df_prop[features])
visualizer.show() """

####################################
## Agrupando das variáveis de RFV ## Recência, Frequência e Valor
####################################

features_rfv = ["avg_review_score",
                "idade_base_dias",
                "qtde_dias_utl_venda",
                "prop_ativacao",
                "qtde_vendas",
                "qtde_produto",
                "qtde_produto_dst",
                 ]

df_rfv = df[features_rfv]

minmax = preprocessing.MinMaxScaler() # Definindo um normalizador
minmax.fit(df_rfv) # Fitando o normalizador
X_rfv = pd.DataFrame( minmax.transform( df_rfv ), # Tranforma o dado
                      columns=features_rfv ) 

model_rfv = cluster.AgglomerativeClustering(n_clusters=9)
model_rfv.fit( X_rfv[features_rfv] )

X_rfv['cluster_id'] = model_rfv.labels_
df['cluster_id_rfv'] = model_rfv.labels_

seaborn.heatmap(X_rfv.groupby("cluster_id").mean(),cmap="YlGnBu")
plt.show()

"""visualizer = KElbowVisualizer(model_rfv, k=(5,20))
visualizer.fit(X_rfv)
visualizer.show()"""