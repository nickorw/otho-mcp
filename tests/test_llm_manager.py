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

from gen_ai_hub.proxy.langchain import init_llm
from gen_ai_hub.proxy.langchain.openai import ChatOpenAI

from src.utils.llm_manager import (
    call_gaih_google,
    call_gaih_openai,
    call_gemini,
    call_gen_ai_hub,
    call_llm,
    get_gaih_google_llm,
    get_gaih_openai_llm,
    proxy_client,
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


class TestO3Integration(unittest.TestCase):
    """
    Live integration tests for o3 model initialization.

    These tests make actual API calls to test both instantiation methods:
    1. init_llm (legacy method used for o1 models)
    2. ChatOpenAI (newer method)

    Run these tests specifically with:
        python -m pytest tests/test_llm_manager.py::TestO3Integration -v
    """

    def setUp(self):
        """Set up test fixtures."""
        self.test_prompt = "What is 2+2? Answer with just the number."
        self.model_name = "o3"

    def test_o3_with_init_llm(self):
        """
        Test o3 initialization using init_llm (legacy method).

        This is the method used for o1, o1-mini, o1-preview models.
        """
        print("\n" + "=" * 60)
        print("Testing o3 with init_llm (legacy method)")
        print("=" * 60)

        try:
            # Initialize using init_llm (same as legacy models)
            llm = init_llm(self.model_name, max_tokens=4096)
            print(f"✓ LLM initialized successfully")
            print(f"  Type: {type(llm).__name__}")

            # Invoke the model
            print(f"  Invoking with prompt: '{self.test_prompt}'")
            response = llm.invoke(self.test_prompt)

            # Extract content
            if hasattr(response, "content"):
                result = response.content
            else:
                result = str(response)

            print(f"✓ Response received: {result}")

            # Basic assertion - we got a response
            self.assertIsNotNone(result)
            self.assertTrue(len(str(result)) > 0)
            print("✓ Test PASSED: init_llm works with o3")

        except Exception as e:
            print(f"✗ Test FAILED with error: {type(e).__name__}: {e}")
            raise

    def test_o3_with_chat_openai(self):
        """
        Test o3 initialization using ChatOpenAI (newer method).

        This is the method used for gpt-4.1+ and other newer models.
        """
        print("\n" + "=" * 60)
        print("Testing o3 with ChatOpenAI (newer method)")
        print("=" * 60)

        try:
            # Initialize using ChatOpenAI (newer method)
            llm = ChatOpenAI(
                proxy_model_name=self.model_name,
                proxy_client=proxy_client,
                temperature=0.5,
            )
            print(f"✓ LLM initialized successfully")
            print(f"  Type: {type(llm).__name__}")

            # Invoke the model
            print(f"  Invoking with prompt: '{self.test_prompt}'")
            response = llm.invoke(self.test_prompt)

            # Extract content
            if hasattr(response, "content"):
                result = response.content
            else:
                result = str(response)

            print(f"✓ Response received: {result}")

            # Basic assertion - we got a response
            self.assertIsNotNone(result)
            self.assertTrue(len(str(result)) > 0)
            print("✓ Test PASSED: ChatOpenAI works with o3")

        except Exception as e:
            print(f"✗ Test FAILED with error: {type(e).__name__}: {e}")
            raise

    def test_o3_via_get_gaih_openai_llm(self):
        """
        Test o3 through the current get_gaih_openai_llm function.

        This tests the current routing logic in llm_manager.py.
        Currently o3 is NOT in legacy_models, so it will use ChatOpenAI.
        """
        print("\n" + "=" * 60)
        print("Testing o3 via get_gaih_openai_llm (current routing)")
        print("=" * 60)

        try:
            # Get LLM through the main function
            llm = get_gaih_openai_llm(self.model_name)
            print(f"✓ LLM initialized successfully")
            print(f"  Type: {type(llm).__name__}")
            print(
                f"  (Current routing sends o3 to: {'init_llm' if self.model_name in ['gpt-4o', 'gpt-4o-mini', 'o1', 'o1-mini', 'o1-preview'] else 'ChatOpenAI'})"
            )

            # Invoke the model
            print(f"  Invoking with prompt: '{self.test_prompt}'")
            response = llm.invoke(self.test_prompt)

            # Extract content
            if hasattr(response, "content"):
                result = response.content
            else:
                result = str(response)

            print(f"✓ Response received: {result}")

            # Basic assertion - we got a response
            self.assertIsNotNone(result)
            self.assertTrue(len(str(result)) > 0)
            print("✓ Test PASSED: get_gaih_openai_llm works with o3")

        except Exception as e:
            print(f"✗ Test FAILED with error: {type(e).__name__}: {e}")
            raise


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


class TestGeminiIntegration(unittest.TestCase):
    """
    Live integration tests for Gemini model initialization via GenAIHub.

    These tests make actual API calls to test get_gaih_google_llm.

    Run these tests specifically with:
        python tests/test_llm_manager.py --gemini-only
    """

    def setUp(self):
        """Set up test fixtures."""
        self.test_prompt = "What is 2+2? Answer with just the number."
        self.model_name = "gemini-2.5-flash"

    def test_gemini_flash_via_get_gaih_google_llm(self):
        """
        Test gemini-2.5-flash initialization using get_gaih_google_llm.

        This tests the LangChain-compatible LLM object for Google/Gemini via GenAIHub.
        """
        print("\n" + "=" * 60)
        print("Testing gemini-2.5-flash via get_gaih_google_llm")
        print("=" * 60)

        try:
            # Initialize using get_gaih_google_llm
            llm = get_gaih_google_llm(self.model_name)
            print(f"✓ LLM initialized successfully")
            print(f"  Type: {type(llm).__name__}")
            print(f"  Model: {self.model_name}")

            # Invoke the model
            print(f"  Invoking with prompt: '{self.test_prompt}'")
            response = llm.invoke(self.test_prompt)

            # Extract content - Gemini may return different structures
            if hasattr(response, "content"):
                result = response.content
            elif hasattr(response, "text"):
                result = response.text
            else:
                result = str(response)

            print(f"✓ Response received: {result}")

            # Basic assertion - we got a response
            self.assertIsNotNone(result)
            self.assertTrue(len(str(result)) > 0)
            print("✓ Test PASSED: get_gaih_google_llm works with gemini-2.5-flash")

        except Exception as e:
            print(f"✗ Test FAILED with error: {type(e).__name__}: {e}")
            raise

    def test_gemini_pro_via_get_gaih_google_llm(self):
        """
        Test gemini-2.5-pro initialization using get_gaih_google_llm.
        """
        print("\n" + "=" * 60)
        print("Testing gemini-2.5-pro via get_gaih_google_llm")
        print("=" * 60)

        try:
            model_name = "gemini-2.5-pro"
            llm = get_gaih_google_llm(model_name)
            print(f"✓ LLM initialized successfully")
            print(f"  Type: {type(llm).__name__}")
            print(f"  Model: {model_name}")

            # Invoke the model
            print(f"  Invoking with prompt: '{self.test_prompt}'")
            response = llm.invoke(self.test_prompt)

            # Extract content
            if hasattr(response, "content"):
                result = response.content
            elif hasattr(response, "text"):
                result = response.text
            else:
                result = str(response)

            print(f"✓ Response received: {result}")

            # Basic assertion - we got a response
            self.assertIsNotNone(result)
            self.assertTrue(len(str(result)) > 0)
            print("✓ Test PASSED: get_gaih_google_llm works with gemini-2.5-pro")

        except Exception as e:
            print(f"✗ Test FAILED with error: {type(e).__name__}: {e}")
            raise


def run_o3_tests():
    """Run only the o3 integration tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add only o3 test class
    suite.addTests(loader.loadTestsFromTestCase(TestO3Integration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


def run_gemini_tests():
    """Run only the Gemini integration tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add only Gemini test class
    suite.addTests(loader.loadTestsFromTestCase(TestGeminiIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run LLM Manager tests")
    parser.add_argument(
        "--o3-only", action="store_true", help="Run only the o3 integration tests"
    )
    parser.add_argument(
        "--gemini-only",
        action="store_true",
        help="Run only the Gemini integration tests",
    )
    args = parser.parse_args()

    if args.o3_only:
        print("\n" + "#" * 60)
        print("# Running o3 Integration Tests")
        print("#" * 60)
        success = run_o3_tests()
    elif args.gemini_only:
        print("\n" + "#" * 60)
        print("# Running Gemini Integration Tests")
        print("#" * 60)
        success = run_gemini_tests()
    else:
        success = run_tests()

    sys.exit(0 if success else 1)
