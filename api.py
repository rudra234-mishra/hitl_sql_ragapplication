from fastapi import FastAPI,HTTPException
import pandas as pd
from logging_config import logger
from sqlagent_architecture.database import database_conn,release_connection
import subprocess
import sys

app=FastAPI(title="Api Endpoint :")

file = "sqlagent_architecture.embedding_ingest"
python = "python"


@app.get('/run')
def run_embedding():
    result=subprocess.run([python,"-m",file])

    if result.returncode !=0:
        return HTTPException(status_code=500,
                            detail="embedding_ingest.py failed")

    else:
        return "successfully run program :"


@app.get('/')
def home():
    return {"Status":"Ok"}


@app.get('/fetch_data')
def fetch_data():

    conn=database_conn()
    query="""
         SELECT * FROM "Rudra"."Sql_Script" """
    try:
        logger.info("fetching data from database :")
        data=pd.read_sql_query(sql=query,
                               con=conn)
        if data.empty:
            logger.info("no records found :")

        else:
            logger.info("data retrive successfully :")
            release_connection(conn)
            result=data.to_dict(orient="records")
            return result

    except Exception as e:
        logger.error("select query failed :%s",e)
        raise HTTPException(status_code=400,
                            detail="failed :")

    
