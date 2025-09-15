"""Core tool package for Agent Zero.

This package exposes built-in tools so they can be discovered by
agent profiles.  Currently it registers the :class:`CodeExecution`
plugin which provides the ``code_execution_tool`` used for running
code and shell commands."""

from .code_execution_tool import CodeExecution

__all__ = ["CodeExecution"]

