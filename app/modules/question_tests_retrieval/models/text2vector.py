import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

# load the environment variables
load_dotenv()
# Define the google api key
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY, request_timeout=120)

def text2vector(text: str):
    vector = embeddings.embed_query(text)
    return vector
