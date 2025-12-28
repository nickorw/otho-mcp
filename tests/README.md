# Otho Tests

This directory contains unit and integration tests for the Otho project.

## Test Structure

- `test_llm_manager.py` - Unit tests for LLM Manager (uses mocking, no API calls)
- `test_llm_manager_integration.py` - Integration tests for LLM Manager (makes REAL API calls)

## Running Tests

### Unit Tests (No API Calls - Safe to Run Anytime)

These tests use mocking and don't make real API calls:

**Recommended: Run with pytest (if installed)**

```bash
# Run unit tests only
python -m pytest tests/test_llm_manager.py -v

# Run with coverage report
python -m pytest tests/test_llm_manager.py --cov=src.utils.llm_manager --cov-report=html
```

**Alternative: Run directly**
```bash
python tests/test_llm_manager.py
```

### Integration Tests (REAL API Calls - Consumes Credits!)

⚠️ **WARNING**: These tests make actual API calls and will consume API credits!

```bash
# Run integration tests (will prompt for confirmation)
python tests/test_llm_manager_integration.py
```

The script will ask for confirmation before running. It tests:
- Direct Gemini API calls
- GenAIHub Google API calls  
- GenAIHub OpenAI API calls
- The call_llm dispatcher function
- Error handling and fallbacks
- Response time performance

**Run ALL tests together** (unit + integration):
```bash
python -m pytest tests/ -v
```

**Why pytest?** 
- Better test discovery
- More detailed output
- Better assertion messages
- Support for fixtures and plugins
- Coverage integration

### Alternative: Run directly (no dependencies)

```bash
# Run specific test file directly
python tests/test_llm_manager.py
```

**Why direct execution?**
- No additional dependencies required
- Quick and simple for single file testing
- Good for debugging individual test files

### Alternative: Run with unittest (built-in)

```bash
# Discover and run all tests
python -m unittest discover tests/ -v
```

**Why unittest?**
- Built into Python (no installation needed)
- Standard library solution
- Good for CI/CD where you want minimal dependencies

## Our Recommendation

For development: Use **pytest** for the best developer experience.
For CI/CD: Use **unittest** or **direct execution** to avoid extra dependencies.

## Writing New Tests

1. Create test files with prefix `test_`
2. Use `unittest.TestCase` as base class (compatible with all methods)
3. Mock external dependencies to avoid API calls
4. Write clear, descriptive test names
5. Add docstrings to explain what's being tested
