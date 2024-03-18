import os
from dotenv import load_dotenv
from app.modules.crud_jds.models.crud_jds import get_jd_summary_by_id
from app.modules.crud_cvs.models.crud_cvs import get_cv_by_id

# import prompt template
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# import the json oupput parser from the langchain core
from langchain_core.output_parsers import JsonOutputParser

# define the parser object
parser = JsonOutputParser()

# Import API key
load_dotenv()

# Define the google api key
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
os.environ['CLAUDE_API_KEY'] = os.getenv('CLAUDE_API_KEY')
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3, convert_system_message_to_human=True, api_key=GOOGLE_API_KEY, request_timeout=120)
chain = llm | parser

# create the prompt template
chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                """
                Given the following CV and JD, calculate the percentage match between the candidate's qualifications and the job requirements:
                CV: {cv}
                JD: {jd}
                To determine the match percentage, analyze the skills and experience in the CV and compare them to the requirements outlined in the JD. Provide the final match percentage as a numeric value between 0-100%, along with a brief explanation of your analysis. Follow this json format: {"Skills Match": {"Required Skills": "","Candidate Skills": "","Match Percentage": "",}, "Experience Match": {"Required Experience": "","Candidate Experience": "","Match Percentage": "",}, "Overall Match Percentage:": "", "Explanation": ""}
                """
            )
        ),
        HumanMessagePromptTemplate.from_template(["{cv}", "{jd}"]),
    ]
)

# def matching cv and jd return percentage of matching using prompt template
def result_matching_cv_jd(id_cv:str, id_jd:str):
    cv_content = get_cv_by_id(id_cv)
    jd_summary = get_jd_summary_by_id(id_jd)
    # create the chat message
    chat_message =  chat_template.format_messages(cv=cv_content, jd=jd_summary)
    result = chain.invoke(chat_message)

    return result
