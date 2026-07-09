import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

logging.basicConfig(
    filename = "logs/ingestion_db.log",
    level = logging.DEBUG,
    format="%(asctime)s -%(levelname)s-%(message)s",
    filemode="a"
)

engine = create_engine('sqlite:///inventory.db')

def injectdb(df, table_name , engine):
    df.to_sql(table_name, con = engine, if_exists ='replace', index= False)

def load_raw_data():
    """ THIS FUNCTION WILL LOAD CSVs as dataframes"""
    start = time.time()
    for file in os.listdir('data'):
      if '.csv' in file:
        df = pd.read_csv('data/'+file)
        logging.info(f"ingesting {file} in db")
        injectdb(df, file[:-4], engine)
    end = time.time()
    total_time =(end-start)/60
    logging.info('Ingestion Complete')
    logging.info(f'\nTOTAL TIME: {total_time} minutes')

if __name__ == '__main__' :
     load_raw_data()
