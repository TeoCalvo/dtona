import pandas as pd
import sqlalchemy
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--date", '-d', help='Data para referencia de safra. Formato YYYY-MM-DD', default='2017-04-01')

args = parser.parse_args()
date = args.date

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

query = import_query( os.path.join(EP_DIR, 'query_1.sql' ) )
query = query.format( date=date)

con = connect_db()

try:
    print("\n Tentando deletar...", end="")
    con.execute( "delete from tb_book_sellers where dt_ref = '{date}'".format(date=date) )
    print("ok.")
except:
    print("Tabela não encontrada!")

try:
    print("\n Tentando criar tabela...", end="")
    base_query = 'create table tb_book_sellers as\n {query}'
    con.execute( base_query.format(query=query) )
    print("ok.")

except:
    print("\n Tabela já existente, inserindo dados...", end="")
    base_query = 'insert into tb_book_sellers \n {query}'
    con.execute( base_query.format(query=query) )
    print("ok.\n")