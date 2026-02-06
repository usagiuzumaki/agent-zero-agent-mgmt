from unittest.mock import MagicMock

def get_sys_modules_mocks():
    """Returns a dictionary of mocks for heavy dependencies to patch sys.modules."""
    mocks = {}

    modules_to_mock = [
        "nest_asyncio", "litellm", "regex", "tiktoken", "git", "psutil",
        "diskcache", "crontab", "yaml", "pytz", "paramiko", "dotenv",
        "aiohttp", "webcolors",

        # Cryptography
        "cryptography", "cryptography.hazmat",
        "cryptography.hazmat.primitives",
        "cryptography.hazmat.primitives.asymmetric",

        # LangChain
        "langchain", "langchain_community",
        "langchain_core", "langchain_core.language_models",
        "langchain_core.language_models.chat_models",
        "langchain_core.language_models.llms",
        "langchain_core.messages", "langchain_core.prompts",
        "langchain_core.runnables", "langchain_core.output_parsers",
        "langchain_core.outputs", "langchain_core.outputs.chat_generation",
        "langchain_core.callbacks", "langchain_core.callbacks.manager",
        "langchain.embeddings", "langchain.embeddings.base"
    ]

    for name in modules_to_mock:
        mocks[name] = MagicMock()

    return mocks
