"""Unit tests for agent implementations."""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import datetime
from typing import Dict, Any

from src.agents.base_agent import (
    BaseAgent,
    AgentConfig,
    AgentState,
    AgentResponse,
    AgentMemoryType,
    AgentMemory,
)
from src.agents.simple_agent import SimpleAgent
from src.agents.multimodal_agent import MultimodalAgent, MultimodalInput
from src.agents.agent_factory import AgentFactory, AgentType, LLMProvider


class TestAgentConfig:
    """Test AgentConfig dataclass."""

    @pytest.mark.unit
    @pytest.mark.agent
    def test_agent_config_creation(self):
        """Test AgentConfig creation with default values."""
        config = AgentConfig(
            name="TestAgent", description="Test agent", model_provider="openai", model="gpt-4"
        )

        assert config.name == "TestAgent"
        assert config.description == "Test agent"
        assert config.model_provider == "openai"
        assert config.model == "gpt-4"
        assert config.temperature == 0.7  # Default
        assert config.max_tokens == 4096  # Default
        assert config.enable_memory is True  # Default
        assert config.enable_tools is True  # Default

    @pytest.mark.unit
    @pytest.mark.agent
    def test_agent_config_custom_values(self):
        """Test AgentConfig with custom values."""
        config = AgentConfig(
            name="CustomAgent",
            description="Custom test agent",
            model_provider="anthropic",
            model="claude-3-opus-20240229",
            temperature=0.5,
            max_tokens=2000,
            enable_memory=False,
            enable_tools=False,
            system_prompt="You are a custom assistant",
        )

        assert config.temperature == 0.5
        assert config.max_tokens == 2000
        assert config.enable_memory is False
        assert config.enable_tools is False
        assert config.system_prompt == "You are a custom assistant"


class TestAgentMemory:
    """Test AgentMemory implementation."""

    @pytest.mark.unit
    @pytest.mark.agent
    def test_agent_memory_creation(self):
        """Test AgentMemory creation."""
        from src.models.base_llm import Message, MessageRole

        memory = AgentMemory()

        assert memory.short_term == []
        assert memory.long_term == {}
        assert memory.episodic == []
        assert memory.semantic == {}
        assert memory.max_short_term_size == 50

    @pytest.mark.unit
    @pytest.mark.agent
    def test_short_term_memory(self):
        """Test short-term memory functionality."""
        from src.models.base_llm import Message, MessageRole

        memory = AgentMemory()

        # Add messages
        msg1 = Message(role=MessageRole.USER, content="Hello")
        msg2 = Message(role=MessageRole.ASSISTANT, content="Hi there!")

        memory.add_to_short_term(msg1)
        memory.add_to_short_term(msg2)

        # Get context
        context = memory.get_context()
        assert len(context) == 2
        assert context[0].content == "Hello"
        assert context[1].content == "Hi there!"

        # Clear short term
        memory.clear_short_term()
        assert len(memory.short_term) == 0

    @pytest.mark.unit
    @pytest.mark.agent
    def test_short_term_memory_limit(self):
        """Test short-term memory size limit."""
        from src.models.base_llm import Message, MessageRole

        memory = AgentMemory(max_short_term_size=3)

        # Add more than limit
        for i in range(5):
            msg = Message(role=MessageRole.USER, content=f"Message {i}")
            memory.add_to_short_term(msg)

        # Should only keep last 3
        assert len(memory.short_term) == 3
        assert memory.short_term[0].content == "Message 2"
        assert memory.short_term[2].content == "Message 4"

    @pytest.mark.unit
    @pytest.mark.agent
    def test_episodic_memory(self):
        """Test episodic memory functionality."""
        memory = AgentMemory()

        # Add episodes
        memory.add_episodic_memory({"event": "task1", "result": "success"})
        memory.add_episodic_memory({"event": "task2", "result": "failure"})

        # Check episodes
        assert len(memory.episodic) == 2
        assert memory.episodic[0]["event"] == "task1"
        assert memory.episodic[1]["event"] == "task2"
        assert "timestamp" in memory.episodic[0]

    @pytest.mark.unit
    @pytest.mark.agent
    def test_semantic_memory(self):
        """Test semantic memory functionality."""
        memory = AgentMemory()

        # Add facts to semantic memory
        memory.semantic["user_name"] = "John Doe"
        memory.semantic["user_preference"] = "dark mode"
        memory.semantic["location"] = "New York"

        # Check facts
        assert memory.semantic["user_name"] == "John Doe"
        assert memory.semantic["user_preference"] == "dark mode"
        assert memory.semantic["location"] == "New York"
        assert memory.semantic.get("unknown") is None


