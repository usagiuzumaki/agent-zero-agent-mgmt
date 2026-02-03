from typing import Literal
import tiktoken

APPROX_BUFFER = 1.1
TRIM_BUFFER = 0.8


def count_tokens(text: str, encoding_name="cl100k_base") -> int:
    if not text:
        return 0

    # Get the encoding
    encoding = tiktoken.get_encoding(encoding_name)

    # Encode the text and count the tokens
    tokens = encoding.encode(text)
    token_count = len(tokens)

    return token_count


def approximate_tokens(
    text: str,
) -> int:
    if not text:
        return 0

    # Optimization: For short strings (e.g. streaming deltas), use a simple heuristic
    # to avoid the overhead of tiktoken encoding.
    # We assume ~3 characters per token (conservative estimate vs typical 4)
    # which aligns with the APPROX_BUFFER conservatism.
    if len(text) < 100:
        return max(1, int(len(text) / 3))

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
