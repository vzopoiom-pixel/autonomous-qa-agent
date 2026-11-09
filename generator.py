import os
import json
from openai import OpenAI
from pydantic import BaseModel
from typing import List

# Initialize OpenAI client (expects OPENAI_API_KEY environment variable)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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

    # Utilizing OpenAI's Structured Outputs for guaranteed schema validation
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
    # Realistic complex requirement snippet
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
    
    print("\n📝 Executive Analysis Summary:")
    print(report.summary)
    
    print("\n⚠️ Identified Requirements Gaps / Logic Flaws:")
    for gap in report.potential_requirements_gaps:
        print(f" - [GAP]: {gap}")
        
    print("\n🔒 Security & Edge Case Alerts:")
    for concern in report.security_and_edge_case_concerns:
        print(f" - [WARN]: {concern}")
        
    print(f"\n✅ Total Automated Test Cases Generated: {len(report.test_cases)}")
    
    # Save the output directly as a structured JSON artifact
    output_filename = "ai_generated_test_suite.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(report.model_dump_json(indent=4))
    print(f"\n💾 Production artifact saved to '{output_filename}'")
