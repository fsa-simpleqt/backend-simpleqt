# import prompt template
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage

# create the prompt template
chat_template_cv_matching = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                """Given the following CV and JD, calculate the percentage match between the candidate's qualifications and the job requirements:
CV: {cv}
JD: {jd}
To determine the match percentage, analyze the skills and experience in the CV and compare them to the requirements outlined in the JD. Provide the final match percentage as a numeric value between 0-100%, along with a brief explanation of your analysis. Follow this json format: {"Skills Match": {"Required Skills": "","Candidate Skills": "","Match Percentage": "",}, "Experience Match": {"Required Experience": "","Candidate Experience": "","Match Percentage": "",}, "Overall Match Percentage:": "", "Explanation": ""}
                """
            )
        ),
        HumanMessagePromptTemplate.from_template(["{cv}", "{jd}"]),
    ]
)

# create the prompt template
chat_template_sumary_jd = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                """Based on the following job description:
{jobdes}
Play the role of an expert in job description analysis. Carefully analyze candidate requirements and job descriptions. Let's separate them into 2 separate parts
                """
            )
        ),
        HumanMessagePromptTemplate.from_template("{jobdes}"),
    ]
)
