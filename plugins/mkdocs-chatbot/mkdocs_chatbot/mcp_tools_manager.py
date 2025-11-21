"""
MCP Tools Manager for ChatBot Plugin

Manages Model Context Protocol (MCP) tools integration.
Allows chatbot to use external tools configured via mkdocs.yaml.
"""

import logging
import json
from typing import List, Dict, Any, Optional, Callable
import requests
import subprocess

logger = logging.getLogger('mkdocs.plugins.chatbot.mcp')


class MCPToolsManager:
    """
    Manages MCP tools for enhanced chatbot capabilities.
    """

    def __init__(self, tools_config: List[Dict[str, Any]]):
        """
        Initialize MCP tools manager.

        Args:
            tools_config: List of tool configurations
                Each tool should have:
                - name: Tool name
                - description: What the tool does
                - type: 'http', 'cli', 'python', 'mcp_server'
                - Additional type-specific configuration
        """
        self.tools_config = tools_config
        self.tools = {}
        self.tool_schemas = []

        self._initialize_tools()

    def _initialize_tools(self):
        """Initialize all configured tools."""
        for tool_config in self.tools_config:
            try:
                tool_name = tool_config.get('name')
                tool_type = tool_config.get('type')

                if not tool_name or not tool_type:
                    logger.warning(f"Invalid tool configuration: {tool_config}")
                    continue

                # Create tool based on type
                if tool_type == 'http':
                    tool = self._create_http_tool(tool_config)
                elif tool_type == 'cli':
                    tool = self._create_cli_tool(tool_config)
                elif tool_type == 'python':
                    tool = self._create_python_tool(tool_config)
                elif tool_type == 'mcp_server':
                    tool = self._create_mcp_server_tool(tool_config)
                else:
                    logger.warning(f"Unknown tool type: {tool_type}")
                    continue

                if tool:
                    self.tools[tool_name] = tool
                    self.tool_schemas.append(self._create_tool_schema(tool_config))
                    logger.info(f"Initialized MCP tool: {tool_name} ({tool_type})")

            except Exception as e:
                logger.error(f"Failed to initialize tool {tool_config.get('name')}: {e}")

    def _create_http_tool(self, config: Dict[str, Any]) -> Callable:
        """Create HTTP-based tool."""
        endpoint = config.get('endpoint')
        method = config.get('method', 'POST').upper()
        headers = config.get('headers', {})
        auth = config.get('auth')

        def http_tool(**kwargs) -> Dict[str, Any]:
            """Execute HTTP tool."""
            try:
                request_headers = headers.copy()

                # Add authentication
                if auth:
                    if auth.get('type') == 'bearer':
                        request_headers['Authorization'] = f"Bearer {auth.get('token')}"
                    elif auth.get('type') == 'apikey':
                        request_headers[auth.get('header', 'X-API-Key')] = auth.get('key')

                # Make request
                if method == 'GET':
                    response = requests.get(endpoint, params=kwargs, headers=request_headers, timeout=30)
                else:
                    response = requests.post(endpoint, json=kwargs, headers=request_headers, timeout=30)

                response.raise_for_status()
                return {'success': True, 'result': response.json()}

            except Exception as e:
                logger.error(f"HTTP tool error: {e}")
                return {'success': False, 'error': str(e)}

        return http_tool

    def _create_cli_tool(self, config: Dict[str, Any]) -> Callable:
        """Create CLI-based tool."""
        command_template = config.get('command')
        shell = config.get('shell', False)
        timeout = config.get('timeout', 30)

        def cli_tool(**kwargs) -> Dict[str, Any]:
            """Execute CLI tool."""
            try:
                # Format command with arguments
                command = command_template.format(**kwargs)

                # Execute command
                result = subprocess.run(
                    command,
                    shell=shell,
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )

                if result.returncode == 0:
                    return {'success': True, 'result': result.stdout}
                else:
                    return {'success': False, 'error': result.stderr}

            except Exception as e:
                logger.error(f"CLI tool error: {e}")
                return {'success': False, 'error': str(e)}

        return cli_tool

    def _create_python_tool(self, config: Dict[str, Any]) -> Callable:
        """Create Python function tool."""
        module_path = config.get('module')
        function_name = config.get('function')

        def python_tool(**kwargs) -> Dict[str, Any]:
            """Execute Python tool."""
            try:
                # Dynamic import
                parts = module_path.rsplit('.', 1)
                if len(parts) == 2:
                    module_name, _ = parts
                    module = __import__(module_name, fromlist=[function_name])
                else:
                    module = __import__(module_path)

                func = getattr(module, function_name)
                result = func(**kwargs)

                return {'success': True, 'result': result}

            except Exception as e:
                logger.error(f"Python tool error: {e}")
                return {'success': False, 'error': str(e)}

        return python_tool

    def _create_mcp_server_tool(self, config: Dict[str, Any]) -> Callable:
        """Create MCP server tool."""
        server_url = config.get('server_url')
        tool_name = config.get('tool_name')

        def mcp_server_tool(**kwargs) -> Dict[str, Any]:
            """Execute MCP server tool."""
            try:
                # Call MCP server
                response = requests.post(
                    f"{server_url}/tools/{tool_name}",
                    json={'params': kwargs},
                    timeout=30
                )

                response.raise_for_status()
                return response.json()

            except Exception as e:
                logger.error(f"MCP server tool error: {e}")
                return {'success': False, 'error': str(e)}

        return mcp_server_tool

    def _create_tool_schema(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create OpenAI-compatible tool schema for function calling.

        Args:
            config: Tool configuration

        Returns:
            Tool schema in OpenAI function format
        """
        parameters = config.get('parameters', {})

        # Build parameters schema
        properties = {}
        required = []

        for param_name, param_config in parameters.items():
            param_type = param_config.get('type', 'string')
            param_desc = param_config.get('description', '')
            param_required = param_config.get('required', False)

            properties[param_name] = {
                'type': param_type,
                'description': param_desc
            }

            # Add enum if specified
            if 'enum' in param_config:
                properties[param_name]['enum'] = param_config['enum']

            if param_required:
                required.append(param_name)

        return {
            'type': 'function',
            'function': {
                'name': config['name'],
                'description': config.get('description', ''),
                'parameters': {
                    'type': 'object',
                    'properties': properties,
                    'required': required
                }
            }
        }

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool by name.

        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments

        Returns:
            Tool execution result
        """
        if tool_name not in self.tools:
            return {'success': False, 'error': f"Tool '{tool_name}' not found"}

        try:
            tool = self.tools[tool_name]
            result = tool(**arguments)
            logger.info(f"Executed tool {tool_name} successfully")
            return result
        except Exception as e:
            logger.error(f"Tool execution error for {tool_name}: {e}")
            return {'success': False, 'error': str(e)}

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Get OpenAI-compatible tool schemas for all tools."""
        return self.tool_schemas

    def get_tool_names(self) -> List[str]:
        """Get list of available tool names."""
        return list(self.tools.keys())

    def is_available(self) -> bool:
        """Check if any tools are available."""
        return len(self.tools) > 0


# Example MCP tools configuration:
"""
mcp_tools:
  - name: search_documentation
    description: Search through project documentation
    type: http
    endpoint: https://api.example.com/search
    method: POST
    headers:
      Content-Type: application/json
    auth:
      type: bearer
      token: ${SEARCH_API_KEY}
    parameters:
      query:
        type: string
        description: Search query
        required: true
      limit:
        type: integer
        description: Maximum number of results
        required: false

  - name: execute_code_snippet
    description: Execute a code snippet and return the result
    type: cli
    command: python -c "{code}"
    shell: true
    timeout: 10
    parameters:
      code:
        type: string
        description: Python code to execute
        required: true

  - name: get_file_info
    description: Get information about a file
    type: python
    module: pathlib
    function: Path.stat
    parameters:
      path:
        type: string
        description: File path
        required: true

  - name: custom_analysis
    description: Run custom code analysis
    type: mcp_server
    server_url: http://localhost:8000
    tool_name: analyze_code
    parameters:
      code:
        type: string
        description: Code to analyze
        required: true
"""
