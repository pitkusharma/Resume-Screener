from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

# Import LLM
from app.core.config import llm

# LLM response output model
from app.models.llm_parser import ParsedResume

parser = PydanticOutputParser(pydantic_object=ParsedResume)

async def extract_resume_metadata(text: str) -> dict:
    """
    Extract structured details (name, email, phone, skills, experience, education) from resume text using LLM.

    Args:
        text (str): Raw text extracted from the resume.

    Returns:
        dict: Parsed resume details as dictionary, or {} if parsing fails.
    """
    prompt_template = ChatPromptTemplate.from_template("""
    You are an expert resume parser. Extract the following from the resume text:
    - Full Name
    - Email
    - Phone
    - Skills (list)
    - Experience (list of {{company, role, duration}})
    - Education (list of {{degree, institution, year}})

    Resume text:
    {resume_text}

    {format_instructions}
    """)

    format_instructions = parser.get_format_instructions()

    # Final input for LLM
    prompt = prompt_template.format(resume_text=text, format_instructions=format_instructions)

    # Using async invoke
    response = await llm.ainvoke(prompt)

    try:
        return parser.parse(response.content).model_dump()
    except Exception:
        return {}


# sample_text = """"""
#
# async def main():
#     print("Testing resume parser with LLM...")
#     result = await extract_resume_metadata(sample_text)
#     print("\nParsed Resume Metadata:")
#     print(result)
# import asyncio
# if __name__ == "__main__":
#     asyncio.run(main())
