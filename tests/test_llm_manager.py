"""
Unit tests for the LLM Manager module.

This test suite covers the LLM initialization and calling functionality,
including tests for different LLM providers (Gemini, OpenAI, Anthropic).
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables before importing llm_manager
import dotenv

dotenv.load_dotenv()

from src.utils.llm_manager import (
    call_gaih_google,
    call_gaih_openai,
    call_gemini,
    call_gen_ai_hub,
    call_llm,
)


class TestLLMManager(unittest.TestCase):
    """Test cases for LLM Manager functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_prompt = "What is the capital of France?"
        self.test_model = "gemini-2.5-flash"
        self.expected_response = "Paris is the capital of France."

    @patch("src.utils.llm_manager.llm_gemini")
    def test_call_gemini(self, mock_llm_gemini):
        """Test direct Gemini API call."""
        # Mock the response
        mock_response = Mock()
        mock_response.text = self.expected_response
        mock_llm_gemini.models.generate_content.return_value = mock_response

        # Call the function
        result = call_gemini(self.test_prompt)

        # Assertions
        self.assertEqual(result, self.expected_response)
        mock_llm_gemini.models.generate_content.assert_called_once_with(
            model="gemini-2.5-flash",
            contents=self.test_prompt,
        )

    @patch("src.utils.llm_manager.GenerativeModel")
    @patch("src.utils.llm_manager.proxy_client")
    def test_call_gen_ai_hub(self, mock_proxy_client, mock_generative_model):
        """Test GenAIHub native API call."""
        # Mock the GenerativeModel instance and response
        mock_llm_instance = Mock()
        mock_response = Mock()
        mock_response._raw_response = self.expected_response
        mock_llm_instance.generate_content.return_value = mock_response
        mock_generative_model.return_value = mock_llm_instance

        # Call the function
        result = call_gen_ai_hub(self.test_model, self.test_prompt)

        # Assertions
        self.assertEqual(result, self.expected_response)
        mock_generative_model.assert_called_once()
        mock_llm_instance.generate_content.assert_called_once()

    @patch("src.utils.llm_manager.GenerativeModel")
    @patch("src.utils.llm_manager.proxy_client")
    def test_call_gaih_google(self, mock_proxy_client, mock_generative_model):
        """Test Google model call via GenAIHub."""
        # Mock the GenerativeModel instance and response
        mock_llm_instance = Mock()
        mock_response = Mock()
        mock_response._raw_response = self.expected_response
        mock_llm_instance.generate_content.return_value = mock_response
        mock_generative_model.return_value = mock_llm_instance

        # Call the function
        result = call_gaih_google(self.test_model, self.test_prompt)

        # Assertions
        self.assertEqual(result, self.expected_response)
        mock_generative_model.assert_called_once()
        mock_llm_instance.generate_content.assert_called_once()

    @patch("src.utils.llm_manager.ChatOpenAI")
    @patch("src.utils.llm_manager.proxy_client")
    def test_call_gaih_openai(self, mock_proxy_client, mock_chat_openai):
        """Test OpenAI model call via GenAIHub."""
        # Mock the ChatOpenAI instance and response
        mock_llm_instance = Mock()
        mock_response = Mock()
        mock_response.content = self.expected_response
        mock_llm_instance.invoke.return_value = mock_response
        mock_chat_openai.return_value = mock_llm_instance

        # Call the function
        result = call_gaih_openai(self.test_model, self.test_prompt)

        # Assertions
        self.assertEqual(result, self.expected_response)
        mock_chat_openai.assert_called_once_with(
            proxy_model_name=self.test_model,
            proxy_client=mock_proxy_client,
            temperature=0.5,
        )
        mock_llm_instance.invoke.assert_called_once_with(self.test_prompt)

    @patch("src.utils.llm_manager.call_gemini")
    def test_call_llm_gemini_direct(self, mock_call_gemini):
        """Test call_llm with gemini-direct type."""
        mock_call_gemini.return_value = self.expected_response

        result = call_llm("gemini-direct", self.test_prompt)

        self.assertEqual(result, self.expected_response)
        mock_call_gemini.assert_called_once_with(self.test_prompt)

    @patch("src.utils.llm_manager.call_gaih_google")
    def test_call_llm_gemini(self, mock_call_gaih_google):
        """Test call_llm with gemini type."""
        mock_call_gaih_google.return_value = self.expected_response

        result = call_llm("gemini", self.test_prompt, self.test_model)

        self.assertEqual(result, self.expected_response)
        mock_call_gaih_google.assert_called_once_with(self.test_model, self.test_prompt)

    @patch("src.utils.llm_manager.call_gaih_openai")
    def test_call_llm_openai(self, mock_call_gaih_openai):
        """Test call_llm with openai type."""
        mock_call_gaih_openai.return_value = self.expected_response

        result = call_llm("openai", self.test_prompt, "o1")

        self.assertEqual(result, self.expected_response)
        mock_call_gaih_openai.assert_called_once_with("o1", self.test_prompt)

    @patch("src.utils.llm_manager.call_gen_ai_hub")
    def test_call_llm_anthropic(self, mock_call_gen_ai_hub):
        """Test call_llm with anthropic type."""
        mock_call_gen_ai_hub.return_value = self.expected_response

        result = call_llm("anthropic", self.test_prompt, self.test_model)

        self.assertEqual(result, self.expected_response)
        mock_call_gen_ai_hub.assert_called_once_with(self.test_model, self.test_prompt)

    @patch("src.utils.llm_manager.call_gemini")
    def test_call_llm_default(self, mock_call_gemini):
        """Test call_llm with unrecognized type defaults to Gemini."""
        mock_call_gemini.return_value = self.expected_response

        result = call_llm("unknown_type", self.test_prompt)

        self.assertEqual(result, self.expected_response)
        mock_call_gemini.assert_called_once_with(self.test_prompt)

    @patch("src.utils.llm_manager.call_gaih_google")
    def test_call_llm_with_default_model(self, mock_call_gaih_google):
        """Test call_llm uses default model when none provided."""
        mock_call_gaih_google.return_value = self.expected_response

        result = call_llm("gemini", self.test_prompt)

        # Should use default model "gemini-2.5-pro" (as per implementation)
        mock_call_gaih_google.assert_called_once_with(
            "gemini-2.5-pro", self.test_prompt
        )


class TestLLMManagerIntegration(unittest.TestCase):
    """Integration tests that verify the LLM manager can be imported and used."""

    def test_import_llm_manager(self):
        """Test that llm_manager can be imported successfully."""
        try:
            from src.utils.llm_manager import call_llm

            self.assertTrue(callable(call_llm))
        except ImportError as e:
            self.fail(f"Failed to import llm_manager: {e}")

    def test_llm_manager_functions_exist(self):
        """Test that all expected functions exist in llm_manager."""
        from src.utils import llm_manager

        expected_functions = [
            "call_gemini",
            "call_gen_ai_hub",
            "call_gaih_google",
            "call_gaih_openai",
            "call_llm",
        ]

        for func_name in expected_functions:
            self.assertTrue(
                hasattr(llm_manager, func_name),
                f"Function {func_name} not found in llm_manager",
            )
            self.assertTrue(
                callable(getattr(llm_manager, func_name)),
                f"{func_name} is not callable",
            )


def run_tests():
    """Run the test suite."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestLLMManager))
    suite.addTests(loader.loadTestsFromTestCase(TestLLMManagerIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
