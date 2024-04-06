import os
import json

from dotenv import load_dotenv
from app.modules.crud_jds.models.crud_jds import get_jd_summary_by_id
from app.modules.crud_cvs.models.crud_cvs import get_cv_content_by_id, edit_cv
from app.utils.chat_templates import chat_template_cv_matching, input_data_cv_matching
from app.configs.llm_model import llm
from app.utils.jd_history import create_jd_history

from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.memory.chat_message_histories.in_memory import ChatMessageHistory
from langchain_core.output_parsers import JsonOutputParser
from langchain.schema import messages_from_dict
parser = JsonOutputParser()

def change_llm(jd_summary, id_jd):
    # delete json file
    os.remove(f"data/chat_history/{id_jd}_chat_history.json")
    # create new json file
    create_jd_history(jd_summary, id_jd)

def calculate_matching_score(result):
    scores = []
    w1 = 0.8
    w2 = 0.15
    w3 = 0.05
    # Quantity score
    S_quantity = float(result['quantity_score'])
    # Technical score
    technical_score = float(result['technical_skills']['technical_score'])
    for project in result['projects']:
        s1 = int(project['relevance_score'])
        s2 = int(project['difficulty_score'])
        s3 = int(project['duration_score'])
        scores.append(w1 * s1 + w2 * s2 + w3 * s3)
    total_score = sum(scores)
    score_project = 0
    for score in scores:
        score_project += score * (score / total_score)
    # Experience score
    expreience_score = S_quantity*score_project
    # Overall score
    overall_score = 0.6*expreience_score + 0.4*technical_score

    return {"technical_score": technical_score, "expreience_score": round(expreience_score, 2), "overall_score": round(overall_score, 2)}

def load_history_and_matching(cv_need_matching: str, id_jd: str):
    jd_summary = get_jd_summary_by_id(id_jd=id_jd)

    # Change llm only - testing zone
    # change_llm(jd_summary, id_jd)

    save_json_name = id_jd + "_chat_history.json"
    save_json_path = os.path.join("data/chat_history", save_json_name)

    with open(save_json_path, 'r') as f:
        retrieve_from_db = json.load(f)

    retrieved_messages = messages_from_dict(retrieve_from_db)
    retrieved_chat_history = ChatMessageHistory(messages=retrieved_messages)

    retrieved_memory = ConversationBufferMemory(chat_memory=retrieved_chat_history, memory_key="chat_history", return_messages=True)
    chat_llm_chain_matchcv = LLMChain(
        llm=llm,
        prompt=chat_template_cv_matching,
        verbose=True,
        memory=retrieved_memory,)
    
    input_data = input_data_cv_matching(cv_need_matching=cv_need_matching, jd_summary=jd_summary)
    
    llm_response = chat_llm_chain_matchcv.invoke({"input_data_cv_matching": input_data})
    matched_result = llm_response.get("text")
    # convert matched_result to json
    matched_result = parser.parse(matched_result)
    
    return matched_result

# def matching cv and jd return percentage of matching using prompt template
def result_matching_cv_jd(id_cv:str, id_jd:str):
    cv_content = get_cv_content_by_id(id_cv)
    
    # Result matching cv and jd
    matched_result = load_history_and_matching(cv_need_matching=cv_content, id_jd=id_jd)

    calculated_score = calculate_matching_score(matched_result)

    # update matched status and matched_result in database
    edit_cv(id_cv, {"matched_status": True, "matched_result": matched_result, "calculated_score": calculated_score})
    return {"matched_result": matched_result, "calculated_score": calculated_score}

def matchingcv_testzone(cv_need_matching: str, jd_summary:str):
    pass