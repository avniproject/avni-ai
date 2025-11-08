"""
DSPy Configuration Management for Avni Smart Form Builder.

Simple configuration management for DSPy integration.
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class DSPyConfig:
    """DSPy configuration container."""
    model_provider: str = "openai"
    model_name: str = "gpt-4o-mini"
    api_key: str = ""
    max_tokens: int = 4000
    temperature: float = 0.7
    enable_tracing: bool = True
    
    def __post_init__(self):
        if not self.api_key:
            self.api_key = os.getenv("OPENAI_API_KEY", "")


def get_dspy_config() -> DSPyConfig:
    """Get DSPy configuration from environment."""
    return DSPyConfig(
        model_provider=os.getenv("DSPY_MODEL_PROVIDER", "openai"),
        model_name=os.getenv("DSPY_MODEL_NAME", "gpt-4o-mini"),
        api_key=os.getenv("OPENAI_API_KEY", ""),
        max_tokens=int(os.getenv("DSPY_MAX_TOKENS", "4000")),
        temperature=float(os.getenv("DSPY_TEMPERATURE", "0.7")),
        enable_tracing=os.getenv("DSPY_TRACING", "true").lower() == "true"
    )