"""
Backend API Server for ChatBot Plugin

Provides REST APIs for:
- RAG queries
- MCP tool execution
- n8n integration
- Enhanced chatbot capabilities
"""

import logging
from typing import Dict, Any, Optional
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

logger = logging.getLogger('mkdocs.plugins.chatbot.api')


def create_app(rag_manager, mcp_tools_manager, config: Dict[str, Any]) -> Flask:
    """
    Create Flask app for chatbot API.

    Args:
        rag_manager: RAGManager instance
        mcp_tools_manager: MCPToolsManager instance
        config: Plugin configuration

    Returns:
        Flask app
    """
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    # Store managers in app context
    app.rag_manager = rag_manager
    app.mcp_tools_manager = mcp_tools_manager
    app.config_data = config

    @app.route('/health', methods=['GET'])
    def health():
        """Health check endpoint."""
        return jsonify({
            'status': 'ok',
            'rag_available': rag_manager.is_available() if rag_manager else False,
            'mcp_tools_available': mcp_tools_manager.is_available() if mcp_tools_manager else False
        })

    @app.route('/api/query', methods=['POST'])
    def query():
        """
        Query endpoint for enhanced chat with RAG.

        Request body:
        {
            "message": "user message",
            "page_context": {"title": "...", "url": "...", "content": "..."},
            "conversation_history": [...]
        }

        Response:
        {
            "response": "assistant response",
            "sources": [...],  # if RAG is used
            "tool_calls": [...]  # if tools were used
        }
        """
        try:
            data = request.json
            message = data.get('message', '')
            page_context = data.get('page_context', {})
            conversation_history = data.get('conversation_history', [])

            if not message:
                return jsonify({'error': 'Message is required'}), 400

            # Query RAG if available
            rag_sources = []
            if app.rag_manager and app.rag_manager.is_available():
                rag_sources = app.rag_manager.query(message, page_context)
                logger.info(f"Retrieved {len(rag_sources)} sources from RAG")

            # Build enhanced context
            context_parts = []

            # Add RAG sources
            if rag_sources:
                context_parts.append("**Relevant Documentation:**\n")
                for i, source in enumerate(rag_sources[:3], 1):  # Top 3 sources
                    context_parts.append(f"{i}. {source['content']}")
                    if metadata := source.get('metadata'):
                        # Add source file information
                        source_info = []
                        if file_path := metadata.get('file_path'):
                            source_info.append(f"File: {file_path}")
                        if file_type := metadata.get('file_type'):
                            source_info.append(f"Type: {file_type}")
                        if md5_hash := metadata.get('file_md5'):
                            source_info.append(f"MD5: {md5_hash}")
                        if git_commit := metadata.get('git_commit'):
                            source_info.append(f"Git: {git_commit}")
                        if git_tag := metadata.get('git_tag'):
                            source_info.append(f"Tag: {git_tag}")
                        elif git_nearest_tag := metadata.get('git_nearest_tag'):
                            source_info.append(f"Nearest Tag: {git_nearest_tag}")
                        if git_branch := metadata.get('git_branch'):
                            source_info.append(f"Branch: {git_branch}")
                        if title := metadata.get('title'):
                            source_info.append(f"Title: {title}")

                        if source_info:
                            context_parts.append(f"   Source: {', '.join(source_info)}")
                context_parts.append("")

            # Add current page context
            if page_context.get('content'):
                context_parts.append(f"**Current Page:** {page_context.get('title', 'Unknown')}")
                context_parts.append(page_context.get('content', '')[:1000])  # Limit context
                context_parts.append("")

            enhanced_context = "\n".join(context_parts)

            # Check if using n8n
            if app.config_data.get('enable_n8n') and app.config_data.get('n8n_webhook_url'):
                response_text = call_n8n(
                    app.config_data,
                    message,
                    enhanced_context,
                    conversation_history
                )
            else:
                # Use OpenAI API (or compatible)
                response_text = call_llm(
                    app.config_data,
                    message,
                    enhanced_context,
                    conversation_history
                )

            # Return response
            result = {
                'response': response_text,
                'sources': [
                    {
                        'content': s['content'][:200] + '...' if len(s['content']) > 200 else s['content'],
                        'metadata': s.get('metadata', {}),
                        'score': s.get('score', 0)
                    }
                    for s in rag_sources[:3]
                ],
                'tool_calls': []
            }

            return jsonify(result)

        except Exception as e:
            logger.error(f"Query error: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/tools/execute', methods=['POST'])
    def execute_tool():
        """
        Execute MCP tool.

        Request body:
        {
            "tool_name": "tool name",
            "arguments": {...}
        }

        Response:
        {
            "success": true/false,
            "result": {...}
        }
        """
        try:
            if not app.mcp_tools_manager or not app.mcp_tools_manager.is_available():
                return jsonify({'error': 'MCP tools not available'}), 503

            data = request.json
            tool_name = data.get('tool_name', '')
            arguments = data.get('arguments', {})

            if not tool_name:
                return jsonify({'error': 'Tool name is required'}), 400

            # Execute tool
            result = app.mcp_tools_manager.execute_tool(tool_name, arguments)

            return jsonify(result)

        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/tools/list', methods=['GET'])
    def list_tools():
        """
        List available MCP tools.

        Response:
        {
            "tools": [...]
        }
        """
        try:
            if not app.mcp_tools_manager or not app.mcp_tools_manager.is_available():
                return jsonify({'tools': []})

            tools = app.mcp_tools_manager.get_tool_schemas()
            return jsonify({'tools': tools})

        except Exception as e:
            logger.error(f"List tools error: {e}")
            return jsonify({'error': str(e)}), 500

    return app


def call_llm(config: Dict[str, Any], message: str, context: str, history: list) -> str:
    """
    Call LLM API (OpenAI or compatible).

    Args:
        config: Plugin configuration
        message: User message
        context: Enhanced context from RAG
        history: Conversation history

    Returns:
        LLM response text
    """
    api_base_url = config.get('api_base_url', 'https://api.openai.com/v1')
    api_key = config.get('api_key', '')
    model = config.get('model', 'gpt-4o-mini')
    system_prompt = config.get('system_prompt', '')

    # Build messages
    messages = [
        {
            'role': 'system',
            'content': f"{system_prompt}\n\n{context}" if context else system_prompt
        }
    ]

    # Add history
    messages.extend(history)

    # Add current message
    messages.append({
        'role': 'user',
        'content': message
    })

    # Call API
    headers = {
        'Content-Type': 'application/json'
    }
    if api_key:
        headers['Authorization'] = f"Bearer {api_key}"

    response = requests.post(
        f"{api_base_url}/chat/completions",
        headers=headers,
        json={
            'model': model,
            'messages': messages,
            'temperature': config.get('temperature', 0.7),
            'max_tokens': config.get('max_tokens', 1000)
        },
        timeout=60
    )

    response.raise_for_status()
    data = response.json()

    return data['choices'][0]['message']['content']


def call_n8n(config: Dict[str, Any], message: str, context: str, history: list) -> str:
    """
    Call n8n webhook (which acts as OpenAI API replacement).

    Args:
        config: Plugin configuration
        message: User message
        context: Enhanced context from RAG
        history: Conversation history

    Returns:
        Response text from n8n
    """
    webhook_url = config.get('n8n_webhook_url', '')
    api_key = config.get('n8n_api_key', '')

    if not webhook_url:
        raise ValueError("n8n webhook URL not configured")

    # Build messages
    messages = [
        {
            'role': 'system',
            'content': config.get('system_prompt', '') + '\n\n' + context if context else config.get('system_prompt', '')
        }
    ]
    messages.extend(history)
    messages.append({
        'role': 'user',
        'content': message
    })

    # Call n8n webhook
    headers = {
        'Content-Type': 'application/json'
    }
    if api_key:
        headers['Authorization'] = f"Bearer {api_key}"

    # n8n webhook can accept OpenAI-like format
    response = requests.post(
        webhook_url,
        headers=headers,
        json={
            'messages': messages,
            'model': config.get('model', 'gpt-4o-mini'),
            'temperature': config.get('temperature', 0.7),
            'max_tokens': config.get('max_tokens', 1000)
        },
        timeout=60
    )

    response.raise_for_status()
    data = response.json()

    # Handle different n8n response formats
    if 'choices' in data:
        # OpenAI-compatible format
        return data['choices'][0]['message']['content']
    elif 'response' in data:
        # Custom format
        return data['response']
    elif 'text' in data:
        # Simple format
        return data['text']
    else:
        # Return raw JSON as string
        return str(data)


def start_api_server(host: str, port: int, rag_manager, mcp_tools_manager, config: Dict[str, Any]):
    """
    Start API server in a separate thread.

    Args:
        host: Server host
        port: Server port
        rag_manager: RAGManager instance
        mcp_tools_manager: MCPToolsManager instance
        config: Plugin configuration

    Returns:
        Thread object
    """
    app = create_app(rag_manager, mcp_tools_manager, config)

    def run_server():
        """Run Flask server."""
        try:
            # Disable Flask startup messages
            import sys
            from io import StringIO

            # Redirect Flask logs
            log = logging.getLogger('werkzeug')
            log.setLevel(logging.ERROR)

            app.run(host=host, port=port, debug=False, use_reloader=False)
        except Exception as e:
            logger.error(f"API server error: {e}")

    # Start server in background thread
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()

    return thread
