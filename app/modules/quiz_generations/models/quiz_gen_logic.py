from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.output_parsers import JsonOutputParser

from langchain_community.vectorstores import Qdrant
import qdrant_client

import os
from dotenv import load_dotenv

# load the environment variables
load_dotenv()

# Define the google api key
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
os.environ['QDRANT_API_KEY'] = os.getenv('QDRANT_API_KEY')
os.environ['QDRANT_URL'] = os.getenv('QDRANT_URL')

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")
QDRANT_URL = os.environ.get("QDRANT_URL")

def generate_question(jobtext: str):
    pass