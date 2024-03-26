import os
from dotenv import load_dotenv
from app.modules.crud_jds.models.crud_jds import get_jd_summary_by_id
from app.modules.crud_cvs.models.crud_cvs import get_cv_content_by_id, edit_cv
from app.utils.chat_templates import chat_template_cv_matching

from langchain_google_genai import ChatGoogleGenerativeAI
<<<<<<< HEAD
# from langchain_anthropic import ChatAnthropic
# from langchain_openai import OpenAI
=======
>>>>>>> main

# import the json oupput parser from the langchain core
from langchain_core.output_parsers import JsonOutputParser

# define the parser object
parser = JsonOutputParser()

# Import API key
load_dotenv()

# Define the google api key
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.1, convert_system_message_to_human=True, api_key=GOOGLE_API_KEY, request_timeout=120)
chain = llm | parser

# def matching cv and jd return percentage of matching using prompt template
def result_matching_cv_jd(id_cv:str, id_jd:str):
    cv_content = get_cv_content_by_id(id_cv)
    jd_summary = get_jd_summary_by_id(id_jd)
    # create the chat message
    chat_message =  chat_template_cv_matching.format_messages(cv=cv_content, jd=jd_summary)

    matched_result = chain.invoke(chat_message)

    # update matched status and matched_result in database
    edit_cv(id_cv, {"matched_status": True, "matched_result": matched_result})

    return matched_result