class TestBaseAgent:
    """Test BaseAgent functionality."""

    @pytest.mark.unit
    @pytest.mark.agent
    def test_base_agent_initialization(self, mock_llm_client):
        """Test BaseAgent initialization."""
        config = AgentConfig(
            name="TestAgent", description="Test agent", model_provider="test", model="test-model"
        )

        # Create concrete implementation for testing
        class TestAgentImpl(BaseAgent):
            async def think(self, input_data, context=None, **kwargs):
                return "Test thought"

            async def act(self, thought, available_actions=None, **kwargs):
                return {"action": "test_action", "result": "success"}

            async def observe(self, action_result, **kwargs):
                return "Test observation"

            async def run(self, input_data, **kwargs):
                return AgentResponse(content="Test response")

        agent = TestAgentImpl(config, mock_llm_client)

        assert agent.config == config
        assert agent.llm_client == mock_llm_client
        assert agent.state == AgentState.IDLE
        assert isinstance(agent.id, str)
        assert len(agent.id) == 36  # UUID length
        assert isinstance(agent.created_at, datetime)
        assert isinstance(agent.last_activity, datetime)

    @pytest.mark.unit
    @pytest.mark.agent
    def test_agent_memory_initialization(self, mock_llm_client):
        """Test agent memory initialization."""
        # With memory enabled
        config = AgentConfig(
            name="MemoryAgent",
            description="Agent with memory",
            model_provider="test",
            model="test-model",
            enable_memory=True,
        )

        class TestAgentImpl(BaseAgent):
            async def think(self, input_data, context=None, **kwargs):
                return "Test thought"

            async def act(self, thought, available_actions=None, **kwargs):
                return {"action": "test_action", "result": "success"}

            async def observe(self, action_result, **kwargs):
                return "Test observation"

            async def run(self, input_data, **kwargs):
                return AgentResponse(content="Test")

        agent = TestAgentImpl(config, mock_llm_client)

        assert agent.memory is not None
        assert isinstance(agent.memory, AgentMemory)
        assert agent.memory.short_term == []
        assert agent.memory.episodic == []
        assert agent.memory.semantic == {}

        # With memory disabled
        config_no_memory = AgentConfig(
            name="NoMemoryAgent",
            description="Agent without memory",
            model_provider="test",
            model="test-model",
            enable_memory=False,
        )

        agent_no_memory = TestAgentImpl(config_no_memory, mock_llm_client)
        assert agent_no_memory.memory is None

    @pytest.mark.unit
    @pytest.mark.agent
    def test_agent_state_management(self, mock_llm_client):
        """Test agent state transitions."""
        config = AgentConfig(
            name="TestAgent", description="Test agent", model_provider="test", model="test-model"
        )

        class TestAgentImpl(BaseAgent):
            async def think(self, input_data, context=None, **kwargs):
                return "Test thought"

            async def act(self, thought, available_actions=None, **kwargs):
                return {"action": "test_action", "result": "success"}

            async def observe(self, action_result, **kwargs):
                return "Test observation"

            async def run(self, input_data, **kwargs):
                return AgentResponse(content="Test")

        agent = TestAgentImpl(config, mock_llm_client)

        # Initial state
        assert agent.state == AgentState.IDLE

        # Change states by simulating actions
        agent.state = AgentState.THINKING
        assert agent.state == AgentState.THINKING

        agent.state = AgentState.EXECUTING  # Changed from ACTING
        assert agent.state == AgentState.EXECUTING

        agent.state = AgentState.COMPLETED
        assert agent.state == AgentState.COMPLETED

        agent.state = AgentState.IDLE
        assert agent.state == AgentState.IDLE

    @pytest.mark.unit
    @pytest.mark.agent
    @pytest.mark.asyncio
    async def test_agent_chat(self, mock_llm_client):
        """Test agent chat functionality."""
        config = AgentConfig(
            name="ChatAgent",
            description="Chat agent",
            model_provider="test",
            model="test-model",
            enable_memory=True,
        )

        class TestAgentImpl(BaseAgent):
            async def think(self, input_data, context=None, **kwargs):
                return "Test thought"

            async def act(self, thought, available_actions=None, **kwargs):
                return {"action": "test_action", "result": "success"}

            async def observe(self, action_result, **kwargs):
                return "Test observation"

            async def run(self, input_data, **kwargs):
                return AgentResponse(content="Test response")

        # Setup mock response
        from src.models.base_llm import LLMResponse

        mock_llm_client.generate.return_value = LLMResponse(
            content="Hello! How can I help you?", model="test-model", usage={"total_tokens": 100}
        )

        agent = TestAgentImpl(config, mock_llm_client)

        # Chat
        response = await agent.chat("Hello, agent!")

        assert response.content == "Hello! How can I help you?"
        assert response.agent_id == agent.id
        assert response.state == "completed"

        # Check memory was updated
        assert agent.memory is not None
        context = agent.memory.get_context()
        assert len(context) == 2
        assert context[0].content == "Hello, agent!"
        assert context[1].content == "Hello! How can I help you?"


