from sklearn import tree
import pandas as pd
import sqlalchemy
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--date", help="Data referencia para escorar safra")
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
df = pd.read_sql_query(f"SELECT * FROM tb_book_sellers WHERE dt_ref='{args.date}' ", con)
print("ok")

print("Realizando a clusterização...", end="")
df["cluster_id"] = model['model'].predict( df[model['features']] )
print("ok.")

print("Enviando base clusterizada para o banco de dados...", end="")
df[ ["dt_ref","seller_id", "cluster_id"] ].to_sql( "tb_cluster", con, index=False )
print("ok.")