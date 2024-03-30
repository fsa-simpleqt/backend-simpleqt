# import prompt template
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

# create the prompt template cv_matching
chat_template_cv_matching = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""
Let's think step by step.
Act as a HR Manager in the Information Technology field, given the CV and JD, your task is calculating the matching score between the candidate's qualifications and the job requirements.
It's ok to say candidate does not match the requirement. If the CV is empty, provide a score of 0.
Score range:
    0 to 20: Poor match
    20 to 50: Fair match
    50 to 80: Good match
    80 to 100: Very good match
Scoring guide:
To determine the matching score, analyze the techinical skills, experience in the CV and compare them to the requirements outlined in the JD.
For each section provide the matching score as a numeric value between 0-100, along with a brief explanation of your analysis.
    Technique Skills section: 
        Evaluated based on the relevance of the skills to the job (programming languages, frameworks, databases, cloud technologies and other techinical skills). 
        Example, for an AI Engineer position, Python, Pytorch, TensorFlow, NLP, and LLM are more relevant than Java, C++, or SQL. 
        Candidate with more relevant techinique skills get higher score.
    Experience section: 
        Evaluated based on the relevance, the level of difficult, the duration of the projects to the job and the number of projects in total . 
        Prioritize the relevance, then the level of difficult and the duration.
        Give score to each project, then calculate the quality score and the quantity score.
        Quantity score is calculated by the number of projects:
            0.5 to 0.6: few projects's quantity (1-3 projects)
            0.7 to 0.85: decent projects's quantity (4-6 projects)
            0.85 to 1.0: many projects's quantity (6+ projects)
        Quality score is calculated by the average of all projects' score.
        Experience score = Quality score multiplies by Quantity score
        Example:
        For an AI Engineer position, projects in AI's score > Project in Data Science's score > Project in Front-end's score.
        Projects and experience in companies and corporation's score > Projects and experience in contests > Projects and experience in university's subjetcs.
        Projects and experience in long duration score > Projects and experience in short duration score.
        Projects and experience with high difficult's score > Projects and experience with low difficult's score.
        Candidate with better experience get higher score.
    Overall score = (Technique Skills + Experience) / 2
Skip Education and Achivements section if the candidate does not have any education or achivements.
All comments should use singular pronouns such as "he", "she", "the candidate", or the candidate's name.
You will be penalized if you make up information or provide inaccurate information. You must only use the information provided in the CV and JD. 
"""),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("""
Given the CV below, calculate the matching score between the candidate's qualifications and the job requirements in the JD.
{cv}
You MUST ONLY respond JSON using this format:
(
    "technical_skills":
        ( "technical score": "", "explanation": "" ),
    "experience":
        ( 
            (
            "project_name": "", 
            "score": "", 
            "explanation": "" 
            ),
        # ... more projects
        ),
        ( "quality score": "" ),
        ( "quantity score": "" ),
        ( "experience score": "quality score * quantity score" )
    ),
    "overall_score": "Show the SCORE only."
)
"""),
    ]
)

# create the prompt template history_jd
chat_template_history_jd = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=("""
This is my Job Description. 
Given a job description, identify and summarize the baseline knowledge requirements for applicants. 
Highlight key areas such as educational background, programming proficiency, technical experience and knowledge, language and communication skills, personal qualities, and any specific experience or priority considerations. Provide a structured summary that can be used to evaluate if applicants meet the minimum requirements to proceed to the interview stage. Remember this for the next step."""
            )
        ),
        HumanMessagePromptTemplate.from_template("{jd_summary}"),
    ]
)

# create the prompt template summary_jd
chat_template_sumary_jd = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=("""
Given the job description:
Let's distill it into four parts, focusing on an emphasis distribution where Required Hard Skills, and Job Responsibilities, Experience Requirements, and Soft Skills in Context. Provide a summary as follows:
    - Job Responsibilities: Briefly describe the main duties and projects the role entails, focusing on what the employee will be primarily doing.
    - Required Hard Skills: Detail the essential technical skills, educational qualifications, and any specialized knowledge necessary for performing the job effectively. This section should form the bulk of the summary.
    - Experience Requirements: Highlight the experience level and specific types of previous work or projects that are important for the role, indicating the practical application of skills.
    - Soft Skills in Context: Outline the interpersonal and soft skills required for the role, emphasizing how they contribute to team dynamics, problem-solving, and overall performance within the company.
Let's include any additional notes that may be relevant for understanding preferred qualifications or other aspects not covered by the main sections.
"""
            )
        ),
        HumanMessagePromptTemplate.from_template("""This is my Job Description: {jd}. Distill it into four parts and REMEMBER this for the next step."""),
    ]
)
