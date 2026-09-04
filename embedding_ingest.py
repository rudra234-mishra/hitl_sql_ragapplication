import requests
from sqlagent_architecture.model import embedding_conn
from logging_config import logger
from sqlagent_architecture.database import database_conn
from sqlagent_architecture.database import release_connection
url="http://127.0.0.1:8000/fetch_data"

insert_query="""
     INSERT INTO "Rudra"."Sql_Script_Embedding" ("Script","Embedding")
     VALUES(%s,%s)
"""
truncate_query="""
     TRUNCATE TABLE "Rudra"."Sql_Script_Embedding"
"""

def truncate_table():
    try:
        conn=database_conn()
        cur=conn.cursor()
        logger.info("truncating table: Rudra.Sql_Script_Embedding")
        cur.execute(query=truncate_query)

        logger.info("truncating table successfully :")
        cur.close()
        conn.commit()
        release_connection(conn)

    except Exception as e:
        logger.error("failed to execute truncate query :%s",e)


def embedding_ingest():
    try:
        conn=database_conn()
        cur=conn.cursor()
        model=embedding_conn()
        logger.info("response getting from url :")
        response=requests.get(url)
        logger.info("response fetch successfully :")
        truncate_table()

        for i in response.json():
            script=i["Script"]
            logger.info("generate embedding vector for script :%s",script)
            vector=model.embed_query(script)
            logger.info("successfully generate :")
            cur.execute(insert_query,(script,vector,))

        conn.commit()
        cur.close()
        logger.info("store embedding successfully in db :")
        release_connection(conn)

    except Exception as e:
        logger.error("embedding ingestion failed :%s",e)


embedding_ingest()