"""Fixed unit tests for LLM client implementations."""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import json
from typing import Dict, Any

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
