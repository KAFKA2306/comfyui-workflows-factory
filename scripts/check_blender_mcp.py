#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["mcp-for-blender==2.2.9"]
# ///
"""Blender MCP から現在のシーンを読み取り、接続を検査する。"""

import asyncio
import os
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def check_scene():
    settings = StdioServerParameters(
        command="uvx",
        args=["mcp-for-blender@2.2.9"],
        env={**os.environ, "DISABLE_TELEMETRY": "true"},
    )
    async with stdio_client(settings) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            response = await session.call_tool("get_scene_info", {"limit": 1})
            summary = next((item.text.strip() for item in response.content if item.type == "text"), "")
    if response.isError or not summary.startswith("Scene "):
        raise RuntimeError(summary or "シーン情報がありません")
    print(summary.splitlines()[0])


if __name__ == "__main__":
    try:
        asyncio.run(asyncio.wait_for(check_scene(), timeout=30))
    except Exception as error:
        sys.exit(f"Blender MCP に接続できません。Blender の Start MCP Server を確認してください。\n{error}")
