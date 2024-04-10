import os
import json
from fastapi import HTTPException

from app.modules.crud_jds.models.crud_jds import get_jd_summary_by_id, get_jd_by_id
from app.modules.crud_cvs.models.crud_cvs import get_cv_content_by_id, edit_cv, get_cv_by_id
from app.utils.chat_templates import chat_template_cv_matching, input_data_cv_matching
from app.configs.llm_model import llm
from urllib.request import urlopen

from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.memory.chat_message_histories.in_memory import ChatMessageHistory
from langchain_core.output_parsers import JsonOutputParser
from langchain.schema import messages_from_dict
parser = JsonOutputParser()

def check_config_score(config_score: dict):
    # Technical score weight
    W_technical_score = config_score["technical_score_config"]["W_technical_score"]
    # Expreience score weight
    W_expreience_score = config_score["experience_score_config"]["W_experience_score"]

    # Ingredient of expreience score
    relevance_score_w = config_score["experience_score_config"]["relevance_score_w"]
    difficulty_score_w = config_score["experience_score_config"]["difficulty_score_w"]
    duration_score_w = config_score["experience_score_config"]["duration_score_w"]

    if W_technical_score + W_expreience_score != 1:
        return HTTPException(status_code=400, detail="Sum of W_technical_score and W_expreience_score must be 1")
    if relevance_score_w + difficulty_score_w + duration_score_w != 1:
        return HTTPException(status_code=400, detail="Sum of relevance_score_w, difficulty_score_w and duration_score_w must be 1")

def calculate_quantity_score(projects):
    n = len(projects)
    quantity_score = 0.35 + 0.05 * n
    if quantity_score > 0.9:
        return 0.9
    elif n in [1, 2]:
        return 0.35
    else:
        return quantity_score

def calculate_matching_score(matched_result: dict, config_score: dict):
    # Technical score weight
    W_technical_score = config_score["technical_score_config"]["W_technical_score"]
    # Expreience score weight
    W_expreience_score = config_score["experience_score_config"]["W_experience_score"]

    # Ingredient of expreience score
    relevance_score_w = config_score["experience_score_config"]["relevance_score_w"]
    difficulty_score_w = config_score["experience_score_config"]["difficulty_score_w"]
    duration_score_w = config_score["experience_score_config"]["duration_score_w"]

    # Technical score
    technical_score = float(matched_result["technical_skills"]["technical_score"])
    # Quantity score
    projects = matched_result["projects"]
    S_quantity = calculate_quantity_score(projects)

    # Project score
    scores = []
    for project in matched_result["projects"]:
        s1 = float(project["relevance_score"])
        s2 = float(project["difficulty_score"])
        s3 = float(project["duration_score"])
        scores.append(relevance_score_w * s1 + difficulty_score_w * s2 + duration_score_w * s3)
    total_score = sum(scores)
    score_project = 0
    for score in scores:
        score_project += score * (score / total_score)
    # Experience score
    expreience_score = S_quantity*score_project
    # Overall score
    overall_score = W_technical_score * technical_score + W_expreience_score * expreience_score

    return {"technical_score": technical_score, "expreience_score": round(expreience_score, 2), "overall_score": round(overall_score, 2)}

def load_history_and_matching(cv_need_matching: str, id_jd: str):
    jd_summary = get_jd_summary_by_id(id_jd=id_jd)
    chat_history_url = get_jd_by_id(id_jd).get("chat_history_url")

    response = urlopen(chat_history_url)
    retrieve_from_db = json.loads(response.read())

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
def result_matching_cv_jd(id_cv:str, id_jd:str, config_score: dict, start_matching: bool):    
    if start_matching:
        cv_content = get_cv_content_by_id(id_cv)
        # Result matching cv and jd
        matched_result = load_history_and_matching(cv_need_matching=cv_content, id_jd=id_jd)
        matching_score = calculate_matching_score(matched_result=matched_result, config_score=config_score)
        # update matched status and matched_result in database
        edit_cv(id_cv, {"matched_status": True, "matched_result": matched_result, "matching_score": matching_score})
    else:
        # load matched_result from database
        matched_result = get_cv_by_id(id_cv).get("matched_result")
        matching_score = calculate_matching_score(matched_result=matched_result, config_score=config_score)
        # update matched status and matched_result in database
        edit_cv(id_cv, {"matching_score": matching_score})

    return id_cv, matching_score
