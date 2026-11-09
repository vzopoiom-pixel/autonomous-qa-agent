import pytest
from unittest.mock import MagicMock
from generator import AutonomousQAAgent, RequirementAnalysisSuite, QA_TestCase

def test_analyze_requirements_success():
    """Verifies successful payload parsing using mocked OpenAI client responses."""
    # 1. Provision structured mock payload data blocks
    mock_case = QA_TestCase(
        title="Verify secure authentication",
        preconditions=["User is registered", "Database online"],
        steps=["Navigate to auth endpoint", "Submit corporate credentials"],
        expected_result="System returns JWT tracking token",
        gherkin_scenario="Scenario: Successful authentication\nGiven environmental states are met..."
    )
    
    mock_suite = RequirementAnalysisSuite(
        requirement_id="REQ-42",
        identified_edge_cases=["Expired tokens handling", "SQL injection insertion bounds"],
        generated_suite=[mock_case]
    )

    # 2. Mock Agent execution layers
    agent = AutonomousQAAgent(api_key="mocked-production-key-token")
    agent.client.beta.chat.completions.parse = MagicMock()
    
    # Configure mock choices payload matrix mapping
    mock_choice = MagicMock()
    mock_choice.message.parsed = mock_suite
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    
    agent.client.beta.chat.completions.parse.return_value = mock_response

    # 3. Trigger analysis and execute rigid integrity checks
    result = agent.analyze_requirements("Sample software specification payload")
    
    assert result.requirement_id == "REQ-42"
    assert len(result.identified_edge_cases) == 2
    assert result.generated_suite[0].title == "Verify secure authentication"
