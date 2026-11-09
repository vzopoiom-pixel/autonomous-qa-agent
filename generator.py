import os
import logging
from typing import List
from pydantic import BaseModel, Field
from openai import OpenAI

# Setup structured logging engine
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QA_TestCase(BaseModel):
    """
    Structured Pydantic validation schema for captured test cases.
    Renamed to prevent conflict with Pytest collection mechanisms.
    """
    title: str = Field(..., description="The definitive, concise title of the test scenario")
    preconditions: List[str] = Field(default=[], description="Array of environmental state prerequisites")
    steps: List[str] = Field(..., description="Sequential step-by-step execution path instructions")
    expected_result: str = Field(..., description="The definitive expected baseline response from the system")
    gherkin_scenario: str = Field(..., description="BDD Gherkin syntax representation of this exact workflow")

class RequirementAnalysisSuite(BaseModel):
    """Container schema for total processed test suites validated from dynamic inputs."""
    requirement_id: str
    identified_edge_cases: List[str]
    generated_suite: List[QA_TestCase]

class AutonomousQAAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("[AGENT] OpenAI API Key is missing from runtime contexts.")
        self.client = OpenAI(api_key=self.api_key)

    def analyze_requirements(self, payload_text: str) -> RequirementAnalysisSuite:
        """Processes raw text specifications using GPT-4o structured validation matrices."""
        logger.info("[AGENT] Initiating dynamic payload analysis cycle...")
        
        system_prompt = (
            "You are an Advanced Autonomous QA Automation Engineer. Analyze the incoming software "
            "requirements payload, extract edge cases, and output a strict JSON suite."
        )

        response = self.client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": payload_text}
            ],
            response_format=RequirementAnalysisSuite,
        )
        logger.info("[AGENT] Structure validation completed successfully.")
        return response.choices[0].message.parsed
