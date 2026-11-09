import os
from openai import OpenAI
from pydantic import BaseModel
from typing import List

class TestCase(BaseModel):
    title: str
    preconditions: str
    steps: List[str]
    expected_result: str
    gherkin_feature: str

class QAAnalysisReport(BaseModel):
    summary: str
    potential_requirements_gaps: List[str]
    security_and_edge_case_concerns: List[str]
    test_cases: List[TestCase]

def analyze_requirements(user_story_text: str) -> QAAnalysisReport:
    """
    Leverages LLM with Structured Outputs to parse business requirements,
    identify logical vulnerabilities, and output a production-ready test suite.
    """
    # Инициализация клиента перенесена внутрь для безопасного тестирования
    api_key = os.environ.get("OPENAI_API_KEY", "mock-key-for-testing")
    client = OpenAI(api_key=api_key)

    prompt = f"""
    You are an expert Senior QA Automation Engineer and AI Specialist.
    Analyze the following User Story/Requirements:
    1. Detect potential logical gaps, missing edge cases, or business logic ambiguities.
    2. Identify security, performance, or boundary vulnerabilities.
    3. Generate a comprehensive test suite (including positive, negative, and edge scenarios).
    4. Provide strict Gherkin (Given-When-Then) syntax for each test case.

    Requirements to analyze:
    \"\"\"{user_story_text}\"\"\"
    """

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a precise, production-grade QA Automation Assistant."},
            {"role": "user", "content": prompt}
        ],
        response_format=QAAnalysisReport,
    )

    return completion.choices.message.parsed

if __name__ == "__main__":
    sample_story = """
    User Story: As a registered premium user, I want to request a wire transfer payout.
    Acceptance Criteria:
    - User triggers 'Request Payout' from the dashboard.
    - System verifies if the balance is sufficient.
    - Transactions above $5,000 require a 2FA SMS verification code (expires in 5 minutes).
    - Payout requests are queued for compliance review if the destination account is international.
    """
    
    print("⏳ Executing AI QA Agent Analysis...")
    report = analyze_requirements(sample_story)
    print(f"\n✅ Total Automated Test Cases Generated: {len(report.test_cases)}")
