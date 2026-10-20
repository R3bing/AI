"""LLM Synthesis module for Quantum Knowledge Weaver.
Uses local Ollama (llama3.1 or qwen2.5) to synthesize grounded, citation-backed answers.
Includes deterministic structured fallback when Ollama daemon is offline.
"""

from typing import List, Optional
import httpx
import structlog
from backend.config import settings
from backend.orchestrator.models import SourceCitation, CrossRefConnection

logger = structlog.get_logger(__name__)


class LLMSynthesizer:
    """Synthesizes factual answers strictly grounded in retrieved API citations."""

    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
        self.fallback_model = settings.ollama_fallback_model
        self.timeout = settings.llm_timeout_seconds

    def _build_prompt(
        self,
        query: str,
        citations: List[SourceCitation],
        cross_references: List[CrossRefConnection],
    ) -> str:
        """Constructs an anti-hallucination prompt instructing the LLM to rely strictly on citations."""
        sources_text = ""
        for i, cit in enumerate(citations, 1):
            sources_text += f"\n[{i}] Source: {cit.source_name}\n"
            sources_text += f"    Title: {cit.title}\n"
            sources_text += f"    Content: {cit.snippet}\n"

        cross_ref_text = ""
        if cross_references:
            cross_ref_text = "\nCROSS-REFERENCE INSIGHTS:\n"
            for cr in cross_references[:4]:
                cross_ref_text += f"- [{cr.relationship.upper()}] between '{cr.source_a_name}' and '{cr.source_b_name}': {cr.notes}\n"

        prompt = f"""You are the Quantum Knowledge Weaver (QKW) AI Brain.
Your role is to synthesize a factual, clear, and comprehensive answer to the user's inquiry based EXCLUSIVELY on the provided retrieved sources below.

RULES:
1. Do NOT hallucinate or assume facts outside the provided sources.
2. Attribute every key point using bracketed citations, e.g. [1], [2], or [Source: Title].
3. If sources from different domains (e.g. Science/arXiv and Religious/Quran) provide relevant complementary views, highlight that connection.
4. If the sources do not contain enough information to fully answer, state clearly what is known from the sources and what is missing.

USER INQUIRY:
{query}

RETRIEVED KNOWLEDGE SOURCES:
{sources_text}
{cross_ref_text}

Provide your structured answer below, with an Executive Summary, Key Findings with inline citations, Cross-Domain Synthesis, and Conclusions:"""
        return prompt

    async def is_ollama_available(self) -> bool:
        """Checks if the local Ollama instance is running and reachable."""
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                resp = await client.get(f"{self.base_url}/api/tags")
                return resp.status_code == 200
        except Exception:
            return False

    def _generate_analytical_fallback(
        self,
        query: str,
        citations: List[SourceCitation],
        cross_references: List[CrossRefConnection],
    ) -> str:
        """Deterministic structured synthesis when Ollama local daemon is not running."""
        if not citations:
            return (
                "**No Direct Citations Found**\n\n"
                f"The Quantum Knowledge Weaver queried candidate APIs for '{query}', but no authoritative records were returned. "
                "Try refining your search terms or expanding domain filters."
            )

        lines = [
            f"### Synthesis: {query}\n",
            "*(Synthesized via QKW Deterministic Extractive Engine. To enable local generative LLM synthesis, ensure Ollama is running with `ollama run llama3.1`)*\n",
            "#### 1. Core Findings from Retrieved APIs:\n",
        ]

        for i, c in enumerate(citations, 1):
            lines.append(f"- **[{i}] {c.source_name} — {c.title}**")
            lines.append(f"  > *\"{c.snippet.strip()}\"*")
            if c.url:
                lines.append(f"  [Link to Source]({c.url})")
            lines.append("")

        if cross_references:
            lines.append("#### 2. Cross-Source Correlation & Relationships:")
            for cr in cross_references:
                badge = "🟢 Corroboration" if cr.relationship == "corroborates" else ("🔴 Contradiction" if cr.relationship == "contradicts" else "🔵 Complementary Context")
                lines.append(f"- {badge}: **{cr.source_a_name}** ⟷ **{cr.source_b_name}**")
                lines.append(f"  *Similarity: {cr.similarity_score * 100:.1f}% — {cr.notes}*")
            lines.append("")

        lines.append("#### 3. Quantum-Classical Consensus:")
        lines.append(
            f"The quantum router converged on {len(set(c.source_name for c in citations))} distinct knowledge domains. "
            "The retrieved evidence collectively provides multi-angle validation for the query topic."
        )

        return "\n".join(lines)

    async def synthesize(
        self,
        query: str,
        citations: List[SourceCitation],
        cross_references: List[CrossRefConnection],
    ) -> str:
        """Invokes Ollama or gracefully falls back to deterministic extraction."""
        if not citations:
            return "No citations available to synthesize an answer."

        # Check if Ollama is available
        ollama_active = await self.is_ollama_available()
        if not ollama_active:
            logger.info("ollama_offline_using_analytical_fallback")
            return self._generate_analytical_fallback(query, citations, cross_references)

        prompt = self._build_prompt(query, citations, cross_references)

        # Attempt synthesis with Ollama
        for target_model in [self.model, self.fallback_model]:
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    payload = {
                        "model": target_model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {"temperature": settings.llm_temperature},
                    }
                    resp = await client.post(f"{self.base_url}/api/generate", json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        response_text = data.get("response", "").strip()
                        if response_text:
                            logger.info("ollama_synthesis_success", model=target_model)
                            return response_text
            except Exception as e:
                logger.warning("ollama_generation_failed", model=target_model, error=str(e))

        # Fallback if Ollama model pull/generation failed
        return self._generate_analytical_fallback(query, citations, cross_references)


# Global instance
llm_synthesizer = LLMSynthesizer()
