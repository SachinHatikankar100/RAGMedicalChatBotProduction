from app.components.pdf_loader import load_pdf, create_text_chunks
from app.components.vector_store import save_vector_store
from app.common.custom_exception import CustomException
from app.common.logger import get_logger

logger = get_logger(__name__)

def load_and_process_documents():
    try:
        logger.info("Making the vectorstore....")
        documents = load_pdf()
        text_chunks = create_text_chunks(documents)
        save_vector_store(text_chunks)
        logger.info("Vectorstore created successfully...")

    except Exception as e:
        error_message = CustomException("Failed while loading and processing documents",e)
        logger.error(str(error_message))

if __name__ == "__main__":
    load_and_process_documents()