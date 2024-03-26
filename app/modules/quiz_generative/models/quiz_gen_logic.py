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

def question_rag(jobtext: str):
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY, request_timeout=120)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    client = qdrant_client.QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )
    
    doc_store = Qdrant(
        client=client,
        collection_name="rag_documents_test", 
        embeddings=embeddings,
    )

    json_parser = JsonOutputParser()

    prompt = ChatPromptTemplate.from_template("""
    Answer the question based only on the following context:                                
    <context>
    {context}
    </context>
                                                                            
    Generate a 10 quiz suitable for the given job description "{input}". Do not include "All of the above" answers.
    Output format is JSON:
    ("__count__": 10, "data": ( "id": "", "question": "", "choices": [ "A. ", "B. ", "C.", "D. " ], "explanation": "", "answer": "", "level": "", "domain": "" )).
    About level help me three levels: "Fresher, Junior, Senior".
    """)

    document_chain = create_stuff_documents_chain(llm, prompt, output_parser=json_parser)

    retriever = doc_store.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    response = retrieval_chain.invoke({"input": jobtext})

    return response["answer"]