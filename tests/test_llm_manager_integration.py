"""
Integration tests for the LLM Manager module.

These tests make ACTUAL API calls to verify the LLM integrations work correctly.
WARNING: These tests will consume API credits and require valid credentials in .env

Run these tests separately from unit tests:
    python tests/test_llm_manager_integration.py
"""

import sys
import unittest
from pathlib import Path

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


class TestLLMManagerIntegration(unittest.TestCase):
    """Integration tests that make real API calls to verify functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_prompt = "What is 2+2? Answer with just the number."
        self.expected_answer = "4"

    def test_call_gemini_direct_real(self):
        """Test direct Gemini API call with real API."""
        print("\n🔄 Testing direct Gemini API call...")
        try:
            result = call_gemini(self.test_prompt)
            print(f"✅ Response: {result[:100]}...")

            # Basic validation - response should exist and contain the answer
            self.assertIsNotNone(result)
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 0)
            self.assertIn(self.expected_answer, result)

            print("✅ Direct Gemini test passed!")
        except Exception as e:
            self.fail(f"Direct Gemini API call failed: {e}")

    def test_call_gaih_google_real(self):
        """Test Google model via GenAIHub with real API."""
        print("\n🔄 Testing GenAIHub Google API call...")
        try:
            result = call_gaih_google("gemini-2.5-flash", self.test_prompt)
            print(f"✅ Response: {result[:100]}...")

            # Basic validation
            self.assertIsNotNone(result)
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 0)

            print("✅ GenAIHub Google test passed!")
        except Exception as e:
            self.fail(f"GenAIHub Google API call failed: {e}")

    def test_call_gaih_openai_real(self):
        """Test OpenAI model via GenAIHub with real API."""
        print("\n🔄 Testing GenAIHub OpenAI API call...")
        try:
            result = call_gaih_openai("o1", self.test_prompt)
            print(f"✅ Response: {result[:100]}...")

            # Basic validation
            self.assertIsNotNone(result)
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 0)
            self.assertIn(self.expected_answer, result)

            print("✅ GenAIHub OpenAI test passed!")
        except Exception as e:
            self.fail(f"GenAIHub OpenAI API call failed: {e}")

    def test_call_llm_dispatcher_gemini_direct(self):
        """Test call_llm dispatcher with gemini-direct type."""
        print("\n🔄 Testing call_llm with gemini-direct...")
        try:
            result = call_llm("gemini-direct", self.test_prompt)
            print(f"✅ Response: {result[:100]}...")

            self.assertIsNotNone(result)
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 0)
            self.assertIn(self.expected_answer, result)

            print("✅ call_llm gemini-direct test passed!")
        except Exception as e:
            self.fail(f"call_llm gemini-direct failed: {e}")

    def test_call_llm_dispatcher_gemini(self):
        """Test call_llm dispatcher with gemini type."""
        print("\n🔄 Testing call_llm with gemini type...")
        try:
            result = call_llm("gemini", self.test_prompt)
            print(f"✅ Response: {result[:100]}...")

            self.assertIsNotNone(result)
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 0)

            print("✅ call_llm gemini test passed!")
        except Exception as e:
            self.fail(f"call_llm gemini failed: {e}")

    def test_call_llm_dispatcher_openai(self):
        """Test call_llm dispatcher with openai type."""
        print("\n🔄 Testing call_llm with openai type...")
        try:
            result = call_llm("openai", self.test_prompt)
            print(f"✅ Response: {result[:100]}...")

            self.assertIsNotNone(result)
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 0)
            self.assertIn(self.expected_answer, result)

            print("✅ call_llm openai test passed!")
        except Exception as e:
            self.fail(f"call_llm openai failed: {e}")

    def test_error_handling_invalid_model(self):
        """Test that invalid model names are handled gracefully."""
        print("\n🔄 Testing error handling with invalid model...")
        try:
            # This should default to gemini-direct
            result = call_llm("invalid_type", self.test_prompt)
            print(f"✅ Fallback response: {result[:100]}...")

            self.assertIsNotNone(result)
            self.assertIsInstance(result, str)

            print("✅ Error handling test passed!")
        except Exception as e:
            self.fail(f"Error handling test failed: {e}")


class TestLLMManagerPerformance(unittest.TestCase):
    """Performance tests to measure API response times."""

    def test_response_time_gemini_direct(self):
        """Measure response time for direct Gemini calls."""
        import time

        print("\n⏱️  Measuring Gemini direct response time...")
        start = time.time()
        result = call_gemini("What is 2+2?")
        elapsed = time.time() - start

        print(f"✅ Response time: {elapsed:.2f}s")
        self.assertLess(elapsed, 30, "Response took too long (>30s)")

    def test_response_time_genaihub(self):
        """Measure response time for GenAIHub calls."""
        import time

        print("\n⏱️  Measuring GenAIHub response time...")
        start = time.time()
        result = call_llm("gemini", "What is 2+2?")
        elapsed = time.time() - start

        print(f"✅ Response time: {elapsed:.2f}s")
        self.assertLess(elapsed, 30, "Response took too long (>30s)")


def run_integration_tests():
    """Run the integration test suite."""
    print("\n" + "=" * 70)
    print("🚀 RUNNING INTEGRATION TESTS - REAL API CALLS")
    print("⚠️  WARNING: These tests will consume API credits!")
    print("=" * 70 + "\n")

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestLLMManagerIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestLLMManagerPerformance))

    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary table
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)

    total_tests = result.testsRun
    passed_tests = total_tests - len(result.failures) - len(result.errors)
    failed_tests = len(result.failures) + len(result.errors)

    print(f"\nTotal Tests Run: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"Success Rate: {(passed_tests / total_tests * 100):.1f}%\n")

    # Detailed results
    print("-" * 70)
    print("DETAILED RESULTS:")
    print("-" * 70)

    # List passed tests
    if passed_tests > 0:
        print("\n✅ PASSED TESTS:")
        all_tests = []
        for test_class in [TestLLMManagerIntegration, TestLLMManagerPerformance]:
            for attr_name in dir(test_class):
                if attr_name.startswith("test_"):
                    all_tests.append(f"{test_class.__name__}.{attr_name}")

        failed_test_names = set()
        for failure in result.failures + result.errors:
            test_name = failure[0]._testMethodName
            test_class = failure[0].__class__.__name__
            failed_test_names.add(f"{test_class}.{test_name}")

        for test in all_tests:
            if test not in failed_test_names:
                test_short_name = (
                    test.split(".")[-1].replace("test_", "").replace("_", " ").title()
                )
                print(f"  ✓ {test_short_name}")

    # List failed tests
    if failed_tests > 0:
        print("\n❌ FAILED TESTS:")
        for failure in result.failures + result.errors:
            test_name = failure[0]._testMethodName
            test_short_name = test_name.replace("test_", "").replace("_", " ").title()
            error_msg = str(failure[1]).split("\n")[0][:60]
            print(f"  ✗ {test_short_name}")
            print(f"    └─ {error_msg}...")

    print("\n" + "=" * 70)
    if result.wasSuccessful():
        print("✅ ALL INTEGRATION TESTS PASSED!")
    else:
        print("⚠️  SOME TESTS FAILED - Review details above")
    print("=" * 70 + "\n")

    return result.wasSuccessful()


if __name__ == "__main__":
    import sys

    # Confirm before running
    print(
        "\n⚠️  WARNING: You are about to run integration tests that make REAL API calls."
    )
    print("This will consume API credits and may incur costs.")
    response = input("\nDo you want to continue? (yes/no): ").strip().lower()

    if response not in ["yes", "y"]:
        print("\n❌ Tests cancelled by user.")
        sys.exit(0)

    success = run_integration_tests()
    sys.exit(0 if success else 1)
