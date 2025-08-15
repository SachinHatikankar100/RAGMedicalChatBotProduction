from langchain_huggingface import HuggingFaceEmbeddings
from app.common.custom_exception import CustomException
from app.common.logger import get_logger
from app.config.config import Config

logger = get_logger(__name__)



def embedding():

    try:
        logger.info("Embedding started")
        model = HuggingFaceEmbeddings(model_name=Config.HFEmbeddings)
        logger.info("Embedding completed")
        return model

    except Exception as e:
        error_message = CustomException("Failed while embedding",e)
        logger.error(str(error_message))
        raise error_message



