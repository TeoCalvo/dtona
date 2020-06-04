import os
import sqlalchemy
import argparse
from datetime import datetime
from dateutil.relativedelta import relativedelta

parser = argparse.ArgumentParser()
parser.add_argument("--date_init", "-i ",help="Data Ref. Inic. da Safra. (str: YYYY-MM-DD)", type=str)
parser.add_argument("--date_end", "-e", help="Data Ref. Fim da Safra. (str: YYYY-MM-DD)", type=str)
args = parser.parse_args()

EP_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(EP_DIR)
BASE_DIR = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.join(BASE_DIR, 'data')

def import_query(path, **kwards):
    with open(path, 'r', **kwards) as file_open:
        result = file_open.read()
    return result

def connect_db():
    return sqlalchemy.create_engine(
        "sqlite:///" + os.path.join(DATA_DIR, 'olist.db'))

con = connect_db()

# loop que roda o script para cada data na lista
dt_end = datetime.strptime(args.date_end, "%Y-%m-%d")
dt = datetime.strptime(args.date_init, "%Y-%m-%d")

query = import_query(os.path.join(EP_DIR, 'query_1.sql'))

while dt <= dt_end:
    dt = dt.strftime("%Y-%m-%d")

    try:
        #print("\n Tentando resetar {dt}...".format(dt=dt), end="")
        con.execute("delete from tb_book_sellers where dt_ref = '{date}'".format(date=dt))
        #print("ok.")
    except:
        #print("Tabela não encontrada!")
        pass

    try:
        #print("\n Tentando criar tabela...", end="")
        base_query = 'create table tb_book_sellers as\n {query}'
        con.execute(base_query.format(query=query.format(date=dt)))
        #print("ok.")
    except:
        #print("\n Tabela já existente, inserindo dados de {dt}...".format(dt=dt), end="")
        base_query = 'insert into tb_book_sellers \n {query}'
        con.execute(base_query.format(query=query.format(date=dt)))
        #print("ok.\n")

    dt = datetime.strptime( dt, "%Y-%m-%d" ) + relativedelta(months=1)