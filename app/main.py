import threading
import subprocess
import time
from app.common.custom_exception import CustomException
from app.common.logger import get_logger
from dotenv import load_dotenv

load_dotenv()

logger = get_logger(__name__)

def run_backend():
    try:
        logger.info("Starting backend...")
        subprocess.run(["uvicorn","app.backend.api:app","--host","127.0.0.1","--port","9999"],check=True) 
        # Subprocess runs the backend process

    except CustomException as e:
        logger.error("Error in backend")
        raise Exception(CustomException("Error in backend",{str(e)}))

def run_frontend():
    try:
        logger.info("Starting frontend...")
        subprocess.run(["python","app/frontend/ui.py"],check=True)
        # Subprocess runs the frontend process
    except CustomException as e:
        logger.error("Error in backend")
        raise Exception(CustomException("Error in backend",{str(e)}))

if __name__ == "__main__":
    try:
        threading.Thread(target=run_backend).start()
        #backend should start first
        time.sleep(2)
        # sleep helps for backend to get ready
        run_frontend()
        # now when the front end runs there should be no error as backend is ready to serve the request
    except CustomException as e:
        logger.error("Error while processing your request")
        raise Exception (str(CustomException("Failed to process your requests",details=e)))
    
    