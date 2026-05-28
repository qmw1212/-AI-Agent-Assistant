"""
File Analyzer Tool
Provides file reading and analysis capabilities
"""

from langchain_core.tools import Tool
import os
from typing import Optional


def analyze_file(file_path: str) -> str:
    """
    Read and analyze text files (txt, md)
    """
    try:
        file_path = file_path.strip().strip('"').strip("'")

        # If not absolute, search relative to this file's directory first
        if not os.path.isabs(file_path):
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            candidate = os.path.join(base_dir, file_path)
            if os.path.exists(candidate):
                file_path = candidate

        if not os.path.exists(file_path):
            return f"Error: File not found at '{file_path}'"

        allowed_extensions = ['.txt', '.md', '.markdown']
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext not in allowed_extensions:
            return f"Error: Unsupported file type '{file_ext}'. Only .txt and .md files are supported."

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.split('\n')
        words = content.split()
        chars = len(content)

        summary = [
            f"File: {os.path.basename(file_path)}",
            f"Size: {chars} characters, {len(words)} words, {len(lines)} lines",
            f"\n--- Full Content ---",
            content,
            f"\n--- End of File ---"
        ]
        return "\n".join(summary)

    except UnicodeDecodeError:
        return "Error: File encoding not supported. Please use UTF-8 encoded text files."
    except PermissionError:
        return f"Error: Permission denied to read '{file_path}'"
    except Exception as e:
        return f"File analysis error: {str(e)}"


def create_file_tool() -> Tool:
    """Create and return the file analyzer tool"""
    return Tool(
        name="FileAnalyzer",
        func=analyze_file,
        description=(
            "Useful for reading and analyzing text files (.txt, .md). "
            "Provides file statistics and content preview. "
            "Input should be a file path (absolute or relative). "
            "Example: 'README.md' or 'C:/Users/Documents/notes.txt'"
        )
    )
