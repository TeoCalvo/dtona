import os
import json
import pandas as pd
import sqlalchemy
from sklearn import cluster
import seaborn
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn import metrics
from sklearn import preprocessing
from sklearn import ensemble
from yellowbrick.cluster import KElbowVisualizer

TRAIN_DIR = os.path.join( os.path.abspath("."), "segmentacao","train" )
TRAIN_DIR = os.path.dirname( os.path.abspath(__file__) )
SGMT_DIR = os.path.dirname(TRAIN_DIR)
MODELS_DIR = os.path.join(SGMT_DIR, "models")

# Abrindo a conexão com banco de dados
con = sqlalchemy.create_engine( "sqlite:///" + "/home/teo/Documentos/pessoais/projetos/ensino/projetos_twitch/maratona_ds/data/olist.db" )

# Carregando um arquivo em memória
with open(os.path.join(TRAIN_DIR, "get_abt.sql"), "r") as open_file:
    query = open_file.read()

# Importa json com a informação de cada um dos agrupamentos
with open( os.path.join(TRAIN_DIR, "features.json"), "r") as open_file:
    features = json.load( open_file )

df = pd.read_sql(query, con)
#############################
### CLUSTER DE CATEGORIAS ###
#############################
df_prop = pd.DataFrame()
for f in features['categorias']:
    df_prop[ f + "_prop" ] = df[f] / df["qtde_produto"]

model_categorias = cluster.AgglomerativeClustering(n_clusters=10) # Define configuração do algoritmo
model_categorias.fit(df_prop) # Fit ajuste do modelo, passando os dados
df['cluster_id_cat'] = model_categorias.labels_

####################################
## Agrupando das variáveis de RFV ## Recência, Frequência e Valor
####################################
df_rfv = df[features['rfv']]
minmax = preprocessing.MinMaxScaler() # Definindo um normalizador
minmax.fit(df_rfv)                    # Fitando o normalizador
X_rfv = pd.DataFrame( minmax.transform( df_rfv ), # Tranforma o dado
                      columns=features['rfv']) 

model_rfv = cluster.AgglomerativeClustering(n_clusters=9)
model_rfv.fit( X_rfv[features['rfv']] )
df['cluster_id_rfv'] = model_rfv.labels_

###################
## CLUSTER FULL ###
###################
df["cluster_id_full"] = df['cluster_id_cat'].astype(str) + "_" + df['cluster_id_rfv'].astype(str)
print(df[["seller_id", "cluster_id_cat", "cluster_id_rfv", "cluster_id_full"]])

#####################
## Rodando árvore ###
#####################
clf = ensemble.RandomForestClassifier( n_estimators=500,
                                       min_samples_split=30,
                                       random_state=1992)

clf.fit(df[ features['categorias'] + features['rfv']], df['cluster_id_full'])
metrics.accuracy_score( df['cluster_id_full'], clf.predict(df[ features['categorias'] + features['rfv']]) )

model = pd.Series( {
    "model":clf,
    "features":features["categorias"] + features["rfv"] }
)

model.to_pickle( os.path.join(MODELS_DIR, 'model.pkl') )