"""Tool package for the egirl agent.

Exposes the :class:`EgirlTool` so the agent can register it during
dynamic tool discovery. Without this export the package was empty,
which could prevent the tool from being located by the loader.
"""

from .egirl_tool import EgirlTool

__all__ = ["EgirlTool"]
