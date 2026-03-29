import time
import os
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from schemas import TestCaseBase
from pydantic import BaseModel, Field
from typing import List
from prompts import five_lens_prompt

# Create a wrapper model so parser returns a List properly
class TestCaseList(BaseModel):
    test_cases: List[TestCaseBase] = Field(description="List of structured test cases")

parser = PydanticOutputParser(pydantic_object=TestCaseList)
# Inject the parser instructions into our prompt
five_lens_prompt.partial_variables = {"format_instructions": parser.get_format_instructions()}

async def generate_test_cases(user_story: str, provider: str = "openai") -> dict:
    start_time = time.time()
    
    # We enforce OpenAI for the MVP, but structure allows extension
    if provider.lower() == "openai":
        # For a real execution, OPENAI_API_KEY must be in the environment natively
        # we will set a default or dummy if missing so it doesn't crash on init
        # but fails on network.
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    else:
        # Fallback to Ollama if explicitly requested
        from langchain_community.llms import Ollama
        llm = Ollama(model="llama3")

    # Construct the pipeline
    chain = five_lens_prompt | llm | parser
    
    # Execute synchronously (blocking, as per MVP constraint)
    # Using invoke because it's a simple sequential execution
    try:
        result: TestCaseList = chain.invoke({"user_story": user_story})
        test_cases = result.test_cases
    except Exception as e:
        # Fallback or error handling in MVP: Wrap error in a fake test case for visibility
        from schemas import TestCaseBase
        error_tc = TestCaseBase(
            test_case_id="ERR-001",
            description=f"LLM Generation Failed: {str(e)}",
            preconditions="User must provide a valid API Key and Story",
            steps=["1. Check API Key", "2. Check Network"],
            expected_result="Test cases are generated",
            test_type="System",
            priority="High"
        )
        test_cases = [error_tc]
        
    generation_time = int((time.time() - start_time) * 1000)
    
    return {
        "test_cases": test_cases,
        "metadata": {
            "provider": provider,
            "generation_time_ms": generation_time
        }
    }
