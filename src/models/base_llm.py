"""Base LLM client abstract class."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union

import numpy as np
from PIL import Image


class MessageRole(Enum):
    """Message roles for conversation."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"


@dataclass
class Message:
    """Represents a message in a conversation."""
    role: MessageRole
    content: Union[str, List[Dict[str, Any]]]
    name: Optional[str] = None
    function_call: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        data = {
            "role": self.role.value,
            "content": self.content
        }
        if self.name:
            data["name"] = self.name
        if self.function_call:
            data["function_call"] = self.function_call
        return data


@dataclass
class LLMResponse:
    """Standardized LLM response."""
    content: str
    model: str
    usage: Dict[str, int]
    finish_reason: Optional[str] = None
    function_call: Optional[Dict[str, Any]] = None
    raw_response: Optional[Any] = None


class BaseLLMClient(ABC):
    """Abstract base class for LLM clients."""
    
    def __init__(
        self,
        api_key: str,
        model: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs
    ):
        """Initialize the LLM client.
        
        Args:
            api_key: API key for the service
            model: Model identifier
            max_tokens: Maximum tokens to generate
            temperature: Temperature for sampling
            **kwargs: Additional provider-specific arguments
        """
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.extra_params = kwargs
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate configuration."""
        if not self.api_key:
            raise ValueError(f"API key is required for {self.__class__.__name__}")
        if not self.model:
            raise ValueError(f"Model name is required for {self.__class__.__name__}")
        if not 0 <= self.temperature <= 2:
            raise ValueError(f"Temperature must be between 0 and 2, got {self.temperature}")
        if self.max_tokens <= 0:
            raise ValueError(f"max_tokens must be positive, got {self.max_tokens}")
    
    @abstractmethod
    async def generate(
        self,
        messages: List[Message],
        **kwargs
    ) -> LLMResponse:
        """Generate a response from the LLM.
        
        Args:
            messages: List of messages in the conversation
            **kwargs: Additional generation parameters
            
        Returns:
            LLMResponse object
        """
        pass
    
    @abstractmethod
    async def generate_stream(
        self,
        messages: List[Message],
        **kwargs
    ):
        """Generate a streaming response from the LLM.
        
        Args:
            messages: List of messages in the conversation
            **kwargs: Additional generation parameters
            
        Yields:
            Partial response chunks
        """
        pass
    
    @abstractmethod
    async def generate_with_image(
        self,
        prompt: str,
        image: Union[str, bytes, Image.Image, np.ndarray],
        **kwargs
    ) -> LLMResponse:
        """Generate a response based on text and image input.
        
        Args:
            prompt: Text prompt
            image: Image input (path, bytes, PIL Image, or numpy array)
            **kwargs: Additional generation parameters
            
        Returns:
            LLMResponse object
        """
        pass
    
    @abstractmethod
    async def generate_embeddings(
        self,
        text: Union[str, List[str]],
        **kwargs
    ) -> Union[List[float], List[List[float]]]:
        """Generate embeddings for the given text.
        
        Args:
            text: Single text or list of texts
            **kwargs: Additional parameters
            
        Returns:
            Embeddings as list of floats or list of lists
        """
        pass
    
    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in a text.
        
        Args:
            text: Text to count tokens for
            
        Returns:
            Number of tokens
        """
        pass
    
    @property
    @abstractmethod
    def supports_functions(self) -> bool:
        """Check if the model supports function calling."""
        pass
    
    @property
    @abstractmethod
    def supports_vision(self) -> bool:
        """Check if the model supports vision inputs."""
        pass
    
    @property
    @abstractmethod
    def supports_streaming(self) -> bool:
        """Check if the model supports streaming responses."""
        pass
    
    @property
    @abstractmethod
    def max_context_length(self) -> int:
        """Get the maximum context length for the model."""
        pass
    
    def prepare_messages(
        self,
        messages: List[Union[Message, Dict[str, Any]]],
        system_prompt: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Prepare messages for the API call.
        
        Args:
            messages: List of Message objects
            system_prompt: Optional system prompt to prepend
            
        Returns:
            List of message dictionaries
        """
        prepared = []
        
        if system_prompt:
            prepared.append({
                "role": MessageRole.SYSTEM.value,
                "content": system_prompt
            })
        
        for msg in messages:
            # Accept either Message objects or raw dicts
            if isinstance(msg, Message):
                prepared.append(msg.to_dict())
            elif isinstance(msg, dict):
                # Basic validation and normalization
                role = msg.get("role")
                content = msg.get("content")
                if isinstance(role, MessageRole):
                    role = role.value
                prepared.append({
                    "role": role,
                    "content": content,
                    **{k: v for k, v in msg.items() if k not in {"role", "content"}},
                })
            else:
                # Fallback to string content as user message
                prepared.append({"role": MessageRole.USER.value, "content": str(msg)})
        
        return prepared
    
    def __repr__(self) -> str:
        """String representation of the client."""
        return f"{self.__class__.__name__}(model='{self.model}')"
