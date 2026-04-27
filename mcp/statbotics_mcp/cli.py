"""Command-line entry point for the Statbotics MCP server."""

from __future__ import annotations

import argparse
import sys
from typing import Optional, Sequence

from .server import mcp


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="statbotics-mcp",
        description=(
            "MCP server for the public Statbotics API. "
            "Defaults to stdio transport for use with local MCP clients "
            "(Claude Desktop, VS Code, Cursor). "
            "Pass --http to expose the server over HTTP/SSE instead."
        ),
    )
    parser.add_argument(
        "--http",
        action="store_true",
        help="Run a streamable-HTTP server instead of speaking MCP over stdio.",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind when --http is used (default: 127.0.0.1).",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind when --http is used (default: 8000).",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.http:
        mcp.run(transport="http", host=args.host, port=args.port)
    else:
        mcp.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
