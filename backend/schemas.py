from pydantic import BaseModel, Field
from typing import List, Optional

class TestCaseBase(BaseModel):
    test_case_id: str = Field(description="Unique identifier for the test case (e.g., TC-001)")
    description: str = Field(description="Clear and concise description of the test scenario")
    preconditions: str = Field(description="Setup or state required before test execution")
    steps: List[str] = Field(description="Ordered list of execution steps")
    expected_result: str = Field(description="The desired state or validation criteria")
    test_type: str = Field(description="Type of test: Functional, Security, UI, Performance, Edge")
    priority: str = Field(description="Execution priority: High, Medium, Low")

class GenerateRequest(BaseModel):
    user_story: str = Field(..., description="The user story text to generate tests for")
    provider: str = Field("openai", description="The LLM provider to use (openai or ollama)")

class GenerateResponse(BaseModel):
    test_cases: List[TestCaseBase]
    metadata: dict
