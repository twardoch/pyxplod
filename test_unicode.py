#!/usr/bin/env python3
"""Test Unicode support with various characters."""


def greet_world():
    """Say hello in multiple languages."""
    return {
        "english": "Hello",
        "spanish": "Hola",
        "french": "Bonjour",
        "german": "Grüße",
        "japanese": "こんにちは",
        "chinese": "你好",
        "arabic": "مرحبا",
        "russian": "Привет",
        "emoji": "👋🌍",
    }


class UnicodeHandler:
    """Handle Unicode text with special characters: áéíóú ñ ç ø."""

    def process(self, text: str) -> str:
        """Process text with Unicode: → ← ↑ ↓ • © ® ™."""
        return f"Processed: {text}"


# Test mathematical symbols: ∑ ∏ ∫ √ ∞ ≈ ≠ ≤ ≥
MATH_PI = "π ≈ 3.14159"
