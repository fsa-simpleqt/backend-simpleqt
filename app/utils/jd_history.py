import os
import json

from langchain.memory import ConversationBufferMemory
from langchain.schema import messages_to_dict
from langchain.chains import LLMChain

# import promt template
from app.utils.chat_templates import chat_template_history_jd
from app.configs.llm_model import llm

def create_jd_history(jd_summary: str, id_jd: str):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    chat_llm_chain_jd = LLMChain(
        llm=llm,
        prompt=chat_template_history_jd,
        verbose=True,
        memory=memory,
    )

    chat_llm_chain_jd.invoke({"jd_summary": jd_summary})

    # check if the folder exist
    if not os.path.exists("data/chat_history"):
        os.makedirs("data/chat_history")

    save_json_name = id_jd+"_chat_history.json"
    save_json_path = os.path.join("data/chat_history", save_json_name)

    extracted_messages = chat_llm_chain_jd.memory.chat_memory.messages
    ingest_to_db = messages_to_dict(extracted_messages)

    json_history = json.dumps(ingest_to_db)
    with open(save_json_path, 'w') as f:
        f.write(json_history)
