import os
import json
from dotenv import load_dotenv


from langchain.memory import ConversationBufferMemory
from langchain.schema import messages_to_dict
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_openai import ChatOpenAI

# import promt template
from app.utils.chat_templates import chat_template_history_jd


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

def create_jd_history(jd_summary: str, id_jd: str):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    chat_llm_chain_jd = LLMChain(
        llm=llm,
        prompt=chat_template_history_jd,
        verbose=True,
        memory=memory,
    )

    chat_llm_chain_jd({"jd_summary": jd_summary})

    # check if the folder exist
    if not os.path.exists("data/chat_history"):
        os.makedirs("data/chat_history")

    save_json_name = id_jd+"_chat_history.json"
    save_json_path = os.path.join("data/chat_history", save_json_name)

    extracted_messages = chat_llm_chain_jd.memory.chat_memory.messages
    ingest_to_db = messages_to_dict(extracted_messages)

    # SAVE MEMORY
    # with open(save_pkl_path, 'wb') as f:
    #     pickle.dump(memory, f)
    json_history = json.dumps(ingest_to_db)
    with open(save_json_path, 'w') as f:
        f.write(json_history)
