from typing import Literal
import functools
import tiktoken

APPROX_BUFFER = 1.1
TRIM_BUFFER = 0.8


@functools.lru_cache()
def get_encoding(encoding_name: str):
    # Caching the encoding object prevents re-initialization overhead on every call.
    return tiktoken.get_encoding(encoding_name)


def count_tokens(text: str, encoding_name="cl100k_base") -> int:
    if not text:
        return 0

    # Get the encoding
    encoding = get_encoding(encoding_name)

    # Encode the text and count the tokens
    tokens = encoding.encode(text)
    token_count = len(tokens)

    return token_count


def approximate_tokens(
    text: str,
) -> int:
    if not text:
        return 0

    # OPTIMIZATION: Use fast heuristic for short strings to avoid tiktoken overhead
    # This is ~20x faster for strings < 100 chars
    if len(text) < 100:
        return max(1, len(text) // 3)

    return int(count_tokens(text) * APPROX_BUFFER)


def trim_to_tokens(
    text: str,
    max_tokens: int,
    direction: Literal["start", "end"],
    ellipsis: str = "...",
) -> str:
    chars = len(text)
    tokens = count_tokens(text)

    if tokens <= max_tokens:
        return text

    approx_chars = int(chars * (max_tokens / tokens) * TRIM_BUFFER)

    if direction == "start":
        return text[:approx_chars] + ellipsis
    return ellipsis + text[chars - approx_chars : chars]
