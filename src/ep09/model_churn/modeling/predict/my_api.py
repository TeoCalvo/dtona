import os
import pandas as pd
import sqlalchemy
DBPATH = "/home/teo/Documentos/pessoais/projetos/ensino/projetos_twitch/maratona_ds/data/olist.db"
con = sqlalchemy.create_engine("sqlite:///"+DBPATH)

PREDICT_DIR = os.path.dirname(os.path.abspath(__file__))
MODELING_DIR = os.path.dirname(PREDICT_DIR)
BASE_DIR = os.path.dirname(MODELING_DIR)
MODELS_DIR = os.path.join(BASE_DIR, "models")

model = pd.read_pickle(os.path.join(MODELS_DIR, "model_churn.pkl"))

query_real_time = """SELECT * FROM tb_book_sellers
                    WHERE seller_id = '{seller_id}'
                    AND dt_ref = (SELECT MAX(DT_REF) FROM tb_book_sellers)
                    """

def churn_score(seller_id):
    '''Consome de uma tabela ja escorada'''
    df = pd.read_sql_query(f"SELECT score FROM tb_churn_score WHERE seller_id = '{seller_id}' ", con)
    return df['score'][0]

def churn_real_time(seller_id):
    '''Escora em tempo real'''
    df = pd.read_sql_query( query_real_time.format(seller_id=seller_id) ,con )
    df_onehot = pd.DataFrame( model["onehot"].transform( df[model['cat_features']]),
                                columns=model["onehot"].get_feature_names( model['cat_features'] ) )
    
    df_full = pd.concat( [df[model["num_features"]],df_onehot], axis=1 )
    df_full = df_full[ model['features_fit'] ]
    result = model['model'].predict_proba( df_full )[:,1][0]
    return result