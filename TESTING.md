# Testing Guide

## Running Tests

### Run all tests
```bash
uv run pytest
```

### Run with verbose output
```bash
uv run pytest -v
```

### Run specific test categories
```bash
# Unit tests only (fast, no external dependencies)
uv run pytest -m unit

# Integration tests only
uv run pytest -m integration

# Run specific test file
uv run pytest tests/test_llm_service.py
```

### Run with coverage
```bash
uv run pytest --cov=app --cov-report=html
```

## Test Structure

### Unit Tests
- **[tests/test_llm_service.py](tests/test_llm_service.py)**: Tests for LLM service
  - Mocks all external API calls
  - Fast execution
  - Tests error handling and edge cases

### Integration Tests
- **[tests/test_webhook_api.py](tests/test_webhook_api.py)**: Tests for webhook endpoints
  - Uses FastAPI TestClient
  - Mocks LLM and WhatsApp API calls
  - Tests full request/response flow

## Demo Scripts

For manual testing and demos, see [examples/](examples/):

### Test LLM service directly
```bash
uv run python examples/demo_llm.py
```

### Test webhook locally
```bash
# Terminal 1 - Start server
uv run python main.py

# Terminal 2 - Send test messages
uv run python examples/demo_webhook_local.py
```

## Writing New Tests

### Unit Test Template
```python
import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.mark.unit
class TestMyFeature:
    async def test_something(self, mocker):
        # Arrange
        mock_service = mocker.patch("app.module.service")

        # Act
        result = await my_function()

        # Assert
        assert result == expected
        mock_service.assert_called_once()
```

### Integration Test Template
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.mark.integration
def test_my_endpoint():
    client = TestClient(app)
    response = client.post("/endpoint", json={"data": "value"})

    assert response.status_code == 200
    assert response.json() == {"expected": "result"}
```

## Continuous Integration

Tests run automatically on:
- Git pre-commit hooks (if configured)
- GitHub Actions (if configured)
- Before Railway deployment (if configured)

## Test Coverage

Current test coverage:
- ✅ LLM service (chat completion, error handling, meal plan generation)
- ✅ Webhook verification
- ✅ Message handling (text, image, status updates)
- ✅ Error scenarios (LLM failures, invalid payloads)

## Troubleshooting

### Tests fail with import errors
```bash
# Reinstall dependencies
uv sync
```

### AsyncIO errors
Make sure you have `pytest-asyncio` installed:
```bash
uv add --dev pytest-asyncio
```

### Mocking issues
Use `pytest-mock` for easier mocking:
```bash
uv add --dev pytest-mock
```
