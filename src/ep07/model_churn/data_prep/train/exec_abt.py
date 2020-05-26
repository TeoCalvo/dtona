import os
import sqlalchemy

TRAIN_DIR = os.path.dirname( os.path.abspath(__file__) )
DATA_PREP_DIR = os.path.dirname( TRAIN_DIR )
BASE_DIR = os.path.dirname( DATA_PREP_DIR )

DATA_DIR = os.path.join( os.path.dirname( os.path.dirname( os.path.dirname( BASE_DIR ) ) ), 'data')

engine = sqlalchemy.create_engine( "sqlite:///" + os.path.join(DATA_DIR, 'olist.db'))

with open( os.path.join( TRAIN_DIR, 'criacao_abt.sql' ), 'r' ) as open_file:
    query = open_file.read()

for i in query.split(";")[:-1]:
    engine.execute( i )