import firebase_admin
from firebase_admin import credentials, storage, db

storageBucket = "fsa-firebase-tutorial.appspot.com"
databaseURL = "https://fsa-firebase-tutorial-default-rtdb.asia-southeast1.firebasedatabase.app/"

cred = credentials.Certificate('credentials\\fsa-firebase-database.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': storageBucket,
    'databaseURL': databaseURL
})


# Upload file to storage
def upload_file(file_path, destination_path):
    bucket = storage.bucket(storageBucket)
    ref = bucket.blob(destination_path)
    ref.upload_from_filename(file_path)
    return True

# Add file's url and metadata to realtime database
def store_metadata(file_url, description):
    database = db.reference('exam_data')  # Or your desired path
    new_file_ref = database.push()
    new_file_ref.set({
        'file_url': file_url,
        'description': description
    })
    return True

# Query file's url and metadata from file's metadata
def query_file_from_metadata(target_description):
    temp_file_dict = {}
    database_json = db.reference('exam_data').get()
    for key, value in database_json.items():
        if (target_description in value.get('description')):
            temp_file_dict.update({key: value})
    return temp_file_dict

# Query database path
def query_file(path):
    database = db.reference(path)
    ref = database.get()
    return ref

# Extract file's url from a bunch of things
def extract_file_url(file_dict):
    file_urls = []
    for key, value in file_dict.items():
        file_urls.append(value['file_url'])
    return file_urls

# Extract file's url with target description from a bunch of things
def extract_file_url_by_description(file_dict, target_description):
    file_urls = []
    for key, value in file_dict.items():
        if value.get('description') == target_description:
            file_urls.append(value.get('file_url'))
    return file_urls

# Read file content, given its url
def read_from_file_url(file_url_list):
    temp_content_list = []
    bucket = storage.bucket(storageBucket)
    for file_url in file_url_list:
        parts = []
        parts = file_url.split('/')
        legal_file_url = parts[3:][0]
        ref = bucket.blob(legal_file_url)
        file_content = ref.download_as_string().decode('utf-8')
        temp_content_list.append(file_content)
    return temp_content_list

# Download file content, given its url
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
