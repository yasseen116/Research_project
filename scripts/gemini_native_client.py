#!/usr/bin/env python3
"""Minimal native Gemini client using only the standard library."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass


def extract_first_json_object(text: str) -> dict:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        stripped = "\n".join(lines).strip()

    try:
        payload = json.loads(stripped)
        if isinstance(payload, dict):
            return payload
    except json.JSONDecodeError:
        pass

    start = stripped.find("{")
    end = stripped.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("Could not find a JSON object in Gemini response")
    payload = json.loads(stripped[start : end + 1])
    if not isinstance(payload, dict):
        raise ValueError("Extracted Gemini payload is not a JSON object")
    return payload


@dataclass
class GeminiConfig:
    api_key: str
    model: str
    base_url: str = "https://generativelanguage.googleapis.com/v1beta"
    timeout_seconds: int = 90
    temperature: float = 0.0

    @classmethod
    def from_env(cls) -> "GeminiConfig":
        api_key = os.environ.get("REQ_GEMINI_API_KEY", "").strip()
        model = os.environ.get("REQ_GEMINI_MODEL", "").strip()
        base_url = os.environ.get("REQ_GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta").strip()
        timeout_raw = os.environ.get("REQ_GEMINI_TIMEOUT_SECONDS", "90").strip()
        temperature_raw = os.environ.get("REQ_GEMINI_TEMPERATURE", "0.0").strip()

        if not api_key:
            raise ValueError("Missing REQ_GEMINI_API_KEY")
        if not model:
            raise ValueError("Missing REQ_GEMINI_MODEL")

        return cls(
            api_key=api_key,
            model=model,
            base_url=base_url.rstrip("/"),
            timeout_seconds=int(timeout_raw),
            temperature=float(temperature_raw),
        )


class GeminiNativeClient:
    def __init__(self, config: GeminiConfig) -> None:
        self.config = config
        self.url = f"{self.config.base_url}/models/{self.config.model}:generateContent"

    def generate_json(
        self,
        prompt: str,
        response_schema: dict,
        temperature: float | None = None,
    ) -> dict:
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt,
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": self.config.temperature if temperature is None else temperature,
                "responseMimeType": "application/json",
                "responseJsonSchema": response_schema,
            },
        }
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.config.api_key,
        }
        request = urllib.request.Request(self.url, data=body, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(request, timeout=self.config.timeout_seconds) as response:
                raw = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {exc.code} from Gemini API: {error_body}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Could not reach Gemini API endpoint {self.url}: {exc}") from exc

        payload = json.loads(raw)
        candidates = payload.get("candidates")
        if not isinstance(candidates, list) or not candidates:
            raise ValueError(f"Gemini response does not contain candidates: {raw}")

        parts = candidates[0].get("content", {}).get("parts", [])
        texts = [part.get("text", "") for part in parts if isinstance(part, dict)]
        text = "\n".join(item for item in texts if item)
        if not text:
            raise ValueError(f"Gemini response did not contain text parts: {raw}")

        return {
            "text": text,
            "usage": payload.get("usageMetadata", {}),
            "raw_response": payload,
        }
