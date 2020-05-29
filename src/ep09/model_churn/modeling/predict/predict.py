import os
import pandas as pd
import sqlalchemy
import argparse
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--dt_ref", help="Data referencia para safra a ser predita: YYYY-MM-DD")
args = parser.parse_args()

PREDICT_DIR = os.path.dirname(os.path.abspath(__file__))
MODELING_DIR = os.path.dirname(PREDICT_DIR)
BASE_DIR = os.path.dirname(MODELING_DIR)
MODELS_DIR = os.path.join(BASE_DIR, "models")
DBPATH = "/home/teo/Documentos/pessoais/projetos/ensino/projetos_twitch/maratona_ds/data/olist.db"

print("Importando modelo...", end="")
model = pd.read_pickle(os.path.join(MODELS_DIR, "model_churn.pkl"))
print("ok.")

print("Abrindo conexão com banco de dados...", end="")
con = sqlalchemy.create_engine("sqlite:///" + DBPATH)
print("ok.")

print("Importando dados...", end="")
df = pd.read_sql_query( f"SELECT * FROM tb_book_sellers WHERE dt_ref='{args.dt_ref}';",
                        con )
print("ok.")

print("Preparando dados para aplicar modelo...", end="")
df_onehot = pd.DataFrame( model['onehot'].transform(df[model['cat_features']]),
                          columns=model['onehot'].get_feature_names(model['cat_features']) )

df_full = pd.concat( [ df[model['num_features']], df_onehot], axis=1 )
df_full = df_full[model['features_fit']]
print("ok.")

print("Criando score...", end="")
df['score'] = model['model'].predict_proba(df_full)[:,1]
print("ok.")

print("Enviando os dados para o banco de dados...", end="")
df_score = df[["dt_ref","seller_id", "score"]].copy()
df_score["dt_atualizacao"] = datetime.datetime.now()
df_score.to_sql( "tb_churn_score", con, if_exists='replace', index=False )
print("ok.")