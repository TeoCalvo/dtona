import pandas as pd
import sqlalchemy
import os
from sklearn import tree
from sklearn import metrics

# para o jupyter
EP_DIR = os.path.join( os.path.abspath( '.' ), 'src', 'ep04')

EP_DIR = os.path.dirname( os.path.abspath( __file__ ) )
SRC_DIR = os.path.dirname( EP_DIR )
BASE_DIR = os.path.dirname( SRC_DIR )
DATA_DIR = os.path.join( BASE_DIR, 'data' )

def import_query( path, **kwards ):
    with open( path, 'r', **kwards ) as file_open:
        result = file_open.read()
    return result

def connect_db():
    return sqlalchemy.create_engine("sqlite:///" + os.path.join( DATA_DIR, 'olist.db' ) )

query = import_query(os.path.join(EP_DIR, 'create_safra.sql'))
con = connect_db()

# O dado e nosso!!!!
df = pd.read_sql( query, con )
columns = df.columns.tolist()

# Variáveis para serem removidas
to_remove = ['seller_id', 'seller_city']

# Variável alvo, target, resposta
target = 'flag_model'

# Remove de fato as variáveis
for i in to_remove + [target]:
    columns.remove(i)

# Defini tipos de variáveis
cat_features = df[ columns ].dtypes[ df[ columns ].dtypes == 'object'].index.tolist()
num_features = list( set( columns ) - set( cat_features) )

# Treinando o algoritmo de arvore de decisao
clf = tree.DecisionTreeClassifier(max_depth=10)
clf.fit( df[num_features], df[target] )

y_pred = clf.predict( df[num_features] )
y_prob = clf.predict_proba( df[num_features] )

metrics.confusion_matrix( df[target], y_pred )

features_importance = pd.Series( clf.feature_importances_, index=num_features)
features_importance.sort_values( ascending=False )[:20]
