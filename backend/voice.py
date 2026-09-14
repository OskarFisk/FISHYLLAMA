"""FishyLLAMA voice/TTS orchestration.

Inspired by the uploaded Jarvis project: sentence-aware streaming, URL cleanup,
voice profiles, interruptible speech, microphone/listening states, and graceful
fallbacks. This module is provider-neutral; actual synthesis can be supplied by
an external/local provider while the browser can use Web Speech as a zero-key
fallback.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from typing import List


@dataclass(frozen=True)
class VoiceProfile:
    id: str
    name: str
    language: str
    gender: str
    style: str
    rate: float
    pitch: float
    description: str


VOICE_PROFILES = [
    VoiceProfile("fishy-neural", "Fishy Neural", "en-US", "neutral", "warm", 1.02, 0.0, "Balanced assistant voice for everyday conversation."),
    VoiceProfile("jarvis-british", "British Assistant", "en-GB", "neutral", "precise", 1.05, -0.05, "A crisp British-style profile, echoing the uploaded Jarvis voice design."),
    VoiceProfile("fishy-calm", "Fishy Calm", "en-US", "neutral", "calm", 0.92, -0.08, "Slower and softer for explanations and long answers."),
    VoiceProfile("fishy-fast", "Fishy Fast", "en-US", "neutral", "energetic", 1.15, 0.04, "Faster delivery for short commands and coding tasks."),
    VoiceProfile("swedish", "Svenska", "sv-SE", "neutral", "natural", 1.0, 0.0, "Swedish voice profile when a Swedish system voice is available."),
]


def simplify_urls(text: str) -> str:
    """Make URLs pronounceable, e.g. https://www.example.com/a -> example.com."""
    pattern = r"https?://[^\s<>()]+"
    def repl(match: re.Match[str]) -> str:
        value = re.sub(r"^https?://", "", match.group(0))
        value = re.sub(r"^www\.", "", value)
        return value.split("/")[0]
    return re.sub(pattern, repl, text)


def clean_for_speech(text: str) -> str:
    """Remove code/markup that should not be spoken aloud."""
    text = re.sub(r"```[\s\S]*?```", " Code block omitted. ", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"https?://[^\s]+", lambda m: simplify_urls(m.group(0)), text)
    text = re.sub(r"[*_>#]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def split_sentences(text: str, max_chars: int = 260) -> List[str]:
    """Split response text into natural, streamable speech chunks.

    The uploaded Jarvis implementation used sentence buffering and a best-effort
    split for long sentences. FishyLLAMA keeps that behavior while also handling
    very long punctuation-free responses.
    """
    text = clean_for_speech(text)
    if not text:
        return []
    pieces = re.split(r"(?<=[.!?])\s+", text)
    output: List[str] = []
    for piece in pieces:
        piece = piece.strip()
        while len(piece) > max_chars:
            candidates = [m.start() for m in re.finditer(r"[,;:]\s", piece[:max_chars])]
            cut = max(candidates) + 1 if candidates else piece.rfind(" ", 0, max_chars)
            if cut <= 0:
                cut = max_chars
            output.append(piece[:cut].strip())
            piece = piece[cut:].strip()
        if piece:
            output.append(piece)
    return output


def profiles() -> list[dict]:
    return [asdict(profile) for profile in VOICE_PROFILES]
