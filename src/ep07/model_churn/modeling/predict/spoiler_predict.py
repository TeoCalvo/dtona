import os
import pandas as pd
import sqlalchemy
from sklearn import tree
from sklearn import preprocessing

PRED_DIR = os.path.join( os.path.abspath('.'), 'src', 'ep07', 'model_churn', 'modeling','predict' )
PRED_DIR = os.path.dirname( os.path.abspath(__file__) )
MODELING_DIR = os.path.dirname( PRED_DIR )
BASE_DIR = os.path.dirname( MODELING_DIR )
DATA_DIR = os.path.join( os.path.dirname( os.path.dirname( os.path.dirname( BASE_DIR ) ) ), 'data')
MODEL_DIR = os.path.join( BASE_DIR, 'models')

# Importando dados
engine = sqlalchemy.create_engine( "sqlite:///" + os.path.join(DATA_DIR, 'olist.db'))
query = '''
select *
from tb_book_sellers
where dt_ref = '2018-06-01'
'''
data = pd.read_sql_query( query, engine )

# Importando modelo
model = pd.read_pickle( os.path.join( MODEL_DIR, 'arvore_decisao.pkl' ) )

# Trabalhando a base para encaixar no modelo
df_onehot = pd.DataFrame( model['onehot'].transform( data[ model['cat_features'] ] ),
                          columns=model['onehot'].get_feature_names( model['cat_features'] )  )
df_predict = pd.concat( [data[ model['num_features'] ], df_onehot ], axis=1 )

# Escorando a base
data['score_churn'] = model['model'].predict_proba( df_predict[ model['features_fit'] ] )[:,1]

data_score = data[['dt_ref', 'seller_id','score_churn']]
data_score.to_sql( 'tb_churn_score', engine, if_exists='replace', index=False )