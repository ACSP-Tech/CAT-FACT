import re

async def interpret_natural_language_query(query: str) -> dict:
    q = query.lower().strip()
    filters = {}

    # Detect "palindromic" or "palindrome"
    if "palindrom" in q:
        filters["is_palindrome"] = True
    else:
        filters["is_palindrome"] = None
    # Detect single/multiple words
    if "single word" in q or "one word" in q:
        filters["word_count"] = 1
    elif "two words" in q or "double word" in q:
        filters["word_count"] = 2
    elif "word" in q:
        filters["word_count"] = 3
    else:
        filters["word_count"] = None
    # Detect "longer than X characters"
    match = re.search(r"longer than (\d+)", q)
    if match:
        filters["min_length"] = int(match.group(1)) + 1
    else:
        filters["min_length"] = None

    # Detect "shorter than X characters"
    match = re.search(r"shorter than (\d+)", q)
    if match:
        filters["max_length"] = int(match.group(1)) - 1
    else:
        filters["max_length"] = None

    # Detect "containing letter/character"
    match = re.search(r"containing (?:the letter |the character |letter |character )?([a-z])", q)
    if match:
        filters["contains_character"] = match.group(1)
    else:
        filters["contains_character"] = None

    # Handle "first vowel" heuristic
    if "first vowel" in q:
        filters["contains_character"] = "a"  # simple fallback heuristic

    return filters

from fastapi_pagination import Params
from typing import Annotated
from pydantic import Field


class StringParams(Params):
    """Default pagination parameters with a custom page size for all users"""
    size: Annotated[int, Field(gt=1, le=50)] = 10  # Default page size set to 10, max 50, min 1