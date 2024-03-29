import os
import json

from dotenv import load_dotenv
from app.modules.crud_jds.models.crud_jds import get_jd_summary_by_id
from app.modules.crud_cvs.models.crud_cvs import get_cv_content_by_id, edit_cv
from app.utils.chat_templates import chat_template_cv_matching

from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.memory.chat_message_histories.in_memory import ChatMessageHistory
from langchain_core.output_parsers import JsonOutputParser
from langchain.schema import messages_from_dict
parser = JsonOutputParser()

# import promt template
from app.utils.chat_templates import chat_template_cv_matching

# Import API key
load_dotenv()

# Define the google api key
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0, convert_system_message_to_human=True, api_key=GOOGLE_API_KEY, request_timeout=120)
# llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, request_timeout=120)

def load_history_and_matching(cv_need_matching: str, id_jd: str):
    save_json_name = id_jd + "_chat_history.json"
    save_json_path = os.path.join("data/chat_history", save_json_name)

    with open(save_json_path, 'r') as f:
        retrieve_from_db = json.load(f)

    retrieved_messages = messages_from_dict(retrieve_from_db)
    retrieved_chat_history = ChatMessageHistory(messages=retrieved_messages)

    retrieved_memory = ConversationBufferMemory(chat_memory=retrieved_chat_history, memory_key="chat_history", return_messages=True)
    chat_llm_chain_matchcv = LLMChain(
        llm=llm,
        prompt=chat_template_cv_matching,
        verbose=True,
        memory=retrieved_memory,
        output_parser=parser)

    matched_result = chat_llm_chain_matchcv({"cv": cv_need_matching})

    return matched_result

# def matching cv and jd return percentage of matching using prompt template
def result_matching_cv_jd(id_cv:str, id_jd:str):
    cv_content = get_cv_content_by_id(id_cv)
    
    # Result matching cv and jd
    matched_result = load_history_and_matching(cv_need_matching=cv_content, id_jd=id_jd)

    # update matched status and matched_result in database
    # edit_cv(id_cv, {"matched_status": True, "matched_result": matched_result})

    return matched_result
