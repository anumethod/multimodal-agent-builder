"""Example Python client for the Multimodal Agent Builder API."""

import asyncio
import base64
from pathlib import Path
from typing import Optional

import httpx


class AgentAPIClient:
    """Client for interacting with the Agent Builder API."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the API client.

        Args:
            base_url: Base URL of the API
        """
        self.base_url = base_url
        self.client = httpx.AsyncClient()

    async def health_check(self) -> dict:
        """Check API health status."""
        response = await self.client.get(f"{self.base_url}/health")
        return response.json()

    async def list_providers(self) -> dict:
        """List available LLM providers."""
        response = await self.client.get(f"{self.base_url}/providers")
        return response.json()

    async def create_agent(
        self,
        name: str,
        agent_type: str = "multimodal",
        provider: str = "openai",
        model: Optional[str] = None,
        **kwargs,
    ) -> dict:
        """Create a new agent.

        Args:
            name: Agent name
            agent_type: Type of agent
            provider: LLM provider
            model: Model name
            **kwargs: Additional configuration

        Returns:
            Agent information
        """
        data = {"name": name, "type": agent_type, "provider": provider, "model": model, **kwargs}
        response = await self.client.post(f"{self.base_url}/agents", json=data)
        return response.json()

    async def list_agents(self) -> list:
        """List all agents."""
        response = await self.client.get(f"{self.base_url}/agents")
        return response.json()

    async def get_agent(self, agent_id: str) -> dict:
        """Get agent information.

        Args:
            agent_id: Agent ID

        Returns:
            Agent information
        """
        response = await self.client.get(f"{self.base_url}/agents/{agent_id}")
        return response.json()

    async def chat(self, agent_id: str, message: str) -> dict:
        """Chat with an agent.

        Args:
            agent_id: Agent ID
            message: User message

        Returns:
            Agent response
        """
        data = {"message": message}
        response = await self.client.post(f"{self.base_url}/agents/{agent_id}/chat", json=data)
        return response.json()

    async def process_image(
        self, agent_id: str, image_path: str, prompt: str = "What's in this image?"
    ) -> dict:
        """Process an image with the agent.

        Args:
            agent_id: Agent ID
            image_path: Path to image file
            prompt: Text prompt

        Returns:
            Agent response
        """
        with open(image_path, "rb") as f:
            files = {"image": f}
            data = {"prompt": prompt}
            response = await self.client.post(
                f"{self.base_url}/agents/{agent_id}/process-image", files=files, data=data
            )
        return response.json()

    async def delete_agent(self, agent_id: str) -> dict:
        """Delete an agent.

        Args:
            agent_id: Agent ID

        Returns:
            Deletion confirmation
        """
        response = await self.client.delete(f"{self.base_url}/agents/{agent_id}")
        return response.json()

    async def quick_chat(self, provider: str, message: str) -> dict:
        """Quick chat with a specific provider.

        Args:
            provider: Provider name (gpt4, gemini, claude)
            message: User message

        Returns:
            Agent response
        """
        data = {"message": message}
        response = await self.client.post(f"{self.base_url}/quick-start/chat-{provider}", data=data)
        return response.json()

    async def close(self):
        """Close the client."""
        await self.client.aclose()


async def example_basic_usage():
    """Example of basic API usage."""
    client = AgentAPIClient()

    try:
        # Check health
        print("🏥 Health Check:")
        health = await client.health_check()
        print(f"  Status: {health['status']}")
        print(f"  Version: {health['version']}")

        # List providers
        print("\n📋 Available Providers:")
        providers = await client.list_providers()
        for provider, details in providers["details"].items():
            configured = "✅" if details["configured"] else "❌"
            print(f"  {configured} {provider}: {len(details['models'])} models")

        # Create an agent
        print("\n🤖 Creating Agent...")
        agent = await client.create_agent(
            name="Example Assistant",
            agent_type="multimodal",
            provider="openai",
            model="gpt-4-turbo-preview",
            description="A helpful multimodal assistant",
            system_prompt="You are a helpful and friendly AI assistant.",
        )
        print(f"  Created: {agent['name']} (ID: {agent['id']})")

        # Chat with the agent
        print("\n💬 Chatting with Agent...")
        response = await client.chat(agent["id"], "Hello! Can you tell me a fun fact about AI?")
        print(f"  Response: {response['content']}")

        # List all agents
        print("\n📑 All Agents:")
        agents = await client.list_agents()
        for a in agents:
            print(f"  - {a['name']} ({a['id']})")

        # Clean up
        print("\n🧹 Cleaning up...")
        await client.delete_agent(agent["id"])
        print("  Agent deleted")

    finally:
        await client.close()


async def example_multimodal():
    """Example of multimodal processing."""
    client = AgentAPIClient()

    try:
        # Create a multimodal agent
        print("🎨 Creating Multimodal Agent...")
        agent = await client.create_agent(
            name="Vision Expert",
            agent_type="multimodal",
            provider="openai",
            model="gpt-4-turbo",
            enable_vision=True,
        )
        print(f"  Created: {agent['name']}")

        # Process an image (if you have one)
        image_path = "example_image.jpg"
        if Path(image_path).exists():
            print("\n🖼️ Processing Image...")
            response = await client.process_image(
                agent["id"], image_path, "Describe this image in detail"
            )
            print(f"  Analysis: {response['content']}")
        else:
            print("\n  No example image found")

        # Clean up
        await client.delete_agent(agent["id"])

    finally:
        await client.close()


async def example_quick_start():
    """Example of quick start endpoints."""
    client = AgentAPIClient()

    try:
        print("⚡ Quick Start Examples\n")

        # Quick chat with GPT-4
        print("🤖 GPT-4:")
        response = await client.quick_chat("gpt4", "What is quantum computing?")
        print(f"  {response['content'][:200]}...\n")

        # Quick chat with Gemini
        print("✨ Gemini:")
        response = await client.quick_chat("gemini", "Explain machine learning")
        print(f"  {response['content'][:200]}...\n")

        # Quick chat with Claude
        print("🎭 Claude:")
        response = await client.quick_chat("claude", "What is artificial intelligence?")
        print(f"  {response['content'][:200]}...\n")

    finally:
        await client.close()


async def example_streaming():
    """Example of streaming responses."""
    async with httpx.AsyncClient() as client:
        # Create agent first
        agent_data = {"name": "Streaming Assistant", "type": "multimodal", "provider": "openai"}
        agent_response = await client.post("http://localhost:8000/agents", json=agent_data)
        agent = agent_response.json()

        # Stream chat response
        print("📡 Streaming Response:")
        async with client.stream(
            "POST",
            f"http://localhost:8000/agents/{agent['id']}/chat",
            json={"message": "Write a short poem about AI", "stream": True},
        ) as response:
            async for chunk in response.aiter_text():
                print(chunk, end="", flush=True)

        # Clean up
        await client.delete(f"http://localhost:8000/agents/{agent['id']}")


def main():
    """Run examples."""
    print("🚀 Multimodal Agent Builder API Examples\n")
    print("=" * 50)

    # Run examples
    asyncio.run(example_basic_usage())
    print("\n" + "=" * 50)
    asyncio.run(example_quick_start())

    # Uncomment to run additional examples:
    # asyncio.run(example_multimodal())
    # asyncio.run(example_streaming())


if __name__ == "__main__":
    main()