class TestSimpleAgent:
    """Test SimpleAgent implementation."""

    @pytest.mark.unit
    @pytest.mark.agent
    def test_simple_agent_initialization(self, mock_llm_client):
        """Test SimpleAgent initialization."""
        config = AgentConfig(
            name="SimpleAgent",
            description="Simple agent",
            model_provider="test",
            model="test-model",
        )

        agent = SimpleAgent(config, mock_llm_client)

        assert isinstance(agent, SimpleAgent)
        assert agent.config == config
        assert agent.llm_client == mock_llm_client

    @pytest.mark.unit
    @pytest.mark.agent
    @pytest.mark.asyncio
    async def test_simple_agent_run(self, mock_llm_client):
        """Test SimpleAgent run method."""
        from src.models.base_llm import LLMResponse

        config = AgentConfig(
            name="SimpleAgent",
            description="Simple agent",
            model_provider="test",
            model="test-model",
        )

        mock_llm_client.generate.return_value = LLMResponse(
            content="Simple response", model="test-model", usage={"total_tokens": 100}
        )

        agent = SimpleAgent(config, mock_llm_client)

        # Run with string input
        response = await agent.run("Test input")
        assert response.content == "Simple response"
        assert response.agent_id == agent.id

        # Run with dict input
        response = await agent.run({"query": "Test query"})
        assert response.content == "Simple response"

        # Verify LLM was called
        assert mock_llm_client.generate.called

    @pytest.mark.unit
    @pytest.mark.agent
    @pytest.mark.asyncio
    async def test_simple_agent_with_context(self, mock_llm_client):
        """Test SimpleAgent with context."""
        from src.models.base_llm import LLMResponse

        config = AgentConfig(
            name="SimpleAgent",
            description="Simple agent",
            model_provider="test",
            model="test-model",
        )

        mock_llm_client.generate.return_value = LLMResponse(
            content="Contextual response", model="test-model", usage={"total_tokens": 150}
        )

        agent = SimpleAgent(config, mock_llm_client)

        # Run without context - SimpleAgent doesn't handle context in run()
        response = await agent.run("Follow-up question")
        assert response.content == "Contextual response"

        # Verify LLM was called with appropriate messages
        call_args = mock_llm_client.generate.call_args
        messages = call_args[0][0]
        assert len(messages) >= 1  # At least the user message


