import pandas as pd
import os
import sqlalchemy

TRAIN_DIR = os.path.join( os.path.abspath('.'), 'src', 'ep05', 'model_churn', 'modeling','train' )
TRAIN_DIR = os.path.dirname( os.path.abspath(__file__) )
MODELING_DIR = os.path.dirname( TRAIN_DIR )
BASE_DIR = os.path.dirname( MODELING_DIR )
DATA_DIR = os.path.join( os.path.dirname( os.path.dirname( os.path.dirname( BASE_DIR ) ) ), 'data')

engine = sqlalchemy.create_engine( "sqlite:///" + os.path.join(DATA_DIR, 'olist.db'))

abt = pd.read_sql_table( 'tb_abt_churn', engine )