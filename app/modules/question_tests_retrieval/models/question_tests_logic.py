import os
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.evaluation import load_evaluator
from langchain.evaluation import EmbeddingDistance

from app.modules.crud_question_test.models.crud_question_tests import get_all_question_tests, get_question_test_url_by_description
from app.configs.database import firebase_bucket

# Import API key
load_dotenv()

# Define the google api key
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# Setting model embedding
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
gemini_evaluator = load_evaluator("embedding_distance", distance_metric=EmbeddingDistance.COSINE, embeddings=embedding_model)


def compare_vector(vector_extract, vector_des):
    maxnimun_value = 2
    for item in vector_des:
        two_object = (vector_extract, item)
        x = gemini_evaluator.evaluate_strings(prediction=two_object[0], reference=two_object[1])
        # print(f"item and score: {item} - {x.get('score')}")
        if x.get('score') < maxnimun_value: 
            maxnimun_value = x.get('score')
            print("maxnimun_value: ", maxnimun_value)
            des_item_choose = item
    if maxnimun_value == 2:
        return False
    elif maxnimun_value < 0.3:
        return des_item_choose
    else:
        return False

def download_question_test(question_test_url):
    # check folder exist
    if not os.path.exists('data/question_tests'):
        os.makedirs('data/question_tests')
    # download file from firebase storage using "gs://" link
    name_bucket = question_test_url.split(f"gs://{firebase_bucket.name}/")[1]
    blob = firebase_bucket.blob(name_bucket)
    blob.download_to_filename(f'data/question_tests/{name_bucket}')
    return True
    


def get_question_test(text):
    all_question_tests = get_all_question_tests()
    value_in_des = []
    for item in all_question_tests:
        value_in_des.append(item['question_tests_description'])
    des_item_choose = compare_vector(text, value_in_des)
    if des_item_choose == False:
        return "No question test found"
    else:
        question_test_url = get_question_test_url_by_description(des_item_choose)
        if download_question_test(question_test_url):
            return True
        else:
            return False
