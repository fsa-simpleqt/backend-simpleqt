import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

# Import API key
load_dotenv()

# Define the google api key
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# define the openai api key
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0, convert_system_message_to_human=True, api_key=GOOGLE_API_KEY, request_timeout=120)
# llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, request_timeout=120)
