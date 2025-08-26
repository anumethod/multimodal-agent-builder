"""Basic tests for LLM client implementations."""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock

from src.models.base_llm import BaseLLMClient, LLMResponse, Message, MessageRole


class TestBaseLLMClient:
    """Test the base LLM client abstract class."""
    
    @pytest.mark.unit
    @pytest.mark.llm
    def test_base_client_is_abstract(self):
        """Test that BaseLLMClient is abstract and cannot be instantiated."""
        # Should not be able to instantiate abstract class
        with pytest.raises(TypeError):
            client = BaseLLMClient(
                api_key="test-key",
                model="test-model",
                temperature=0.7,
                max_tokens=1000
            )
    
    @pytest.mark.unit
    @pytest.mark.llm
    def test_message_dataclass(self):
        """Test Message dataclass."""
        msg = Message(
            role=MessageRole.USER,
            content="Test message"
        )
        
        assert msg.role == MessageRole.USER
        assert msg.content == "Test message"
        assert msg.name is None
        assert msg.function_call is None
        
        # Test to_dict
        msg_dict = msg.to_dict()
        assert msg_dict["role"] == "user"
        assert msg_dict["content"] == "Test message"
    
    @pytest.mark.unit
    @pytest.mark.llm
    def test_message_role_enum(self):
        """Test MessageRole enum."""
        assert MessageRole.SYSTEM.value == "system"
        assert MessageRole.USER.value == "user"
        assert MessageRole.ASSISTANT.value == "assistant"
        assert MessageRole.FUNCTION.value == "function"
    
    @pytest.mark.unit
    @pytest.mark.llm
    def test_llm_response_dataclass(self):
        """Test LLMResponse dataclass."""
        response = LLMResponse(
            content="Test response",
            model="gpt-4",
            usage={"total_tokens": 100}
        )
        
        assert response.content == "Test response"
        assert response.model == "gpt-4"
        assert response.usage["total_tokens"] == 100
        assert response.finish_reason is None
        assert response.function_call is None
        assert response.raw_response is None
