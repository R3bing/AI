"""JARVIS Multimodal Vision Engine.

Provides real-time visual perception for JARVIS:
- Analyzes webcam captures, screen captures, and image files.
- Uses Gemini 2.5 Flash Vision (and fallbacks) to inspect UI, code, physical objects, and diagrams.
"""

from __future__ import annotations

import base64
import os
import time
from typing import Dict, Any, Optional
import httpx
import structlog
from backend.config import settings

logger = structlog.get_logger(__name__)


class JarvisVisionEngine:
    """Multimodal vision perception for JARVIS ('The Camera & Screen Eyes')."""

    def __init__(self):
        self.gemini_key = settings.gemini_api_key
        self.gemini_model = "gemini-2.5-flash"
        self.openai_key = settings.openai_api_key

    async def analyze_image(
        self,
        image_bytes: bytes,
        prompt: str = "Analyze this image in detail and tell me what you see.",
        mime_type: str = "image/jpeg",
    ) -> Dict[str, Any]:
        """Analyzes an image and returns JARVIS's executive perception."""
        t0 = time.perf_counter()
        encoded = base64.b64encode(image_bytes).decode("utf-8")

        # 1. Try Gemini 2.5 Flash Multimodal
        if self.gemini_key:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.gemini_model}:generateContent?key={self.gemini_key}"
                payload = {
                    "contents": [
                        {
                            "parts": [
                                {
                                    "text": (
                                        "You are JARVIS, an ultra-advanced AI operating system and executive companion. "
                                        "Speak in a concise, sharp, brilliant, and proactive tone. "
                                        f"Directive: {prompt}"
                                    )
                                },
                                {
                                    "inline_data": {
                                        "mime_type": mime_type,
                                        "data": encoded,
                                    }
                                },
                            ]
                        }
                    ],
                    "generationConfig": {
                        "temperature": 0.4,
                        "maxOutputTokens": 1024,
                    },
                }
                async with httpx.AsyncClient(timeout=30.0) as client:
                    resp = await client.post(url, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        candidates = data.get("candidates", [])
                        if candidates:
                            text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                            elapsed = time.perf_counter() - t0
                            return {
                                "success": True,
                                "analysis": text,
                                "provider": "Gemini 2.5 Flash Vision",
                                "latency_sec": round(elapsed, 2),
                            }
            except Exception as e:
                logger.warning("gemini_vision_failed", error=str(e))

        # 2. Try OpenAI Vision if available
        if self.openai_key:
            try:
                url = "https://api.openai.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.openai_key}"}
                payload = {
                    "model": "gpt-4o-mini",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": f"You are JARVIS. Be sharp and executive. {prompt}"},
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:{mime_type};base64,{encoded}"},
                                },
                            ],
                        }
                    ],
                    "max_tokens": 1024,
                }
                async with httpx.AsyncClient(timeout=30.0) as client:
                    resp = await client.post(url, json=payload, headers=headers)
                    if resp.status_code == 200:
                        data = resp.json()
                        text = data["choices"][0]["message"]["content"]
                        elapsed = time.perf_counter() - t0
                        return {
                            "success": True,
                            "analysis": text,
                            "provider": "OpenAI GPT-4o Vision",
                            "latency_sec": round(elapsed, 2),
                        }
            except Exception as e:
                logger.warning("openai_vision_failed", error=str(e))

        # Fallback
        elapsed = time.perf_counter() - t0
        return {
            "success": False,
            "analysis": "Vision sensor captured the frame successfully, but external vision API credentials are not active.",
            "provider": "Local Hardware Frame Buffer",
            "latency_sec": round(elapsed, 2),
        }


jarvis_vision = JarvisVisionEngine()
