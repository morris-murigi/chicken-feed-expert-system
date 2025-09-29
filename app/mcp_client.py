import asyncio
import sys
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()

    async def connect_to_server(self, server_script_path: str):
        """Connect to MCP server (chicken feed expert system)."""
        command = "python"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None,
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        # List tools
        response = await self.session.list_tools()
        print("Connected. Tools:", [tool.name for tool in response.tools])

    async def process_query(self, query: str, verbose: bool = False) -> str:
        """Send a natural language query to Claude, handle tool calls.

        Args:
            query (str): The user’s question.
            verbose (bool): If True, include tool call logs in output. Default False.
        """
        messages = [{"role": "user", "content": query}]

        response = await self.session.list_tools()
        available_tools = [
            {"name": tool.name, "description": tool.description, "input_schema": tool.inputSchema}
            for tool in response.tools
        ]

        response = self.anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=800,
            messages=messages,
            tools=available_tools,
        )

        final_text = []
        assistant_message_content = []

        for content in response.content:
            if content.type == "text":
                final_text.append(content.text)
                assistant_message_content.append(content)
            elif content.type == "tool_use":
                tool_name = content.name
                tool_args = content.input

                # Call the tool
                result = await self.session.call_tool(tool_name, tool_args)

                if verbose:
                    # Only show tool call info if verbose=True
                    final_text.append(f"(Tool {tool_name} called with {tool_args})")

                assistant_message_content.append(content)
                messages.append({"role": "assistant", "content": assistant_message_content})
                messages.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": content.id,
                                "content": result.content,
                            }
                        ],
                    }
                )

                # Get refined response after tool result
                response = self.anthropic.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=800,
                    messages=messages,
                    tools=available_tools,
                )

                # Append only the assistant’s natural response
                for c in response.content:
                    if c.type == "text":
                        final_text.append(c.text)

        return "\n".join(final_text)


    async def cleanup(self):
        await self.exit_stack.aclose()


async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        while True:
            query = input("Query (or quit): ").strip()
            if query.lower() == "quit":
                break
            result = await client.process_query(query)
            print("\nResponse:", result)
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
