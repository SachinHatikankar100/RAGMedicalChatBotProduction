from app.common.custom_exception import CustomException
from app.common.logger import get_logger
from app.components.vector_store import load_vector_store
from app.components.llm import load_llm
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

logger = get_logger(__name__)

CUSTOM_PROMPT_TEMPLATE="""

Answer the following medical question in 2-3 lines maximum using only the information provided in the context.

Context:
{context}

Question:
{question}

Answer:

"""


def set_custom_prompt():
    return PromptTemplate(template=CUSTOM_PROMPT_TEMPLATE, input_variables=["context","question"])

def retrieve_qa_chain():
    try:
        db = load_vector_store()
        if db is None:
            raise CustomException("Vector store not found")
        
        llm = load_llm()
        if llm is None:
            raise CustomException("LLM is not found")
        
        qa_chain= RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever = db.as_retriever(search_kwargs={"k":1}),
            return_source_documents = False,
            chain_type_kwargs={'prompt':set_custom_prompt()}

        )
        return qa_chain    
    except Exception as e:
        error_message = CustomException("Failed in qa chain",e)
        logger.error(str(error_message))
        raise error_message

def get_answer(question):
    try:
        retriever = retrieve_qa_chain()
        if retriever is not None:
            response=retriever.invoke({"query":question})
            return response["result"]
        else:
            raise CustomException("QA chain is empty")
        

    except Exception as e:
        error_message = CustomException("Error when getting response from qa chain",e)
        raise error_message

    