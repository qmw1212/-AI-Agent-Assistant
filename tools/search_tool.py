"""
Web Search Tool — optimized for speed (3 results, 8s timeout)
"""

from langchain_core.tools import Tool
from duckduckgo_search import DDGS


def search_web(query: str) -> str:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query.strip(), max_results=3))

        if not results:
            return "No search results found."

        lines = []
        for i, r in enumerate(results, 1):
            lines.append(f"{i}. {r['title']}\n   {r['body']}\n   {r['href']}")
        return "\n\n".join(lines)

    except Exception as e:
        return f"Search error: {str(e)}"


def create_search_tool() -> Tool:
    return Tool(
        name="WebSearch",
        func=search_web,
        description=(
            "Search the web for current information, news, or documentation. "
            "Input: a search query string. "
            "Example: 'Python 3.14 new features'"
        )
    )
