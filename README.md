# Multimodal Agent Builder

## Troubleshooting & Developer Notes

- **Use Bash for Shell Scripts:** If you see “unexpected operator” or “parse error,” always run scripts with `bash script.sh` (not `sh script.sh` or in zsh).
- **Formatting and Linting:** After cloning, run `npm run prettier` and `npm run lint:fix` to fix common JSX, import, and whitespace issues.
- **Editor/LSP Setup:** TypeScript warnings may appear if your environment uses a different TS or ESLint version; run `npm install` and use VSCode for best results.
- **JSX Nesting:** Avoid placing `<a>` inside custom `<Link>`. If needed, use `<span>` or your own `<AppLink>` instead to avoid React warnings.
- **Dependencies:** If some UI icons or components are missing, check your `package.json`. Run `npm install` to ensure all dependencies are present.
- **TypeScript Strictness:** Some warnings may appear if strict options are enabled (see `tsconfig.json`). They don't break runtime behavior but should be resolved for clarity.
- **String Matching in CLI Edits:** Automated editing tools require exact matches including whitespace; copy relevant code and check file content before using CLI replacements.

See also: KNOWN_ISSUES.md (if present) for current edge cases and gotchas.

A powerful and flexible framework for building multimodal AI agents using state-of-the-art language models including OpenAI GPT-4, Google Gemini-2.5, and Anthropic Claude.

## 🚀 Features

- **Multi-LLM Support**: Seamlessly integrate with OpenAI GPT-4, Google Gemini-2.5, and Anthropic Claude
- **Multimodal Capabilities**: Process text, images, and audio inputs
- **Agent Orchestration**: Build complex agent workflows using LangChain
- **REST API**: FastAPI-based endpoints for easy integration
- **Modular Architecture**: Easily extend with new LLMs or agent types
- **Type Safety**: Full type hints with Pydantic validation
- **Async Support**: Built-in async/await support for high performance

## 📋 Prerequisites

- Python 3.10 or higher
- API keys for:
  - OpenAI
  - Google Gemini
  - Anthropic (Claude)

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/anumethod/multimodal-agent-builder.git
cd multimodal-agent-builder
```

### 2. Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -e .
```

For development dependencies:

```bash
pip install -e ".[dev]"
```

### 4. Set up environment variables

Copy the example environment file and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
- `OPENAI_API_KEY`: Your OpenAI API key
- `GEMINI_API_KEY`: Your Google Gemini API key
- `ANTHROPIC_API_KEY`: Your Anthropic API key

## 🚀 Quick Start

### Running the API Server

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

### Basic Usage Example

```python
from src.models.openai_client import OpenAIClient
from src.models.gemini_client import GeminiClient
from src.models.claude_client import ClaudeClient
from src.agents.multimodal_agent import MultimodalAgent

# Initialize LLM clients
openai_client = OpenAIClient()
gemini_client = GeminiClient()
claude_client = ClaudeClient()

# Create a multimodal agent
agent = MultimodalAgent(
    llm_client=openai_client,
    name="Assistant",
    description="A helpful multimodal assistant"
)

# Process text
response = await agent.process_text("What is the weather like today?")

# Process image
response = await agent.process_image("path/to/image.jpg", "What's in this image?")

# Process audio
response = await agent.process_audio("path/to/audio.mp3", "Transcribe this audio")
```

## 📁 Project Structure

```
multimodal-agent-builder/
├── src/
│   ├── agents/          # Agent implementations
│   │   ├── base_agent.py
│   │   └── multimodal_agent.py
│   ├── models/          # LLM client implementations
│   │   ├── openai_client.py
│   │   ├── gemini_client.py
│   │   └── claude_client.py
│   ├── utils/           # Utility functions
│   │   ├── image_utils.py
│   │   ├── audio_utils.py
│   │   └── logging.py
│   └── main.py          # FastAPI application
├── config/
│   └── config.py        # Configuration management
├── tests/               # Test suite
│   ├── test_config.py
│   ├── test_models.py
│   └── test_agents.py
├── .env.example         # Environment variables template
├── .gitignore
├── pyproject.toml       # Project metadata and dependencies
└── README.md
```

## 🧪 Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=src --cov-report=html
```

## 📝 API Endpoints

### Create Agent
```http
POST /agents
Content-Type: application/json

{
  "name": "MyAgent",
  "model": "gpt-4",
  "description": "A helpful assistant",
  "temperature": 0.7
}
```

### Invoke Agent
```http
POST /agents/{agent_id}/invoke
Content-Type: application/json

{
  "input": "Hello, how can you help me?",
  "type": "text"
}
```

### Upload and Process Image
```http
POST /agents/{agent_id}/process-image
Content-Type: multipart/form-data

image: [file]
prompt: "What's in this image?"
```

### Upload and Process Audio
```http
POST /agents/{agent_id}/process-audio
Content-Type: multipart/form-data

audio: [file]
prompt: "Transcribe this audio"
```

## 🔧 Configuration

Configuration is managed through environment variables and the `config/config.py` module. Key settings include:

- **API Keys**: Required for each LLM provider
- **Model Settings**: Temperature, max tokens, etc.
- **Rate Limiting**: Configurable request limits
- **File Upload**: Max file size and allowed types
- **Logging**: Log level and format

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4
- Google for Gemini
- Anthropic for Claude
- LangChain community for the orchestration framework

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Note**: This project is in active development. Features and APIs may change.
