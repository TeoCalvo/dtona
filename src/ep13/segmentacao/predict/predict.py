from sklearn import tree
import pandas as pd
import sqlalchemy
import os
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--date", help="Data referencia para escorar safra")
parser.add_argument("-k", help="Número de clusters para fazer a propensão")
args = parser.parse_args()

PREDICT_DIR = os.path.join( os.path.abspath("."), "segmentacao","predict")
PREDICT_DIR = os.path.dirname( os.path.abspath(__file__) )
SGMT_DIR = os.path.dirname(PREDICT_DIR)
MODELS_DIR = os.path.join(SGMT_DIR, "models")

print("Importando o modelo...", end="")
model = pd.read_pickle( os.path.join(MODELS_DIR, "model.pkl") )
print("ok.")

print("Importando base para ser clusterizada...", end="")
con = sqlalchemy.create_engine( "sqlite:///" + "/home/teo/Documentos/pessoais/projetos/ensino/projetos_twitch/maratona_ds/data/olist.db" )
df = pd.read_sql_query(f"SELECT * FROM tb_book_sellers WHERE dt_ref='2018-09-01' ", con)
print("ok")

print("Realizando a clusterização...", end="")
probs = model['model'].predict_proba( df[model['features']] )
print("ok.")

print("Enviando base clusterizada para o banco de dados...", end="")
df[ ["dt_ref","seller_id", "cluster_id"] ].to_sql( "tb_cluster", con, index=False )
print("ok.")

def make_order(probs, classes, k=5 ):
    list_probs = list(zip( probs, classes ))
    list_probs.sort(key=lambda x: x[0], reverse=True)
    return [ i[-1] for i in list_probs[:k]]

""" np.apply_along_axis( func1d=make_order,
                     axis=1,
                     arr=probs.tolist(),
                     classes=model['model'].classes_.tolist(),
                     k=5 ) """

result = pd.DataFrame( [make_order(i, model['model'].classes_.tolist(), k=args.k) for i in probs],
                        columns= ["rank_cluster_" + str(i) for i in range(1, args.k+1)] )

result['seller_id'] = df['seller_id']
result['dt_ref'] = df['dt_ref']

result.to_sql( "tb_cluster", con, index=False, if_exists="replace" )