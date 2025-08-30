"""Shared test fixtures and configuration."""

import os
import sys
import pytest
import asyncio
from typing import Dict, Any, Generator
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import modules to test
from src.models.base_llm import BaseLLMClient, Message, LLMResponse
from src.agents.base_agent import BaseAgent, AgentConfig
from src.agents.agent_factory import AgentFactory
from config.config import Settings


# Fixtures for test data
@pytest.fixture
def test_config() -> Dict[str, Any]:
    """Provide test configuration."""
    return {
        "name": "TestAgent",
        "description": "Test agent for unit tests",
        "model_provider": "openai",
        "model": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 1000,
        "enable_memory": True,
        "enable_tools": True,
    }


@pytest.fixture
def mock_settings(monkeypatch):
    """Mock settings with test API keys."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-anthropic-key")
    monkeypatch.setenv("GEMINI_API_KEY", "test-gemini-key")
    monkeypatch.setenv("APP_ENV", "development")  # Use valid environment

    settings = Settings()
    return settings


@pytest.fixture
def mock_llm_client():
    """Create a mock LLM client."""
    client = AsyncMock(spec=BaseLLMClient)
    client.generate.return_value = LLMResponse(
        content="Test response", model="test-model", usage={"total_tokens": 10}
    )
    client.generate_stream = AsyncMock()
    client.count_tokens.return_value = 10
    client.model = "test-model"
    client.api_key = "test-key"
    return client


@pytest.fixture
def mock_agent(mock_llm_client):
    """Create a mock agent."""
    config = AgentConfig(
        name="TestAgent", description="Test agent", model_provider="test", model="test-model"
    )

    agent = Mock(spec=BaseAgent)
    agent.config = config
    agent.llm_client = mock_llm_client
    agent.id = "test-agent-id"
    agent.chat = AsyncMock(return_value={"content": "Test response"})
    agent.run = AsyncMock(return_value={"content": "Test response"})

    return agent


@pytest.fixture
def sample_image_data():
    """Provide sample image data for testing."""
    # Create a small 1x1 pixel PNG
    return b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\x00\x00\x00\x01\x00\x01UU\x86\x18\x00\x00\x00\x00IEND\xaeB`\x82"


@pytest.fixture
def sample_audio_data():
    """Provide sample audio data for testing."""
    # Create a minimal WAV header + data
    return b"RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00D\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00"


@pytest.fixture
def sample_training_data():
    """Provide sample training data."""
    return [
        {
            "image_id": "test_001",
            "caption": "A cat sitting on a mat",
            "url": "http://example.com/image1.jpg",
        },
        {
            "image_id": "test_002",
            "caption": "A dog playing in the park",
            "url": "http://example.com/image2.jpg",
        },
    ]


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response."""
    return {
        "id": "chatcmpl-test",
        "object": "chat.completion",
        "created": 1234567890,
        "model": "gpt-4",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": "This is a test response from OpenAI"},
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
    }


@pytest.fixture
def mock_gemini_response():
    """Mock Gemini API response."""
    return {
        "candidates": [
            {
                "content": {
                    "parts": [{"text": "This is a test response from Gemini"}],
                    "role": "model",
                },
                "finishReason": "STOP",
            }
        ],
        "usageMetadata": {
            "promptTokenCount": 10,
            "candidatesTokenCount": 20,
            "totalTokenCount": 30,
        },
    }


@pytest.fixture
def mock_anthropic_response():
    """Mock Anthropic API response."""
    return {
        "id": "msg_test",
        "type": "message",
        "role": "assistant",
        "content": [{"type": "text", "text": "This is a test response from Claude"}],
        "model": "claude-3-opus-20240229",
        "stop_reason": "end_turn",
        "usage": {"input_tokens": 10, "output_tokens": 20},
    }


@pytest.fixture
async def async_client():
    """Create an async test client for FastAPI."""
    from httpx import AsyncClient
    from src.main import app

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for test files."""
    test_dir = tmp_path / "test_data"
    test_dir.mkdir()
    return test_dir


@pytest.fixture
def mock_file_upload():
    """Create a mock file upload object."""
    from fastapi import UploadFile
    from io import BytesIO

    def _create_upload(
        filename: str, content: bytes, content_type: str = "application/octet-stream"
    ):
        file = UploadFile(filename=filename, file=BytesIO(content), content_type=content_type)
        return file

    return _create_upload


# Event loop configuration for async tests
@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Cleanup fixtures
@pytest.fixture(autouse=True)
def cleanup_agents():
    """Clean up agents after each test."""
    yield
    # Clear any global agent storage
    from src.main import agent_store

    agent_store.clear()


@pytest.fixture(autouse=True)
def cleanup_env(monkeypatch):
    """Reset environment variables after each test."""
    yield
    # Environment is automatically restored by monkeypatch


# Mock external services
@pytest.fixture
def mock_external_apis():
    """Mock all external API calls."""
    with (
        patch("openai.OpenAI") as mock_openai,
        patch("google.generativeai.GenerativeModel") as mock_gemini,
        patch("anthropic.Anthropic") as mock_anthropic,
    ):
        # Configure mocks
        mock_openai.return_value.chat.completions.create = AsyncMock()
        mock_gemini.return_value.generate_content = AsyncMock()
        mock_anthropic.return_value.messages.create = AsyncMock()

        yield {"openai": mock_openai, "gemini": mock_gemini, "anthropic": mock_anthropic}
