"""OpenAI GPT-4 client implementation."""

import base64
import io
from typing import Any, AsyncGenerator, Dict, List, Optional, Union

import numpy as np
import openai
import tiktoken

# Use attribute access on the module so external patches work reliably
from PIL import Image

from config.config import settings
from src.models.base_llm import BaseLLMClient, LLMResponse, Message, MessageRole


class OpenAIClient(BaseLLMClient):
    """OpenAI GPT-4 client implementation."""

    # Model capabilities mapping
    MODEL_CAPABILITIES = {
        "gpt-4-turbo-preview": {
            "vision": True,
            "functions": True,
            "streaming": True,
            "max_context": 128000,
            "max_output": 4096,
        },
        "gpt-4-turbo": {
            "vision": True,
            "functions": True,
            "streaming": True,
            "max_context": 128000,
            "max_output": 4096,
        },
        "gpt-4": {
            "vision": False,
            "functions": True,
            "streaming": True,
            "max_context": 8192,
            "max_output": 4096,
        },
        "gpt-4-32k": {
            "vision": False,
            "functions": True,
            "streaming": True,
            "max_context": 32768,
            "max_output": 4096,
        },
        "gpt-3.5-turbo": {
            "vision": False,
            "functions": True,
            "streaming": True,
            "max_context": 16384,
            "max_output": 4096,
        },
    }

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        organization: Optional[str] = None,
        **kwargs,
    ):
        """Initialize OpenAI client.

        Args:
            api_key: OpenAI API key (defaults to settings)
            model: Model name (defaults to settings)
            max_tokens: Maximum tokens to generate
            temperature: Temperature for sampling
            organization: Optional organization ID
            **kwargs: Additional parameters
        """
        # Use settings as defaults
        config = settings.get_llm_config("openai")
        api_key = api_key or config["api_key"]
        model = model or config["model"]
        max_tokens = max_tokens or config["max_tokens"]
        temperature = temperature if temperature is not None else config["temperature"]

        super().__init__(api_key, model, max_tokens, temperature, **kwargs)

        # Initialize OpenAI client
        self.client = openai.AsyncOpenAI(api_key=self.api_key, organization=organization)

        # Initialize tokenizer for the model
        try:
            self.tokenizer = tiktoken.encoding_for_model(self.model)
        except KeyError:
            # Fallback to cl100k_base encoding for newer models
            self.tokenizer = tiktoken.get_encoding("cl100k_base")

    async def generate(
        self,
        messages: List[Message],
        functions: Optional[List[Dict[str, Any]]] = None,
        function_call: Optional[Union[str, Dict[str, Any]]] = None,
        **kwargs,
    ) -> LLMResponse:
        """Generate a response from OpenAI GPT-4.

        Args:
            messages: List of messages in the conversation
            functions: Optional list of function definitions
            function_call: Optional function calling behavior
            **kwargs: Additional parameters

        Returns:
            LLMResponse object
        """
        # Prepare messages
        prepared_messages = self.prepare_messages(messages)

        # Build request parameters
        params = {
            "model": self.model,
            "messages": prepared_messages,
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "temperature": kwargs.get("temperature", self.temperature),
            "top_p": kwargs.get("top_p", 1.0),
            "frequency_penalty": kwargs.get("frequency_penalty", 0.0),
            "presence_penalty": kwargs.get("presence_penalty", 0.0),
        }

        # Add function calling if supported and provided
        if self.supports_functions and functions:
            params["functions"] = functions
            if function_call is not None:
                params["function_call"] = function_call

        # Make API call
        response = await self.client.chat.completions.create(**params)

        # Extract response data
        choice = response.choices[0]
        message = choice.message

        return LLMResponse(
            content=message.content or "",
            model=response.model,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
            finish_reason=choice.finish_reason,
            function_call=message.function_call if hasattr(message, "function_call") else None,
            raw_response=response,
        )

    async def generate_stream(self, messages: List[Message], **kwargs) -> AsyncGenerator[str, None]:
        """Generate a streaming response from OpenAI.

        Args:
            messages: List of messages
            **kwargs: Additional parameters

        Yields:
            Response chunks
        """
        prepared_messages = self.prepare_messages(messages)

        params = {
            "model": self.model,
            "messages": prepared_messages,
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "temperature": kwargs.get("temperature", self.temperature),
            "stream": True,
        }

        stream = await self.client.chat.completions.create(**params)

        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    async def generate_with_image(
        self, prompt: str, image: Union[str, bytes, Image.Image, np.ndarray], **kwargs
    ) -> LLMResponse:
        """Generate a response based on text and image input.

        Args:
            prompt: Text prompt
            image: Image input
            **kwargs: Additional parameters

        Returns:
            LLMResponse object
        """
        if not self.supports_vision:
            raise ValueError(f"Model {self.model} does not support vision inputs")

        # Convert image to base64
        image_base64 = self._process_image(image)

        # Create message with image
        messages = [
            Message(
                role=MessageRole.USER,
                content=[
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
                    },
                ],
            )
        ]

        return await self.generate(messages, **kwargs)

    async def generate_embeddings(
        self, text: Union[str, List[str]], model: str = "text-embedding-3-small", **kwargs
    ) -> Union[List[float], List[List[float]]]:
        """Generate embeddings for text.

        Args:
            text: Text or list of texts
            model: Embedding model to use
            **kwargs: Additional parameters

        Returns:
            Embeddings
        """
        is_single = isinstance(text, str)
        input_text = [text] if is_single else text

        response = await self.client.embeddings.create(model=model, input=input_text, **kwargs)

        embeddings = [item.embedding for item in response.data]

        return embeddings[0] if is_single else embeddings

    def count_tokens(self, text: str) -> int:
        """Count tokens in text.

        Args:
            text: Text to count tokens for

        Returns:
            Number of tokens
        """
        return len(self.tokenizer.encode(text))

    def _process_image(self, image: Union[str, bytes, Image.Image, np.ndarray]) -> str:
        """Process image to base64 string.

        Args:
            image: Image in various formats

        Returns:
            Base64 encoded image string
        """
        if isinstance(image, str):
            # If it's a file path
            with open(image, "rb") as f:
                image_bytes = f.read()
        elif isinstance(image, bytes):
            image_bytes = image
        elif isinstance(image, Image.Image):
            # Convert PIL Image to bytes
            buffer = io.BytesIO()
            image.save(buffer, format="JPEG")
            image_bytes = buffer.getvalue()
        elif isinstance(image, np.ndarray):
            # Convert numpy array to PIL Image then to bytes
            pil_image = Image.fromarray(image)
            buffer = io.BytesIO()
            pil_image.save(buffer, format="JPEG")
            image_bytes = buffer.getvalue()
        else:
            raise ValueError(f"Unsupported image type: {type(image)}")

        return base64.b64encode(image_bytes).decode("utf-8")

    @property
    def supports_functions(self) -> bool:
        """Check if model supports function calling."""
        return self.MODEL_CAPABILITIES.get(self.model, {"functions": False})["functions"]

    @property
    def supports_vision(self) -> bool:
        """Check if model supports vision inputs."""
        return self.MODEL_CAPABILITIES.get(self.model, {"vision": False})["vision"]

    @property
    def supports_streaming(self) -> bool:
        """Check if model supports streaming."""
        return self.MODEL_CAPABILITIES.get(self.model, {"streaming": True})["streaming"]

    @property
    def max_context_length(self) -> int:
        """Get maximum context length."""
        return self.MODEL_CAPABILITIES.get(self.model, {"max_context": 8192})["max_context"]
