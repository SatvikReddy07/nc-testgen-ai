from langchain.prompts import PromptTemplate

# The 5-Lens prompt instructs the LLM to think from 5 different QA perspectives.
FIVE_LENS_PROMPTSTR = """You are a Senior QA Automation Engineer and Test Case Architect.
Your task is to analyze the following User Story and generate comprehensive, structured test cases.

USER STORY:
{user_story}

To ensure complete coverage, you MUST evaluate the story using the "5-Lens Method":
1. **Functional Lens**: Does the feature work across the happy path and standard alternate paths?
2. **Edge Case Lens**: What extreme inputs, corrupted states, or unexpected user behaviors might break it?
3. **Security Lens**: Could this be exploited via injection, unauthorized access, or logic bypass?
4. **UI/UX Lens**: How does it behave on different screens, rendering states, or with accessibility tools?
5. **Performance Lens**: What happens under load, concurrent requests, or network latency?

Generate at least one high-quality test case for each lens.

{format_instructions}
"""

five_lens_prompt = PromptTemplate(
    template=FIVE_LENS_PROMPTSTR,
    input_variables=["user_story"],
    partial_variables={"format_instructions": ""} # Will be injected by the parser
)
