from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain_community.vectorstores import Qdrant
import qdrant_client

from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools.tavily_search import TavilySearchResults

from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field
import json
from langchain_core.agents import AgentActionMessageLog, AgentFinish

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, PromptTemplate, HumanMessagePromptTemplate
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents import AgentExecutor

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import ConfigurableFieldSpec

from langchain_core.output_parsers import JsonOutputParser
parser_res = JsonOutputParser()

import os
from dotenv import load_dotenv

# load the environment variables
load_dotenv()

# Define the google api key
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
os.environ['QDRANT_API_KEY'] = os.getenv('QDRANT_API_KEY')
os.environ['QDRANT_URL'] = os.getenv('QDRANT_URL')
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['TAVILY_API_KEY'] = os.getenv('TAVILY_API_KEY')

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")
QDRANT_URL = os.environ.get("QDRANT_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Retrieve tool
client = qdrant_client.QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

doc_store = Qdrant(
    client=client,
    collection_name="langchain_knowledge_base", 
    embeddings=embeddings,
)

retriever = doc_store.as_retriever()
retriever_tool = create_retriever_tool(
    retriever,
    "langchain_search",
    "Search for information about LangChain. For any questions about LangChain, you must use this tool!",
)

# Tavily Tool
search = TavilySearchResults(max_results=3)

# Response schema
class Quiz_Gen_Response(BaseModel):
    """Parsing quiz. Output format is JSON only."""
    output: str = Field(
        description='The generated quiz in JSON format: {"count":10,"data":[{"id":int,"question":str,"choices":["A.","B.","C.","D."],"explanation":str,"answer":str,"level":str[Fresher,Junior,Senior],"domain":str}]}'
)

# Custom parsing logic
def parse(output):
    # If no function was invoked, return to user
    if "function_call" not in output.additional_kwargs:
        return AgentFinish(return_values={"output": output.content}, log=output.content)

    # Parse out the function call
    function_call = output.additional_kwargs["function_call"]
    name = function_call["name"]
    inputs = json.loads(function_call["arguments"])

    # If the RAG_Response function was invoked, return to the user with the function inputs
    if name == "Quiz_Gen_Response":
        return AgentFinish(return_values=inputs, log=str(function_call))
    # Otherwise, return an agent action
    else:
        return AgentActionMessageLog(
            tool=name, tool_input=inputs, log="", message_log=[output]
        )

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], template='You are a helpful assistant')),
        MessagesPlaceholder(variable_name='chat_history'),
        HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['input'], template='{input}')),
        MessagesPlaceholder(variable_name='agent_scratchpad')
    ]
)
tools = []
llm_with_tools = llm.bind_functions([Quiz_Gen_Response])
agent = (
    {
        "input": lambda x: x["input"],
        # Format agent scratchpad from intermediate steps
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
        "chat_history": lambda x: x["chat_history"],
    }
    | prompt
    | llm_with_tools
    | parse
)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

store = {}
def get_session_history(user_id: str, conversation_id: str) -> BaseChatMessageHistory:
    if (user_id, conversation_id) not in store:
        store[(user_id, conversation_id)] = ChatMessageHistory()
    return store[(user_id, conversation_id)]

with_message_history = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    history_factory_config=[
        ConfigurableFieldSpec(
            id="user_id",
            annotation=str,
            name="User ID",
            description="Unique identifier for the user.",
            default="",
            is_shared=True,
        ),
        ConfigurableFieldSpec(
            id="conversation_id",
            annotation=str,
            name="Conversation ID",
            description="Unique identifier for the conversation.",
            default="",
            is_shared=True,
        ),
    ],
)

def is_valid_json(json_string):
    valid_json = json.loads(json_string)
    return valid_json

def generate_question(jobtext: str):
    store.clear()
    keyword_res = with_message_history.invoke(
        {"input": f"What are the technical keywords mentioned in this job description and level of JD need (Fresher, Junior, Senior): {jobtext}"},
        config={"configurable": {"user_id": "quangdinh", "conversation_id": "abc123"}},
    )
    response = with_message_history.invoke(
        {"input": f"""YOUR TASK is CREATE a 10 QUESTIONS based on the keywords technical skills below:
         {keyword_res["output"]}"""},
        config={"configurable": {"user_id": "quangdinh", "conversation_id": "abc123"}},
    )
    llm_res_json = parser_res.parse(response["output"])
    print(type(response["output"]))
    print(type(llm_res_json))
    return llm_res_json