import os
import docx
from dotenv import load_dotenv

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
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# def matching cv and jd return percentage of matching using prompt template
def result_matching_cv_jd(cv_text, jd_text):
    # create the prompt template
    chat_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=(
                    """
                    Given the following CV and JD, calculate the percentage match between the candidate's qualifications and the job requirements:
                    CV: {cv}
                    JD: {jd}
                    To determine the match percentage, analyze the skills and experience in the CV and compare them to the requirements outlined in the JD. Provide the final match percentage as a numeric value between 0-100%, along with a brief explanation of your analysis. Follow this json format: {"Skills Match": {"Required Skills": "","Candidate  Skills": "","Match Percentage": "",}, "Experience Match": {"Required Experience": "","Candidate Experience": "","Match Percentage": "",}, "Overall Match Percentage:": "", "Explanation": ""}
                    """
                )
            ),
            HumanMessagePromptTemplate.from_template(["{cv}", "{jd}"]),
        ]
    )

    # create the chat message
    chat_message =  chat_template.format_messages(cv=cv_text, jd=jd_text)

    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3, convert_system_message_to_human=True, api_key=GOOGLE_API_KEY, request_timeout=120)
    chain = llm | parser
    result = chain.invoke(chat_message)

    return result
