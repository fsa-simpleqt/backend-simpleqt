import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Define the google api key
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

def text2vector(text):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
    vector = embeddings.embed_query(text)
    return vector
