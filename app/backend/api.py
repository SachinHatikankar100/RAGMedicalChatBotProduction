from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from app.common.logger import get_logger
from app.components.retriever import get_answer

logger = get_logger(__name__)

app = FastAPI()

class RequestState(BaseModel):
    question:str
    

@app.post("/medicalchat")
def medicalchat_endpoint(request:RequestState):
    try:
        response = get_answer(
            request.question
            )
        return {"response":response}
    except Exception as e:
        logger.error("Error while getting response from retriever",{str(e)})
        raise HTTPException(
            status_code=500,
            detail="Unable to process your medical question at this time"
        )

