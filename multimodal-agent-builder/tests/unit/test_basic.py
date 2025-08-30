"""Basic tests to verify setup and core components."""

import pytest
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class TestBasicSetup:
    """Test basic project setup."""

    @pytest.mark.unit
    def test_project_structure(self):
        """Test that project structure exists."""
        assert project_root.exists()
        assert (project_root / "src").exists()
        assert (project_root / "config").exists()
        assert (project_root / "tests").exists()

    @pytest.mark.unit
    def test_imports(self):
        """Test that basic imports work."""
        # Test config import
        from config.config import Settings

        settings = Settings()
        assert settings is not None

        # Test agent imports
        from src.agents.base_agent import BaseAgent, AgentConfig

        assert BaseAgent is not None
        assert AgentConfig is not None

        # Test model imports
        from src.models.base_llm import BaseLLMClient

        assert BaseLLMClient is not None

    @pytest.mark.unit
    def test_agent_config_creation(self):
        """Test AgentConfig creation."""
        from src.agents.base_agent import AgentConfig

        config = AgentConfig(
            name="TestAgent", description="A test agent", model_provider="openai", model="gpt-4"
        )

        assert config.name == "TestAgent"
        assert config.description == "A test agent"
        assert config.model_provider == "openai"
        assert config.model == "gpt-4"

    @pytest.mark.unit
    def test_settings_defaults(self):
        """Test Settings default values."""
        from config.config import Settings

        settings = Settings()
        assert settings.app_name == "Multimodal Agent Builder"
        assert settings.app_version == "0.1.0"
        assert settings.app_port == 8000
        assert settings.app_host == "0.0.0.0"

    @pytest.mark.unit
    def test_utils_imports(self):
        """Test utility imports."""
        # Test logging utils
        from src.utils.logging_utils import logger, setup_logger

        assert logger is not None
        assert setup_logger is not None

        # Test audio utils
        from src.utils.audio_utils import AudioProcessor

        assert AudioProcessor is not None

        # Test training utils
        from src.utils.training_utils import AdaptiveTrainingManager

        assert AdaptiveTrainingManager is not None

    @pytest.mark.unit
    def test_api_imports(self):
        """Test API imports."""
        from src.main import app

        assert app is not None

        from src.api.training_endpoints import router

        assert router is not None

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_basic_async(self):
        """Test basic async functionality."""
        import asyncio

        async def simple_async():
            await asyncio.sleep(0.001)
            return "success"

        result = await simple_async()
        assert result == "success"
