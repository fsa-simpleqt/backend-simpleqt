import os
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.evaluation import load_evaluator
from langchain.evaluation import EmbeddingDistance

import firebase_admin
from firebase_admin import credentials, storage, db

# Import API key
load_dotenv()
# Define the google api key
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

storageBucket = "fsa-firebase-tutorial.appspot.com"
databaseURL = "https://fsa-firebase-tutorial-default-rtdb.asia-southeast1.firebasedatabase.app/"
cred = credentials.Certificate('credentials\\fsa-firebase-database.json')

#Initialize the app
firebase_admin.initialize_app(cred, {
     'storageBucket': storageBucket,
     'databaseURL': databaseURL
})

# Setting model embedding
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
gemini_evaluator = load_evaluator("embedding_distance", distance_metric=EmbeddingDistance.COSINE, embeddings=embedding_model)


#Connect to firebase and query a list have key of description and content of description
def query_firebase():
    temp_file_list = []
    database_json = db.reference('EXAM-DATA').get()
    for key, value in database_json.items():
        temp_file_list.append({key: (value.get('description'))})
    return temp_file_list

#find the directory of firebase database
def query_file(path):
    database = db.reference(path)
    ref = database.get()
    return ref

#Extract url file by description
def extract_file_url_by_description(file_dict, target_description):
    file_urls = []
    for key, value in file_dict.items():
        if value.get('description') == target_description:
            file_urls.append(value.get('file_url'))
    return file_urls

#download test from firebase 
def download_from_file_url(file_url_list, local_directory):
    temp_content_list = []
    bucket = storage.bucket(storageBucket)
    for file_url in file_url_list:
        parts = []
        parts = file_url.split('/')
        legal_file_url = parts[3:][0]
        ref = bucket.blob(legal_file_url)
        local_filename = f"{local_directory}/{legal_file_url}"
        ref.download_to_filename(local_filename)
        print(f"Downloaded {legal_file_url} to {local_filename}")
    return True

def download_from_description(target_description, download_path='data\question_for_jd'):
    database_file = query_file('EXAM-DATA')
    file_url_list = extract_file_url_by_description(database_file, target_description)
    download_from_file_url(file_url_list, download_path)
    return

#In a list above, get all value: all description in database 
def get_des_list(list):
    list_des = []
    for item in list:
        for key, value in item.items():
             list_des.append(value)
    return list_des

#Compare two vector: The first vector is extract text and all description in database 
def compare_vector(vector_extract, vector_des):
    maxnimun_value = 2
    for item in vector_des:
        two_object = (vector_extract, item)
        x = gemini_evaluator.evaluate_strings(prediction=two_object[0], reference=two_object[1]) #use gemini_evaluator to compare two vector
        if x.get('score') < maxnimun_value: 
            maxnimun_value = x.get('score') 
            item_choose = item
        
    return item_choose  

#get question (download all question) of prompt
def get_question(text):
    text = "Job Title is Senior AI Engineer, Level is Senior, and Brief summary of required skills is NLP, experiencing in using Docker"
    value_db = query_firebase()
    value_in_des = get_des_list(value_db)
    item_choose = compare_vector(text, value_in_des)
    print(item_choose)
    download_from_description(item_choose)

if __name__ == "__main__":
    get_question("hihi")
