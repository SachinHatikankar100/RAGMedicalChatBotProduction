from app.common.custom_exception import CustomException
from app.common.logger import get_logger
import os
from langchain_community.document_loaders import PyPDFLoader,DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config.config import Config
from dotenv import load_dotenv

load_dotenv()
logger = get_logger(__name__)

def load_pdf():
    try:
        if not os.path.exists(Config.data):
            raise CustomException("File path does not exists")
        
        loader = DirectoryLoader(Config.data,glob="*.pdf",loader_cls=PyPDFLoader)
        documents = loader.load()

        if not documents:
            raise CustomException("No documents found")
        
        return documents

    except:
        raise CustomException("Data path not found")


def create_text_chunks(documents):
    try:
        if not documents:
            raise Exception("No documents found")
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.chunk_size, 
            chunk_overlap=Config.chunk_overlap
            )
        text_chunks = text_splitter.split_documents(documents)

        return text_chunks
    except Exception as e:
        raise CustomException("Failed to generate chunks" , e)
        