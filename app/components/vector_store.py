from app.components.pdf_loader import create_text_chunks, load_pdf
from app.common.custom_exception import CustomException
from app.common.logger import get_logger
from app.components.embedding import embedding
from langchain_community.vectorstores import FAISS
from app.config.config import Config
import os

logger = get_logger(__name__)

def load_vector_store():
    try:
        
        if os.path.exists(Config.vector_database):
            hfembedding = embedding()
            return FAISS.load_local(
                Config.vector_database,
                hfembedding,
                allow_dangerous_deserialization=True
            )
        else:
            logger.error("No vectore store found...")
    except Exception as e:
        raise CustomException("loading vector failed")


def save_vector_store(text_chunks):
    try:
        if not text_chunks:
            raise Exception("No chunks found")
        
        hfembedding = embedding()
        db = FAISS.from_documents(text_chunks,hfembedding)

        db.save_local(Config.vector_database)

        return db

    except Exception as e:
        raise CustomException("saving vector failed")
    

