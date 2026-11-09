import pytest
from unittest.mock import MagicMock, patch
from generator import analyze_requirements, QAAnalysisReport, TestCase

@pytest.fixture
def mock_openai_response():
    """Generates a mock structured response identical to OpenAI's parsed output."""
    mock_test_case = TestCase(
        title="Mock Test Case",
        preconditions="User is logged in",
        steps=["Step 1", "Step 2"],
        expected_result="Success",
        gherkin_feature="Scenario: Mock Scenario"
    )
    
    return QAAnalysisReport(
        summary="Test summary",
        potential_requirements_gaps=["Gap 1"],
        security_and_edge_case_concerns=["Concern 1"],
        test_cases=[mock_test_case]
    )

@patch("generator.OpenAI")
def test_analyze_requirements_success(mock_openai_class, mock_openai_response):
    """Validates that the agent correctly invokes the LLM client."""
    # Создаем цепочку вызовов mock для client.beta.chat.completions.parse
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client
    
    mock_parse = mock_client.beta.chat.completions.parse
    
    mock_message = MagicMock()
    mock_message.parsed = mock_openai_response
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    mock_parse.return_value.choices = [mock_choice]

    # Запускаем функцию
    sample_text = "As a user I want to log in."
    result = analyze_requirements(sample_text)

    # Проверки
    assert isinstance(result, QAAnalysisReport)
    assert result.summary == "Test summary"
    assert len(result.test_cases) == 1
    assert result.test_cases[0].title == "Mock Test Case"
    
    # Проверяем, что парсинг ИИ был вызван с нужной структурой данных
    mock_parse.assert_called_once()
    call_kwargs = mock_parse.call_args.kwargs
    assert call_kwargs["model"] == "gpt-4o-mini"
    assert call_kwargs["response_format"] == QAAnalysisReport