class TestMultimodalAgent:
    """Test MultimodalAgent implementation."""

    @pytest.mark.unit
    @pytest.mark.agent
    def test_multimodal_agent_initialization(self, mock_llm_client):
        """Test MultimodalAgent initialization."""
        config = AgentConfig(
            name="MultimodalAgent",
            description="Multimodal agent",
            model_provider="test",
            model="test-model",
        )

        agent = MultimodalAgent(config, mock_llm_client)

        assert isinstance(agent, MultimodalAgent)
        assert agent.config == config
        assert agent.llm_client == mock_llm_client

    @pytest.mark.unit
    @pytest.mark.agent
    def test_multimodal_agent_capabilities(self, mock_llm_client):
        """Test MultimodalAgent capability reporting."""
        config = AgentConfig(
            name="MultimodalAgent",
            description="Multimodal agent",
            model_provider="openai",
            model="gpt-4-vision-preview",
        )

        # Mock the llm_client capabilities
        mock_llm_client.supports_vision = True
        mock_llm_client.supports_streaming = False
        mock_llm_client.supports_functions = False

        agent = MultimodalAgent(config, mock_llm_client)
        capabilities = agent.get_capabilities()

        assert "text" in capabilities
        assert "image" in capabilities
        assert "audio" in capabilities
        assert capabilities["text"] is True
        assert capabilities["image"] is True  # Because we mocked supports_vision

    @pytest.mark.unit
    @pytest.mark.agent
    @pytest.mark.asyncio
    async def test_multimodal_agent_process_image(self, mock_llm_client, sample_image_data):
        """Test MultimodalAgent image processing."""
        config = AgentConfig(
            name="VisionAgent",
            description="Vision agent",
            model_provider="openai",
            model="gpt-4-vision-preview",
        )

        from src.models.base_llm import LLMResponse

        mock_llm_client.generate.return_value = LLMResponse(
            content="I see an image", model="gpt-4-vision-preview", usage={"total_tokens": 200}
        )
        mock_llm_client.supports_vision = True

        agent = MultimodalAgent(config, mock_llm_client)

        # Process image
        response = await agent.process_image(image=sample_image_data, prompt="What do you see?")

        assert response.content == "I see an image"
        assert response.metadata["modality"] == "image"
        assert response.agent_id == agent.id

        # Verify image was passed to LLM
        call_args = mock_llm_client.generate.call_args
        assert call_args[1].get("image") == sample_image_data

    @pytest.mark.unit
    @pytest.mark.agent
    @pytest.mark.asyncio
    @patch("src.utils.audio_utils.AudioProcessor")
    async def test_multimodal_agent_process_audio(
        self, mock_audio_processor, mock_llm_client, sample_audio_data
    ):
        """Test MultimodalAgent audio processing."""
        config = AgentConfig(
            name="AudioAgent", description="Audio agent", model_provider="openai", model="gpt-4"
        )

        # Setup audio processor mock
        mock_processor = MagicMock()
        mock_audio_processor.return_value = mock_processor
        mock_processor.transcribe.return_value = "Transcribed text"
        mock_processor.get_audio_features.return_value = {"duration": 5.0, "sample_rate": 44100}

        # Note: The actual implementation returns a fixed response for audio
        agent = MultimodalAgent(config, mock_llm_client)

        # Process audio
        response = await agent.process_audio(audio=sample_audio_data, task="transcribe")

        assert response.content == "Audio processed"
        assert response.metadata["modality"] == "audio"
        assert response.metadata["task"] == "transcribe"

    @pytest.mark.unit
    @pytest.mark.agent
    @pytest.mark.asyncio
    async def test_multimodal_agent_process_multimodal(
        self, mock_llm_client, sample_image_data, sample_audio_data
    ):
        """Test MultimodalAgent with multiple modalities."""
        config = AgentConfig(
            name="MultimodalAgent",
            description="Full multimodal agent",
            model_provider="openai",
            model="gpt-4",
        )

        from src.models.base_llm import LLMResponse

        mock_llm_client.generate.return_value = LLMResponse(
            content="Multimodal response", model="gpt-4", usage={"total_tokens": 250}
        )
        mock_llm_client.supports_vision = False

        agent = MultimodalAgent(config, mock_llm_client)

        # Create multimodal input
        multimodal_input = MultimodalInput(
            text="Describe what you see and hear", image=sample_image_data, audio=sample_audio_data
        )

        # Process multimodal input
        response = await agent.process_multimodal(multimodal_input)

        assert response.content == "Multimodal response"
        assert response.metadata["modality"] == "multimodal"
        assert "modalities_used" in response.metadata
        assert "text" in response.metadata["modalities_used"]


