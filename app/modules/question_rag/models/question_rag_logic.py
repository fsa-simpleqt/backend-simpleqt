''' 
Input : str of job description
Output : str of quiz
'''

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import Docx2txtLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

import os
from dotenv import load_dotenv

# load the environment variables
load_dotenv()

# Define the google api key
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# JOB_TEXT = "Job Title is Senior Python Software Engineer, Level is Senior, and Brief summary of required skills is 5+ years of professional Python development experience, Expertise in Python and its frameworks."

def question_rag(jobtext):
    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    loader = Docx2txtLoader("data/w3school_data.docx")

    docs = loader.load()

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(docs)
    vector = FAISS.from_documents(documents, embeddings)

    prompt = ChatPromptTemplate.from_template("""Answer the question based only on the following context:                                
    <context>
    {context}
    </context>
                                                                            
    Generate a 10 quiz suitable for the given job description "{input}". Do not include "All of the above" answers.
    Output format is JSON:
    ("count": 10, "data": ( "id": "", "question": "", "choices": [ "A. ", "B. ", "C.", "D. " ], "explanation": "", "answer": "", "level": "", "domain": "" )).
    About level help me three levels: "Fresher, Junior, Senior".
                                            """)

    document_chain = create_stuff_documents_chain(llm, prompt)

    retriever = vector.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    response = retrieval_chain.invoke({"input": jobtext})

    return response["answer"]