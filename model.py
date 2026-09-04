import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import AzureChatOpenAI,AzureOpenAIEmbeddings
from functools import lru_cache
from logging_config import logger


##llm connection 
@lru_cache(maxsize=1)
def llm_conn():
    try:
        logger.info("connecting to llm model :")
        model=AzureChatOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            model=os.getenv("AZURE_OPENAI_MODEL"),
            api_version=os.getenv("api_version"),
            temperature=0
        )
        logger.info("connection successfull :")
        return model

    except Exception as e:
        logger.error("connection failed :%s",e)


@lru_cache(maxsize=1)
def embedding_conn():
    try:
        logger.info("connecting to embedding model :")
        embed_model=AzureOpenAIEmbeddings(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            api_version=os.getenv("api_version")
        )
        logger.info("connection successfull :")
        return embed_model

    except Exception as e:
        logger.error("connection failed :%s",e)
    