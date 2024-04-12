from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from app.utils.chat_templates import chat_template_sumary_jd

import os
from dotenv import load_dotenv

# load the environment variables
load_dotenv()

# Define the google api key
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# define the parser object
parser = JsonOutputParser()

# setup the gemini pro
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3, convert_system_message_to_human=True, api_key=GOOGLE_API_KEY, request_timeout=120)

def summary_jd(jobdes: str):
    # create the chat message
    chat_message =  chat_template_sumary_jd.format_messages(jd=jobdes)
    # create a chain 
    chain =  llm
    result = chain.invoke(chat_message)
    
    return result.content