from fastapi import APIRouter, Form

from app.modules.quiz_generations.models.quiz_gen_logic import generate_question
from app.modules.crud_jds.models.crud_jds import get_jd_summary_by_id

quiz_gen_router = APIRouter(prefix="/quiz_gen", tags=["quiz_gen"])

@quiz_gen_router.get("/")
async def index():
    return {"message": "Welcome to quiz generator page"}

@quiz_gen_router.post("/send_jd_to_gen_quiz")
async def quiz_gen(id_jd: str):
    try:
        # sumaryjd_text = get_jd_summary_by_id(id_jd=id_jd)
        # json_quiz_gen = generate_question(jobtext=sumaryjd_text)
        json_quiz_gen = {
  "count": 10,
  "data": [
    {
      "id": "1",
      "question": "What is the main focus of the job responsibilities described?",
      "choices": [
        "A. Developing mobile applications",
        "B. Research and development of AI models for NLP and Generative AI",
        "C. Managing social media campaigns",
        "D. Designing user interfaces"
      ],
      "explanation": "The main focus of the job responsibilities is on research, development, testing, deployment, and benchmarking of AI models for NLP and Generative AI.",
      "answer": "B. Research and development of AI models for NLP and Generative AI",
      "level": "Senior",
      "domain": "AI and Machine Learning"
    },
    {
      "id": "2",
      "question": "Which programming language is mentioned as a required hard skill?",
      "choices": [
        "A. Java",
        "B. Python",
        "C. C++",
        "D. Ruby"
      ],
      "explanation": "Python is mentioned as a required hard skill in the job description.",
      "answer": "B. Python",
      "level": "Fresher",
      "domain": "Programming"
    },
    {
      "id": "3",
      "question": "What is a required hard skill related to deep learning frameworks?",
      "choices": [
        "A. TensorFlow",
        "B. Angular",
        "C. React",
        "D. Django"
      ],
      "explanation": "Proficiency in deep learning frameworks such as Pytorch, transformers, and sentence-transformers is required.",
      "answer": "A. Pytorch, transformers, sentence-transformers",
      "level": "Junior",
      "domain": "Deep Learning"
    },
    {
      "id": "4",
      "question": "What experience is required in AI or machine learning?",
      "choices": [
        "A. 3-5 years",
        "B. 1-3 years",
        "C. Fresh graduate",
        "D. No experience required"
      ],
      "explanation": "1-3 years of experience in AI or machine learning is required.",
      "answer": "B. 1-3 years",
      "level": "Fresher",
      "domain": "AI and Machine Learning"
    },
    {
      "id": "5",
      "question": "Which soft skill is important for working effectively in cross-functional teams?",
      "choices": [
        "A. Leadership",
        "B. Collaboration",
        "C. Creativity",
        "D. Time management"
      ],
      "explanation": "Collaboration is important for working effectively in cross-functional teams according to the job description.",
      "answer": "B. Collaboration",
      "level": "Junior",
      "domain": "Soft Skills"
    },
    {
      "id": "6",
      "question": "What type of code is required to be written for backend APIs?",
      "choices": [
        "A. Basic",
        "B. Robust and secure",
        "C. Experimental",
        "D. Frontend"
      ],
      "explanation": "Robust and secure code is required to be written for backend APIs.",
      "answer": "B. Robust and secure",
      "level": "Senior",
      "domain": "Programming"
    },
    {
      "id": "7",
      "question": "What is the focus of the job responsibilities related to machine learning algorithms?",
      "choices": [
        "A. Data visualization",
        "B. Implementing and optimizing machine learning algorithms for NLP and content generation",
        "C. Frontend development",
        "D. Database management"
      ],
      "explanation": "The focus is on implementing and optimizing machine learning algorithms for NLP and content generation.",
      "answer": "B. Implementing and optimizing machine learning algorithms for NLP and content generation",
      "level": "Junior",
      "domain": "Machine Learning"
    },
    {
      "id": "8",
      "question": "What is a required hard skill related to building datasets and training models for text classification?",
      "choices": [
        "A. Data analysis",
        "B. Experience with vector search",
        "C. Building datasets and training models for text classification",
        "D. Web development"
      ],
      "explanation": "Experience building datasets and training models for text classification is a required hard skill.",
      "answer": "C. Building datasets and training models for text classification",
      "level": "Fresher",
      "domain": "Data Science"
    },
    {
      "id": "9",
      "question": "What is a soft skill important for evaluating and implementing practical solutions?",
      "choices": [
        "A. Creativity",
        "B. Problem-solving",
        "C. Communication",
        "D. Time management"
      ],
      "explanation": "Problem-solving is important for evaluating and implementing practical solutions.",
      "answer": "B. Problem-solving",
      "level": "Junior",
      "domain": "Soft Skills"
    },
    {
      "id": "10",
      "question": "What is a soft skill important for communicating effectively in English?",
      "choices": [
        "A. Leadership",
        "B. Collaboration",
        "C. Communication",
        "D. Time management"
      ],
      "explanation": "Communication is important for communicating effectively in English according to the job description.",
      "answer": "C. Communication",
      "level": "Fresher",
      "domain": "Soft Skills"
    }
  ]
}
        return {"message": "Generate question successfully", "json_quiz_gen": json_quiz_gen}
    except Exception as e:
        return {"message": "Please upload only .txt file", "error": str(e)}

@quiz_gen_router.post("/add_gen_quiz_to_jd")
async def quiz_gen(id_jd: str = Form(...), json_quiz_gen: dict = Form(...)):
    pass