#!/bin/bash

# Multimodal Agent Builder API - cURL Examples
# ============================================

API_BASE="http://localhost:8000"

echo "🚀 Multimodal Agent Builder - cURL Examples"
echo "==========================================="
echo ""

# Health Check
echo "1️⃣ Health Check"
echo "---------------"
curl -X GET "$API_BASE/health" \
  -H "Content-Type: application/json" | python3 -m json.tool
echo ""

# List Providers
echo "2️⃣ List Available Providers"
echo "---------------------------"
curl -X GET "$API_BASE/providers" \
  -H "Content-Type: application/json" | python3 -m json.tool
echo ""

# List Agent Types
echo "3️⃣ List Agent Types"
echo "-------------------"
curl -X GET "$API_BASE/agent-types" \
  -H "Content-Type: application/json" | python3 -m json.tool
echo ""

# Create an Agent
echo "4️⃣ Create a New Agent"
echo "---------------------"
AGENT_RESPONSE=$(curl -X POST "$API_BASE/agents" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Assistant",
    "type": "multimodal",
    "provider": "openai",
    "model": "gpt-4-turbo-preview",
    "description": "A test multimodal assistant",
    "system_prompt": "You are a helpful AI assistant.",
    "temperature": 0.7,
    "max_tokens": 2048,
    "enable_memory": true,
    "enable_tools": true,
    "enable_vision": true,
    "enable_audio": true
  }')

echo "$AGENT_RESPONSE" | python3 -m json.tool

# Extract agent ID
AGENT_ID=$(echo "$AGENT_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo "Created agent with ID: $AGENT_ID"
echo ""

# List All Agents
echo "5️⃣ List All Agents"
echo "------------------"
curl -X GET "$API_BASE/agents" \
  -H "Content-Type: application/json" | python3 -m json.tool
echo ""

# Get Agent Info
echo "6️⃣ Get Agent Information"
echo "------------------------"
curl -X GET "$API_BASE/agents/$AGENT_ID" \
  -H "Content-Type: application/json" | python3 -m json.tool
echo ""

# Chat with Agent
echo "7️⃣ Chat with Agent"
echo "------------------"
curl -X POST "$API_BASE/agents/$AGENT_ID/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! Tell me a fun fact about artificial intelligence.",
    "stream": false
  }' | python3 -m json.tool
echo ""

# Invoke Agent (Think-Act-Observe)
echo "8️⃣ Invoke Agent with Custom Input"
echo "---------------------------------"
curl -X POST "$API_BASE/agents/$AGENT_ID/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Analyze the impact of AI on society",
    "kwargs": {}
  }' | python3 -m json.tool
echo ""

# Process Image (requires an actual image file)
echo "9️⃣ Process Image (Example)"
echo "--------------------------"
echo "To process an image, use:"
echo "curl -X POST \"$API_BASE/agents/$AGENT_ID/process-image\" \\"
echo "  -F \"image=@path/to/your/image.jpg\" \\"
echo "  -F \"prompt=What's in this image?\""
echo ""

# Process Multimodal
echo "🔟 Process Multimodal Input (Example)"
echo "------------------------------------"
echo "To process multimodal input:"
echo "curl -X POST \"$API_BASE/agents/$AGENT_ID/process-multimodal\" \\"
echo "  -F \"text=Describe and analyze this content\" \\"
echo "  -F \"image=@path/to/image.jpg\" \\"
echo "  -F \"audio=@path/to/audio.mp3\""
echo ""

# Get Agent Tools
echo "1️⃣1️⃣ Get Agent Tools"
echo "--------------------"
curl -X GET "$API_BASE/agents/$AGENT_ID/tools" \
  -H "Content-Type: application/json" | python3 -m json.tool
echo ""

# Clear Agent Memory
echo "1️⃣2️⃣ Clear Agent Memory"
echo "-----------------------"
curl -X POST "$API_BASE/agents/$AGENT_ID/clear-memory" \
  -H "Content-Type: application/json" | python3 -m json.tool
echo ""

# Quick Start Examples
echo "1️⃣3️⃣ Quick Start - Chat with GPT-4"
echo "-----------------------------------"
curl -X POST "$API_BASE/quick-start/chat-gpt4" \
  -F "message=What is the meaning of life?" | python3 -m json.tool
echo ""

echo "1️⃣4️⃣ Quick Start - Chat with Gemini"
echo "------------------------------------"
curl -X POST "$API_BASE/quick-start/chat-gemini" \
  -F "message=Explain quantum computing in simple terms" | python3 -m json.tool
echo ""

echo "1️⃣5️⃣ Quick Start - Chat with Claude"
echo "------------------------------------"
curl -X POST "$API_BASE/quick-start/chat-claude" \
  -F "message=Write a haiku about technology" | python3 -m json.tool
echo ""

# Delete Agent
echo "1️⃣6️⃣ Delete Agent"
echo "-----------------"
curl -X DELETE "$API_BASE/agents/$AGENT_ID" \
  -H "Content-Type: application/json" | python3 -m json.tool
echo ""

echo "✅ Examples Complete!"
echo ""
echo "📚 Additional Resources:"
echo "  - API Documentation: $API_BASE/docs"
echo "  - ReDoc: $API_BASE/redoc"
echo "  - OpenAPI Schema: $API_BASE/openapi.json"