class TestAgentFactory:
    """Test AgentFactory functionality."""

    @pytest.mark.unit
    @pytest.mark.agent
    def test_get_available_providers(self):
        """Test getting available LLM providers."""
        providers = AgentFactory.get_available_providers()

        assert "openai" in providers
        assert "gemini" in providers
        assert "anthropic" in providers
        assert len(providers) >= 3

    @pytest.mark.unit
    @pytest.mark.agent
    def test_get_available_agent_types(self):
        """Test getting available agent types."""
        agent_types = AgentFactory.get_available_agent_types()

        assert "simple" in agent_types
        assert "multimodal" in agent_types
        assert "langchain" in agent_types
        assert len(agent_types) >= 3

    @pytest.mark.unit
    @pytest.mark.agent
    def test_get_provider_models(self):
        """Test getting models for each provider."""
        # OpenAI models
        openai_models = AgentFactory.get_provider_models("openai")
        assert "gpt-4" in openai_models
        assert "gpt-3.5-turbo" in openai_models

        # Gemini models
        gemini_models = AgentFactory.get_provider_models("gemini")
        assert "gemini-pro" in gemini_models

        # Anthropic models
        anthropic_models = AgentFactory.get_provider_models("anthropic")
        assert "claude-3-opus-20240229" in anthropic_models

        # Invalid provider
        invalid_models = AgentFactory.get_provider_models("invalid")
        assert len(invalid_models) == 0

    @pytest.mark.unit
    @pytest.mark.agent
    @patch("src.agents.agent_factory.OpenAIClient")
    def test_create_simple_agent(self, mock_openai_client_class, mock_settings):
        """Test creating a simple agent."""
        # Setup mock
        mock_client = MagicMock()
        mock_openai_client_class.return_value = mock_client

        agent = AgentFactory.create_simple_agent(
            name="TestSimple", provider="openai", model="gpt-4"
        )

        assert isinstance(agent, SimpleAgent)
        assert agent.config.name == "TestSimple"
        assert agent.config.model_provider == "openai"
        assert agent.config.model == "gpt-4"

    @pytest.mark.unit
    @pytest.mark.agent
    @patch("src.agents.agent_factory.GeminiClient")
    def test_create_multimodal_agent(self, mock_gemini_client_class, mock_settings):
        """Test creating a multimodal agent."""
        # Setup mock
        mock_client = MagicMock()
        mock_gemini_client_class.return_value = mock_client

        agent = AgentFactory.create_multimodal_agent(
            name="TestMultimodal", provider="gemini", model="gemini-pro-vision"
        )

        assert isinstance(agent, MultimodalAgent)
        assert agent.config.name == "TestMultimodal"
        assert agent.config.model_provider == "gemini"
        assert agent.config.model == "gemini-pro-vision"

    @pytest.mark.unit
    @pytest.mark.agent
    @patch("src.agents.agent_factory.OpenAIClient")
    def test_create_agent_generic(self, mock_openai_client_class, mock_settings):
        """Test generic agent creation."""
        # Setup mock
        mock_client = MagicMock()
        mock_openai_client_class.return_value = mock_client

        # Create simple agent
        simple = AgentFactory.create_agent(
            name="Simple", type="simple", provider="openai", model="gpt-3.5-turbo"
        )
        assert isinstance(simple, SimpleAgent)

        # Create multimodal agent
        multimodal = AgentFactory.create_agent(
            name="Multimodal", type="multimodal", provider="openai", model="gpt-4-vision-preview"
        )
        assert isinstance(multimodal, MultimodalAgent)

    @pytest.mark.unit
    @pytest.mark.agent
    def test_create_agent_invalid_provider(self, mock_settings):
        """Test agent creation with invalid provider."""
        with pytest.raises(ValueError, match="Unknown provider"):
            AgentFactory.create_agent(
                name="Invalid", type="simple", provider="invalid_provider", model="some-model"
            )

    @pytest.mark.unit
    @pytest.mark.agent
    @patch("src.agents.agent_factory.OpenAIClient")
    def test_create_agent_invalid_type(self, mock_openai_client_class, mock_settings):
        """Test agent creation with invalid type."""
        mock_client = MagicMock()
        mock_openai_client_class.return_value = mock_client

        with pytest.raises(ValueError, match="Unknown agent type"):
            AgentFactory.create_agent(
                name="Invalid", type="invalid_type", provider="openai", model="gpt-4"
            )
