from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import JsonOutputParser
# from langchain_anthropic import ChatAnthropic

import os
from dotenv import load_dotenv

# load the environment variables
load_dotenv()

# Define the google api key
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
os.environ['CLAUDE_API_KEY'] = os.getenv('CLAUDE_API_KEY')
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY")

# define the parser object
parser = JsonOutputParser()

# setup the gemini pro
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3, convert_system_message_to_human=True, api_key=GOOGLE_API_KEY, request_timeout=120)
# llm = ChatAnthropic(temperature=0, anthropic_api_key=CLAUDE_API_KEY, model_name="claude-3-opus-20240229")
# create the prompt template
finnal_jd_chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                """Return Job title, level(Fresher, Junior, Senior, ...) and Brief summary of required skills about 20 words from the job description. Use the following format: Job Title is {job title}, Level is {level}, and Brief summary of required skills is {brief summary of required skills}."""
            )
        ),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]
)

def jobdes2text(jobdes: str):
    # create the chat message
    chat_message =  finnal_jd_chat_template.format_messages(text=jobdes)
    # create a chain 
    chain =  llm
    result = chain.invoke(chat_message)
    
    return result.content