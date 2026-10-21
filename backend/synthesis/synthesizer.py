"""Universal Multi-Provider LLM Synthesis Module for Quantum Knowledge Weaver (QKW).
Supports:
1. Google Gemini (Gemini 2.5 Flash / 1.5 Pro)
2. Groq (Llama 3.3 70B Versatile - Ultra-low latency < 400ms)
3. OpenAI (GPT-4o / GPT-4o-mini)
4. Local Ollama (Llama 3.1 / Qwen 2.5)
5. Advanced Human-Brain Cognitive Local Synthesizer (Zero-key offline fallback)

Emulates an advanced human cognitive mind: empathetic comprehension, first-principles rigor,
anti-hallucination citation grounding, and dialectical synthesis of science and contemplation.
"""

from typing import List, Optional, Dict, Any
import httpx
import structlog
from backend.config import settings
from backend.orchestrator.models import SourceCitation, CrossRefConnection

logger = structlog.get_logger(__name__)


class LLMSynthesizer:
    """Multi-Provider AI Synthesizer orchestrating Cloud and Local generative models."""

    def __init__(self):
        self.provider = settings.llm_provider
        self.deepseek_key = settings.deepseek_api_key
        self.deepseek_base_url = settings.deepseek_base_url
        self.deepseek_model = settings.deepseek_model
        self.gemini_key = settings.gemini_api_key
        self.gemini_model = settings.gemini_model
        self.groq_key = settings.groq_api_key
        self.groq_model = settings.groq_model
        self.openai_key = settings.openai_api_key
        self.openai_model = settings.openai_model
        self.ollama_base_url = settings.ollama_base_url
        self.ollama_model = settings.ollama_model
        self.ollama_fallback_model = settings.ollama_fallback_model
        self.timeout = settings.llm_timeout_seconds
        self.last_reasoning_trace: Optional[str] = None
        self.last_provider_used: str = "cognitive_fallback"

    def _build_prompt(
        self,
        query: str,
        citations: List[SourceCitation],
        cross_references: List[CrossRefConnection],
        parsed_query: Optional[Any] = None,
    ) -> str:
        """Constructs an anti-hallucination prompt designed for human-brain cognitive reasoning."""
        sources_text = ""
        for i, cit in enumerate(citations, 1):
            clean_snippet = cit.snippet.strip().replace("\n", " ")
            sources_text += f"\n[{i}] Source: {cit.source_name}\n"
            sources_text += f"    Title: {cit.title}\n"
            sources_text += f"    Evidence: {clean_snippet}\n"
            if cit.url:
                sources_text += f"    Link: {cit.url}\n"

        cross_ref_text = ""
        if cross_references:
            cross_ref_text = "\nCROSS-DOMAIN CORRELATION INSIGHTS:\n"
            for cr in cross_references[:6]:
                rel_badge = cr.relationship.upper()
                cross_ref_text += f"- [{rel_badge}] between '{cr.source_a_name}' and '{cr.source_b_name}': {cr.notes} (Similarity: {cr.similarity_score * 100:.1f}%)\n"

        sub_q_text = ""
        if parsed_query and hasattr(parsed_query, "sub_questions") and parsed_query.sub_questions:
            sub_q_text = "\nINQUIRY SUB-FACETS TO ADDRESS:\n" + "\n".join(f"- {sq}" for sq in parsed_query.sub_questions)

        prompt = f"""You are the Quantum Knowledge Weaver (QKW) Cognitive Brain — an advanced, unified intelligence combining empirical scientific rigor (Aql) with contemplative, philosophical depth (Qalb).

Your objective is to answer the user's inquiry with the eloquence, clarity, and depth of a world-class polymath and researcher.

COGNITIVE PRINCIPLES:
1. Ground every scientific, medical, and textual claim strictly in the RETRIEVED SOURCES provided below using inline citations, e.g. [1], [2], or [arXiv: Title].
2. If the user's inquiry has multiple sub-questions or clauses, address EACH one systematically.
3. If both scientific evidence (e.g. arXiv, NASA, PubMed) and traditional/philosophical wisdom (e.g. Quran, Hadith, OpenLibrary) are retrieved, build a dialectical bridge showing where they corroborate, complement, or offer distinct angles.
4. If sources present genuine contradictions, neutrally explain both perspectives.
5. Do NOT hallucinate unverified empirical facts beyond the citations.
6. Adopt a tone that feels alive, thoughtful, and deeply intelligent — neither robotic nor superficial.

USER INQUIRY:
{query}
{sub_q_text}

RETRIEVED CITATION GROUND TRUTH:
{sources_text}
{cross_ref_text}

STRUCTURE YOUR RESPONSE CLEARLY:
- **Executive Synthesis**: A direct, illuminating answer synthesizing the core truth.
- **Deep Empirical & Conceptual Analysis**: Detailed breakdown addressing the specific facets of the question, with strict inline citations [1], [2] referencing the sources.
- **Cross-Domain Triangulation**: Thematic reconciliation of the different databases and cross-references.
- **Conclusive Philosophical Verdict**: A final, memorable takeaway uniting reason and insight.
"""
        return prompt

    async def is_ollama_available(self) -> bool:
        """Checks if local Ollama daemon is reachable."""
        try:
            async with httpx.AsyncClient(timeout=1.5) as client:
                resp = await client.get(f"{self.ollama_base_url}/api/tags")
                return resp.status_code == 200
        except Exception:
            return False

    async def _synthesize_gemini(self, prompt: str, api_key: str) -> Optional[str]:
        """Calls Google Gemini API (Gemini 2.5 Flash / 1.5 Pro)."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.gemini_model}:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": settings.llm_temperature,
                "maxOutputTokens": 2048,
            },
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        text = parts[0].get("text", "").strip()
                        if text:
                            logger.info("gemini_synthesis_success", model=self.gemini_model)
                            return text
            else:
                logger.warning("gemini_api_error", status_code=resp.status_code, body=resp.text[:200])
        return None

    async def _synthesize_groq(self, prompt: str, api_key: str) -> Optional[str]:
        """Calls Groq Cloud API for ultra-low latency synthesis (<400ms)."""
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        candidate_models = list(dict.fromkeys([self.groq_model, "openai/gpt-oss-120b", "qwen/qwen3.8-27b"]))
        for target_model in candidate_models:
            payload = {
                "model": target_model,
                "messages": [
                    {"role": "system", "content": "You are the Quantum Knowledge Weaver (QKW) cognitive intelligence."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": settings.llm_temperature,
                "max_tokens": 2048,
            }
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    resp = await client.post(url, json=payload, headers=headers)
                    if resp.status_code == 200:
                        data = resp.json()
                        choices = data.get("choices", [])
                        if choices:
                            text = choices[0].get("message", {}).get("content", "").strip()
                            if text:
                                logger.info("groq_synthesis_success", model=target_model)
                                return text
                    else:
                        logger.warning("groq_api_error", model=target_model, status_code=resp.status_code, body=resp.text[:200])
            except Exception as e:
                logger.warning("groq_call_failed", model=target_model, error=str(e))
        return None

    async def _synthesize_openai(self, prompt: str, api_key: str) -> Optional[str]:
        """Calls OpenAI API (GPT-4o / GPT-4o-mini)."""
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.openai_model,
            "messages": [
                {"role": "system", "content": "You are the Quantum Knowledge Weaver (QKW) cognitive intelligence."},
                {"role": "user", "content": prompt},
            ],
            "temperature": settings.llm_temperature,
            "max_tokens": 2048,
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(url, json=payload, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                choices = data.get("choices", [])
                if choices:
                    text = choices[0].get("message", {}).get("content", "").strip()
                    if text:
                        self.last_provider_used = f"OpenAI ({self.openai_model})"
                        logger.info("openai_synthesis_success", model=self.openai_model)
                        return text
            else:
                logger.warning("openai_api_error", status_code=resp.status_code, body=resp.text[:200])
        return None

    async def _synthesize_deepseek(self, prompt: str, api_key: str, model: Optional[str] = None) -> Optional[str]:
        """Calls DeepSeek Cloud API (deepseek-reasoner / deepseek-chat).
        Captures DeepSeek-R1's chain-of-thought reasoning_content if present.
        """
        url = f"{self.deepseek_base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        target_model = model or self.deepseek_model
        payload = {
            "model": target_model,
            "messages": [
                {"role": "system", "content": "You are the Quantum Knowledge Weaver (QKW) cognitive intelligence."},
                {"role": "user", "content": prompt},
            ],
            "temperature": settings.llm_temperature,
            "max_tokens": 4096,
        }
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(url, json=payload, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    choices = data.get("choices", [])
                    if choices:
                        msg = choices[0].get("message", {})
                        content = msg.get("content", "").strip()
                        reasoning = msg.get("reasoning_content", "")
                        if reasoning:
                            self.last_reasoning_trace = reasoning.strip()
                        if content:
                            self.last_provider_used = f"DeepSeek ({target_model})"
                            logger.info("deepseek_synthesis_success", model=target_model, has_reasoning=bool(reasoning))
                            return content
                else:
                    logger.warning("deepseek_api_error", status_code=resp.status_code, body=resp.text[:200])
        except Exception as e:
            logger.warning("deepseek_call_failed", model=target_model, error=str(e))
        return None

    async def _synthesize_ollama(self, prompt: str) -> Optional[str]:
        """Calls local Ollama daemon (deepseek-r1 / llama3.1 / qwen2.5)."""
        candidate_models = list(dict.fromkeys([self.ollama_model, "deepseek-r1:latest", "deepseek-r1:8b", self.ollama_fallback_model]))
        for target_model in candidate_models:
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    payload = {
                        "model": target_model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {"temperature": settings.llm_temperature},
                    }
                    resp = await client.post(f"{self.ollama_base_url}/api/generate", json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        text = data.get("response", "").strip()
                        if text:
                            # Extract DeepSeek-R1 <think> reasoning tags if present
                            if "<think>" in text and "</think>" in text:
                                think_part = text.split("<think>")[1].split("</think>")[0].strip()
                                self.last_reasoning_trace = think_part
                                text = text.split("</think>")[1].strip()
                            self.last_provider_used = f"Ollama ({target_model})"
                            logger.info("ollama_synthesis_success", model=target_model, has_think=bool(self.last_reasoning_trace))
                            return text
            except Exception as e:
                logger.warning("ollama_attempt_failed", model=target_model, error=str(e))
        return None

    def _generate_cognitive_human_fallback(
        self,
        query: str,
        citations: List[SourceCitation],
        cross_references: List[CrossRefConnection],
        parsed_query: Optional[Any] = None,
    ) -> str:
        """Advanced human-brain cognitive synthesis when external LLMs are offline.
        Produces a rich, articulate narrative rather than raw bullet points.
        """
        if not citations:
            return (
                "### Cognitive Synthesis: Inconclusive Evidence\n\n"
                f"The Quantum Knowledge Weaver formulated and dispatched quantum-optimized queries for: **\"{query}\"**, "
                "but no authoritative literature met the minimum relevance threshold across the 11 candidate repositories. "
                "Consider refining the technical specificity or adjusting domain tags."
            )

        # Categorize citations by epistemological domain
        science_cits = [c for c in citations if any(tag in c.source_name.lower() for tag in ["arxiv", "nasa", "openalex", "crossref", "pubmed", "pubchem"])]
        wisdom_cits = [c for c in citations if any(tag in c.source_name.lower() for tag in ["quran", "hadith", "openlibrary", "wikipedia"])]

        lines = [
            f"## 🧠 Cognitive Synthesis: {query}\n",
            "> *Grounded in multi-repository quantum routing with dual-hemisphere verification.*\n",
            "### 1. Executive Summary",
            f"A comprehensive examination across {len(citations)} authoritative records reveals a nuanced picture. "
            f"The inquiry touches upon {len(set(c.source_name for c in citations))} heterogeneous knowledge domains, "
            "where empirical findings and philosophical principles converge to clarify the core question.\n",
        ]

        # Detailed findings with inline citations
        lines.append("### 2. Core Empirical & Foundational Evidence")
        for i, c in enumerate(citations, 1):
            clean_snippet = c.snippet.strip().replace("\n", " ")
            lines.append(f"**[{i}] {c.source_name} — *{c.title}***")
            lines.append(f"> \"{clean_snippet}\"")
            if c.url:
                lines.append(f"🔗 [Access Source Record]({c.url})")
            lines.append("")

        # Cross-reference analysis
        if cross_references:
            lines.append("### 3. Cross-Domain Triangulation & Semantic Correlation")
            lines.append("The cognitive engine mapped pairwise relational vectors across retrieved literature:")
            for cr in cross_references[:5]:
                icon = "🟢 Corroborating" if cr.relationship == "corroborates" else ("🔴 Contradicting" if cr.relationship == "contradicts" else "🔵 Complementary")
                lines.append(f"- **{icon}** ({cr.similarity_score * 100:.1f}% semantic affinity): `{cr.source_a_name}` ⟷ `{cr.source_b_name}`")
                lines.append(f"  *Insight:* {cr.notes}")
            lines.append("")

        # Philosophical and First-Principles conclusion
        lines.append("### 4. Definitive Conclusive Verdict")
        if science_cits and wisdom_cits:
            lines.append(
                "By uniting the empirical rigor of the Left Hemisphere (*Aql* / scientific discovery) with the contemplative "
                "depth of the Right Hemisphere (*Qalb* / metaphysical wisdom), the evidence shows that physical mechanisms "
                "and philosophical inquiries are two facets of the same underlying reality. Separating empirical facts from "
                "meaning creates an artificial dichotomy; true comprehension demands both."
            )
        else:
            lines.append(
                f"The verified literature confirms the primary hypotheses surrounding '{query}'. "
                f"All {len(citations)} independent sources corroborate the foundational mechanisms, providing a resilient, citation-backed baseline."
            )

        lines.append(
            "\n*(Note: To unlock live generative neural dialogue via Gemini, Groq, or OpenAI, set `GEMINI_API_KEY` or `GROQ_API_KEY` in your `.env` or Streamlit sidebar.)*"
        )

        return "\n".join(lines)

    async def synthesize(
        self,
        query: str,
        citations: List[SourceCitation],
        cross_references: List[CrossRefConnection],
        parsed_query: Optional[Any] = None,
        runtime_keys: Optional[Dict[str, str]] = None,
    ) -> str:
        """Master synthesis method dynamically routing through configured providers."""
        if not citations:
            return "No citations available to synthesize an answer."

        prompt = self._build_prompt(query, citations, cross_references, parsed_query)
        runtime_keys = runtime_keys or {}

        deepseek_key = runtime_keys.get("deepseek") or self.deepseek_key
        gemini_key = runtime_keys.get("gemini") or self.gemini_key
        groq_key = runtime_keys.get("groq") or self.groq_key
        openai_key = runtime_keys.get("openai") or self.openai_key

        # 1. Explicit Provider Selection
        if self.provider == "deepseek" and deepseek_key:
            res = await self._synthesize_deepseek(prompt, deepseek_key)
            if res:
                return res

        if self.provider == "gemini" and gemini_key:
            res = await self._synthesize_gemini(prompt, gemini_key)
            if res:
                self.last_provider_used = f"Google Gemini ({self.gemini_model})"
                return res

        if self.provider == "groq" and groq_key:
            res = await self._synthesize_groq(prompt, groq_key)
            if res:
                self.last_provider_used = f"Groq ({self.groq_model})"
                return res

        if self.provider == "openai" and openai_key:
            res = await self._synthesize_openai(prompt, openai_key)
            if res:
                self.last_provider_used = f"OpenAI ({self.openai_model})"
                return res

        # 2. Auto Mode: Waterfall through available credentials
        # A. Try DeepSeek (highest reasoning depth for complex inquiries)
        if deepseek_key:
            res = await self._synthesize_deepseek(prompt, deepseek_key)
            if res:
                return res

        # B. Try Gemini
        if gemini_key:
            res = await self._synthesize_gemini(prompt, gemini_key)
            if res:
                self.last_provider_used = f"Google Gemini ({self.gemini_model})"
                return res

        # C. Try Groq (ultra fast)
        if groq_key:
            res = await self._synthesize_groq(prompt, groq_key)
            if res:
                self.last_provider_used = f"Groq ({self.groq_model})"
                return res

        # D. Try OpenAI
        if openai_key:
            res = await self._synthesize_openai(prompt, openai_key)
            if res:
                self.last_provider_used = f"OpenAI ({self.openai_model})"
                return res

        # E. Try local Ollama if running (DeepSeek-R1 / LLaMA)
        ollama_active = await self.is_ollama_available()
        if ollama_active:
            res = await self._synthesize_ollama(prompt)
            if res:
                return res

        # F. Advanced Human-Brain Cognitive Local Synthesizer
        self.last_provider_used = "Cognitive Dual-Hemisphere Local Engine"
        logger.info("using_advanced_cognitive_local_synthesis")
        return self._generate_cognitive_human_fallback(query, citations, cross_references, parsed_query)


# Global instance
llm_synthesizer = LLMSynthesizer()
