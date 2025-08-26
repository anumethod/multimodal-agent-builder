"""Unit tests for LLM client implementations."""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import json
from typing import Dict, Any

from src.models.base_llm import BaseLLMClient, LLMResponse, Message, MessageRole
from src.models.openai_client import OpenAIClient
from src.models.gemini_client import GeminiClient
from src.models.claude_client import ClaudeClient


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


class TestOpenAIClient:
    """Test OpenAI client implementation."""
    
    @pytest.mark.unit
    @pytest.mark.llm
    @patch('openai.AsyncOpenAI')
    @patch('src.models.openai_client.settings')
    def test_openai_client_initialization(self, mock_settings, mock_openai_class):
        """Test OpenAI client initialization."""
        # Mock settings
        mock_settings.get_llm_config.return_value = {
            "api_key": "test-openai-key",
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        client = OpenAIClient(
            api_key="test-openai-key",
            model="gpt-4",
            temperature=0.7
        )
        
        assert client.model == "gpt-4"
        assert client.api_key == "test-openai-key"
        mock_openai_class.assert_called_once()
    
    @pytest.mark.unit
    @pytest.mark.llm
    @pytest.mark.asyncio
    @patch('openai.AsyncOpenAI')
    @patch('src.models.openai_client.settings')
    async def test_openai_generate(self, mock_settings, mock_openai_class, mock_openai_response):
        """Test OpenAI generate method."""
        # Mock settings
        mock_settings.get_llm_config.return_value = {
            "api_key": "test-key",
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 1000
        }
        # Setup mock
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create = AsyncMock(return_value=Mock(**mock_openai_response))
        
        client = OpenAIClient(api_key="test-key", model="gpt-4")
        
        # Test generation
        messages = [{"role": "user", "content": "Hello"}]
        response = await client.generate(messages)
        
        assert response == "This is a test response from OpenAI"
        mock_client.chat.completions.create.assert_called_once()
    
    @pytest.mark.unit
    @pytest.mark.llm
    @pytest.mark.asyncio
    @patch('openai.OpenAI')
    async def test_openai_generate_with_image(self, mock_openai_class, mock_openai_response):
        """Test OpenAI generate with image support."""
        # Setup mock
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.return_value = Mock(**mock_openai_response)
        
        config = LLMConfig(api_key="test-key", model="gpt-4-vision-preview")
        client = OpenAIClient(config)
        
        # Test generation with image
        messages = [{"role": "user", "content": "Describe this image"}]
        response = await client.generate(messages, image=b"fake-image-data")
        
        assert response == "This is a test response from OpenAI"
        
        # Verify image was processed
        call_args = mock_client.chat.completions.create.call_args
        assert call_args is not None
        messages_arg = call_args[1]['messages']
        assert any("image_url" in str(msg) for msg in messages_arg)
    
    @pytest.mark.unit
    @pytest.mark.llm
    @patch('openai.OpenAI')
    def test_openai_count_tokens(self, mock_openai_class):
        """Test OpenAI token counting."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        config = LLMConfig(api_key="test-key", model="gpt-4")
        client = OpenAIClient(config)
        
        # Test token counting (approximation)
        text = "This is a test message"
        token_count = client.count_tokens(text)
        
        assert token_count > 0
        assert isinstance(token_count, int)
    
    @pytest.mark.unit
    @pytest.mark.llm
    @pytest.mark.asyncio
    @patch('openai.OpenAI')
    async def test_openai_function_calling(self, mock_openai_class):
        """Test OpenAI function calling support."""
        # Setup mock with function call response
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        function_response = {
            "id": "chatcmpl-test",
            "object": "chat.completion",
            "created": 1234567890,
            "model": "gpt-4",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": None,
                    "function_call": {
                        "name": "get_weather",
                        "arguments": '{"location": "New York"}'
                    }
                },
                "finish_reason": "function_call"
            }],
            "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
        }
        
        mock_client.chat.completions.create.return_value = Mock(**function_response)
        
        config = LLMConfig(api_key="test-key", model="gpt-4")
        client = OpenAIClient(config)
        
        # Test with functions
        messages = [{"role": "user", "content": "What's the weather?"}]
        functions = [{
            "name": "get_weather",
            "description": "Get weather information",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                }
            }
        }]
        
        response = await client.generate(messages, functions=functions)
        
        # Should return function call info
        assert "get_weather" in response
        assert "New York" in response


class TestGeminiClient:
    """Test Gemini client implementation."""
    
    @pytest.mark.unit
    @pytest.mark.llm
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_gemini_client_initialization(self, mock_model_class, mock_configure):
        """Test Gemini client initialization."""
        config = LLMConfig(
            api_key="test-gemini-key",
            model="gemini-pro",
            temperature=0.7
        )
        
        client = GeminiClient(config)
        
        assert client.model == "gemini-pro"
        assert client.provider == "gemini"
        assert client.config == config
        mock_configure.assert_called_once_with(api_key="test-gemini-key")
        mock_model_class.assert_called_once_with("gemini-pro")
    
    @pytest.mark.unit
    @pytest.mark.llm
    @pytest.mark.asyncio
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    async def test_gemini_generate(self, mock_model_class, mock_configure, mock_gemini_response):
        """Test Gemini generate method."""
        # Setup mock
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model
        mock_model.generate_content.return_value = Mock(**mock_gemini_response)
        
        config = LLMConfig(api_key="test-key", model="gemini-pro")
        client = GeminiClient(config)
        
        # Test generation
        messages = [{"role": "user", "content": "Hello"}]
        response = await client.generate(messages)
        
        assert response == "This is a test response from Gemini"
        mock_model.generate_content.assert_called_once()
    
    @pytest.mark.unit
    @pytest.mark.llm
    @pytest.mark.asyncio
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    @patch('PIL.Image.open')
    async def test_gemini_generate_with_image(self, mock_pil_open, mock_model_class, mock_configure):
        """Test Gemini generate with image support."""
        # Setup mocks
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model
        mock_image = MagicMock()
        mock_pil_open.return_value = mock_image
        
        response_mock = MagicMock()
        response_mock.text = "Image description from Gemini"
        mock_model.generate_content.return_value = response_mock
        
        config = LLMConfig(api_key="test-key", model="gemini-pro-vision")
        client = GeminiClient(config)
        
        # Test generation with image
        messages = [{"role": "user", "content": "Describe this image"}]
        response = await client.generate(messages, image=b"fake-image-data")
        
        assert response == "Image description from Gemini"
        mock_model.generate_content.assert_called_once()
        
        # Verify image was processed
        call_args = mock_model.generate_content.call_args
        assert len(call_args[0]) > 0  # Should have content list
    
    @pytest.mark.unit
    @pytest.mark.llm
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_gemini_count_tokens(self, mock_model_class, mock_configure):
        """Test Gemini token counting."""
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model
        mock_model.count_tokens.return_value = Mock(total_tokens=15)
        
        config = LLMConfig(api_key="test-key", model="gemini-pro")
        client = GeminiClient(config)
        
        # Test token counting
        text = "This is a test message"
        token_count = client.count_tokens(text)
        
        assert token_count == 15
        mock_model.count_tokens.assert_called_once_with(text)


class TestClaudeClient:
    """Test Claude client implementation."""
    
    @pytest.mark.unit
    @pytest.mark.llm
    @patch('anthropic.Anthropic')
    def test_claude_client_initialization(self, mock_anthropic_class):
        """Test Claude client initialization."""
        config = LLMConfig(
            api_key="test-anthropic-key",
            model="claude-3-opus-20240229",
            temperature=0.7
        )
        
        client = ClaudeClient(config)
        
        assert client.model == "claude-3-opus-20240229"
        assert client.provider == "anthropic"
        assert client.config == config
        mock_anthropic_class.assert_called_once_with(api_key="test-anthropic-key")
    
    @pytest.mark.unit
    @pytest.mark.llm
    @pytest.mark.asyncio
    @patch('anthropic.Anthropic')
    async def test_anthropic_generate(self, mock_anthropic_class, mock_anthropic_response):
        """Test Anthropic generate method."""
        # Setup mock
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client
        mock_client.messages.create.return_value = Mock(**mock_anthropic_response)
        
        config = LLMConfig(api_key="test-key", model="claude-3-opus-20240229")
        client = AnthropicClient(config)
        
        # Test generation
        messages = [{"role": "user", "content": "Hello"}]
        response = await client.generate(messages)
        
        assert response == "This is a test response from Claude"
        mock_client.messages.create.assert_called_once()
    
    @pytest.mark.unit
    @pytest.mark.llm
    @pytest.mark.asyncio
    @patch('anthropic.Anthropic')
    async def test_anthropic_generate_with_image(self, mock_anthropic_class):
        """Test Anthropic generate with image support."""
        # Setup mock with image response
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client
        
        image_response = {
            "id": "msg_test",
            "type": "message",
            "role": "assistant",
            "content": [{
                "type": "text",
                "text": "I can see an image"
            }],
            "model": "claude-3-opus-20240229",
            "stop_reason": "end_turn",
            "usage": {"input_tokens": 50, "output_tokens": 20}
        }
        
        mock_client.messages.create.return_value = Mock(**image_response)
        
        config = LLMConfig(api_key="test-key", model="claude-3-opus-20240229")
        client = AnthropicClient(config)
        
        # Test generation with image
        messages = [{"role": "user", "content": "Describe this image"}]
        response = await client.generate(messages, image=b"fake-image-data")
        
        assert response == "I can see an image"
        
        # Verify image was included in request
        call_args = mock_client.messages.create.call_args
        messages_arg = call_args[1]['messages']
        assert any("image" in str(msg).lower() for msg in messages_arg)
    
    @pytest.mark.unit
    @pytest.mark.llm
    @patch('anthropic.Anthropic')
    def test_anthropic_count_tokens(self, mock_anthropic_class):
        """Test Anthropic token counting."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client
        
        config = LLMConfig(api_key="test-key", model="claude-3-opus-20240229")
        client = AnthropicClient(config)
        
        # Test token counting (approximation)
        text = "This is a test message"
        token_count = client.count_tokens(text)
        
        assert token_count > 0
        assert isinstance(token_count, int)
    
    @pytest.mark.unit
    @pytest.mark.llm
    @pytest.mark.asyncio
    @patch('anthropic.Anthropic')
    async def test_anthropic_system_prompt(self, mock_anthropic_class):
        """Test Anthropic system prompt handling."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client
        
        response_data = {
            "id": "msg_test",
            "type": "message",
            "role": "assistant",
            "content": [{"type": "text", "text": "Following system instructions"}],
            "model": "claude-3-opus-20240229",
            "stop_reason": "end_turn",
            "usage": {"input_tokens": 30, "output_tokens": 10}
        }
        
        mock_client.messages.create.return_value = Mock(**response_data)
        
        config = LLMConfig(
            api_key="test-key",
            model="claude-3-opus-20240229",
            system_prompt="You are a helpful assistant"
        )
        client = AnthropicClient(config)
        
        # Test with system prompt
        messages = [{"role": "user", "content": "Hello"}]
        response = await client.generate(messages)
        
        assert response == "Following system instructions"
        
        # Verify system prompt was included
        call_args = mock_client.messages.create.call_args
        assert "system" in call_args[1]
        assert call_args[1]["system"] == "You are a helpful assistant"


# Test error handling for all clients
class TestLLMClientErrorHandling:
    """Test error handling across all LLM clients."""
    
    @pytest.mark.unit
    @pytest.mark.llm
    @pytest.mark.asyncio
    @patch('openai.OpenAI')
    async def test_openai_api_error(self, mock_openai_class):
        """Test OpenAI client handles API errors."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        
        config = LLMConfig(api_key="test-key", model="gpt-4")
        client = OpenAIClient(config)
        
        with pytest.raises(Exception, match="API Error"):
            await client.generate([{"role": "user", "content": "Hello"}])
    
    @pytest.mark.unit
    @pytest.mark.llm
    @pytest.mark.asyncio
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    async def test_gemini_api_error(self, mock_model_class, mock_configure):
        """Test Gemini client handles API errors."""
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model
        mock_model.generate_content.side_effect = Exception("API Error")
        
        config = LLMConfig(api_key="test-key", model="gemini-pro")
        client = GeminiClient(config)
        
        with pytest.raises(Exception, match="API Error"):
            await client.generate([{"role": "user", "content": "Hello"}])
    
    @pytest.mark.unit
    @pytest.mark.llm
    @pytest.mark.asyncio
    @patch('anthropic.Anthropic')
    async def test_anthropic_api_error(self, mock_anthropic_class):
        """Test Anthropic client handles API errors."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client
        mock_client.messages.create.side_effect = Exception("API Error")
        
        config = LLMConfig(api_key="test-key", model="claude-3-opus-20240229")
        client = AnthropicClient(config)
        
        with pytest.raises(Exception, match="API Error"):
            await client.generate([{"role": "user", "content": "Hello"}])
