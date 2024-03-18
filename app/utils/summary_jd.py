from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_anthropic import ChatAnthropic

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
# create the prompt template
finnal_jd_chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                """Based on the following job description:
{jobdes}
Play the role of an expert in job description analysis. Carefully analyze candidate requirements and job descriptions. Let's separate them into 2 separate parts
                """
            )
        ),
        HumanMessagePromptTemplate.from_template("{jobdes}"),
    ]
)

def summary_jd(jobdes: str):
    # create the chat message
    chat_message =  finnal_jd_chat_template.format_messages(jobdes=jobdes)
    # create a chain 
    chain =  llm
    result = chain.invoke(chat_message)
    
    return result.content