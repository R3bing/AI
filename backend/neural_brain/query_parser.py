"""Neuro-Cognitive Query Parser for Quantum Knowledge Weaver.
Deconstructs long, conversational, multi-clause inquiries into:
- Core research entities & semantic concepts
- Epistemic domain classification (Empirical, Theological, Biomedical, Chemical, Space, Humanities)
- Targeted API search queries (preventing query saturation in external academic search engines)
- Focused sub-questions for multi-hop cognitive reasoning.
"""

import re
from typing import List, Dict, Set, Optional
from pydantic import BaseModel, Field


class ParsedCognitiveQuery(BaseModel):
    """Structured decomposition of a natural language inquiry."""
    raw_query: str
    cleaned_intent: str
    core_entities: List[str] = Field(default_factory=list)
    epistemic_domains: List[str] = Field(default_factory=list)
    sub_questions: List[str] = Field(default_factory=list)
    api_targeted_queries: Dict[str, str] = Field(default_factory=dict)
    dominant_mode: str = "balanced"  # empirical, contemplative, or balanced


class CognitiveQueryParser:
    """Emulates human brain prefrontal comprehension for complex, multi-sentence queries."""

    # Conversational filler phrases to strip from academic search tokens
    CONVERSATIONAL_FILLERS = [
        r"\b(could|can|would|will)\s+you\s+(please\s+)?(explain|tell|describe|clarify|elaborate|help)\b",
        r"\bi\s+(am|was|have\s+been)\s+(wondering|thinking|feeling|curious|interested)\s+(about|if|whether|how)\b",
        r"\bwhat\s+(is|are|do|does)\s+the\s+(significance|meaning|impact|concept)\s+of\b",
        r"\bi\s+want\s+to\s+(know|understand|learn)\b",
        r"\bcan\s+you\s+give\s+me\s+an\s+overview\s+of\b",
        r"\bplease\s+(explain|describe|analyze)\b",
        r"\bin\s+(deep|simple|layman|scientific)\s+detail\b",
        r"\bfrom\s+(both|the)\s+perspective\s+of\b",
        r"\bwhat\s+does\s+(modern|current)\s+(science|physics|medicine)\s+say\s+about\b",
        r"\bwhat\s+do\s+(ancient|theological|religious|traditional)\s+texts?\s+say\s+about\b",
    ]

    STOPWORDS = {
        "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
        "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both",
        "but", "by", "can", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does",
        "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had",
        "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her",
        "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd",
        "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself",
        "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off",
        "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own",
        "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some",
        "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then",
        "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those",
        "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll",
        "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's",
        "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't",
        "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves",
        "please", "tell", "explain", "give", "detail", "also", "really", "just", "like"
    }

    DOMAIN_LEXICONS = {
        "physics": [
            "quantum", "physics", "entanglement", "qubit", "gravity", "spacetime", "relativity",
            "cosmology", "black hole", "universe", "expansion", "wave", "particle", "string theory",
            "thermodynamics", "entropy", "optics", "photon", "atom", "mechanics"
        ],
        "biomedical": [
            "cell", "cancer", "protein", "dna", "gene", "virus", "treatment", "medicine", "clinical",
            "disease", "brain", "neuron", "neural", "synapse", "consciousness", "health", "therapy",
            "pathology", "immune", "biology"
        ],
        "theological": [
            "quran", "hadith", "prophet", "islam", "allah", "surah", "verse", "sunnah", "prayer",
            "faith", "deen", "soul", "ruh", "qalb", "heart", "god", "spiritual", "afterlife",
            "creation", "wisdom", "contemplation", "tafakkur"
        ],
        "astrophysics": [
            "space", "astronomy", "planet", "galaxy", "cosmology", "telescope", "orbit", "universe",
            "star", "mars", "nasa", "cosmic", "hubble", "james webb", "nebula", "solar"
        ],
        "chemistry": [
            "chemical", "compound", "molecule", "formula", "drug", "acid", "synthesis", "bonding",
            "reaction", "molecular", "pubchem", "polymer", "solute", "atomic"
        ],
        "academic": [
            "citation", "paper", "journal", "author", "scholar", "study", "literature", "review",
            "doi", "crossref", "openalex", "peer-reviewed", "experiment"
        ],
        "humanities": [
            "philosophy", "ethics", "history", "ancient", "mind", "consciousness", "morality",
            "epistemology", "metaphysics", "literature", "society", "theology"
        ],
    }

    def parse(self, raw_query: str) -> ParsedCognitiveQuery:
        """Parses a long, conversational, multi-sentence query into structured cognitive elements."""
        clean_text = raw_query.strip()
        
        # 1. Clean conversational filler for search engines
        filtered_text = clean_text
        for pattern in self.CONVERSATIONAL_FILLERS:
            filtered_text = re.sub(pattern, " ", filtered_text, flags=re.IGNORECASE)
        
        # Remove punctuation for token parsing
        tokens_raw = re.findall(r"\b[a-zA-Z0-9_\-]{3,}\b", filtered_text)
        substantive_tokens = [w for w in tokens_raw if w.lower() not in self.STOPWORDS]

        # 2. Extract Core Named Entities / Compound Concepts
        # Look for multi-word phrases and capitalized words
        compounds = []
        lower_raw = clean_text.lower()
        for domain, keywords in self.DOMAIN_LEXICONS.items():
            for kw in keywords:
                if kw in lower_raw and kw not in compounds:
                    compounds.append(kw)
        
        # Add high-signal tokens if not already covered
        for tok in substantive_tokens[:6]:
            if tok.lower() not in compounds and len(tok) > 3:
                compounds.append(tok.lower())

        core_entities = compounds[:8]

        # 3. Detect Epistemic Domains
        detected_domains = []
        for domain, keywords in self.DOMAIN_LEXICONS.items():
            match_count = sum(1 for kw in keywords if kw in lower_raw)
            if match_count > 0:
                detected_domains.append(domain)

        if not detected_domains:
            detected_domains = ["academic", "physics"]

        # 4. Determine Dominant Mode
        is_empirical = any(d in detected_domains for d in ["physics", "biomedical", "astrophysics", "chemistry"])
        is_contemplative = any(d in detected_domains for d in ["theological", "humanities"])
        if is_empirical and is_contemplative:
            dominant_mode = "balanced"
        elif is_empirical:
            dominant_mode = "empirical"
        else:
            dominant_mode = "contemplative"

        # 5. Extract Sub-Questions from multi-clause sentences
        clauses = re.split(r"[?;.!\n]|(?:\band\s+(?:how|what|whether|why|can)\b)", clean_text)
        sub_questions = []
        for cl in clauses:
            cl_clean = cl.strip()
            if len(cl_clean.split()) >= 3:
                # Add question mark if missing
                if not cl_clean.endswith("?"):
                    cl_clean += "?"
                sub_questions.append(cl_clean)

        if not sub_questions:
            sub_questions = [clean_text]

        # 6. Generate Tailored API Queries
        # This solves the critical issue: academic APIs choke on 40-word sentences.
        api_targeted = self._build_api_targeted_queries(clean_text, substantive_tokens, detected_domains)

        # Build clean intent summary
        cleaned_intent = " ".join(substantive_tokens[:7]) if substantive_tokens else clean_text[:60]

        return ParsedCognitiveQuery(
            raw_query=clean_text,
            cleaned_intent=cleaned_intent,
            core_entities=core_entities,
            epistemic_domains=detected_domains,
            sub_questions=sub_questions[:4],
            api_targeted_queries=api_targeted,
            dominant_mode=dominant_mode,
        )

    def _build_api_targeted_queries(
        self,
        raw_query: str,
        substantive_tokens: List[str],
        detected_domains: List[str],
    ) -> Dict[str, str]:
        """Constructs targeted, high-precision search keywords for each candidate API."""
        raw_lower = raw_query.lower()
        top_tokens = " ".join(substantive_tokens[:5])

        # Domain clusters
        physics_terms = [t for t in substantive_tokens if any(t in kw for kw in self.DOMAIN_LEXICONS["physics"] + self.DOMAIN_LEXICONS["astrophysics"])]
        bio_terms = [t for t in substantive_tokens if any(t in kw for kw in self.DOMAIN_LEXICONS["biomedical"])]
        theological_terms = [t for t in substantive_tokens if any(t in kw for kw in self.DOMAIN_LEXICONS["theological"])]
        chemical_terms = [t for t in substantive_tokens if any(t in kw for kw in self.DOMAIN_LEXICONS["chemistry"])]

        # Specific mappings
        targeted = {}

        # 1. arXiv: physics, cosmology, quantum, AI, math
        if physics_terms:
            targeted["arxiv"] = " ".join(physics_terms[:4])
        else:
            targeted["arxiv"] = " ".join(substantive_tokens[:4])

        # 2. PubMed: biomedical, genetics, health, neuroscience
        if bio_terms:
            targeted["pubmed"] = " ".join(bio_terms[:4])
        else:
            targeted["pubmed"] = " ".join(substantive_tokens[:4])

        # 3. Wikipedia: head concept (1-3 words max)
        targeted["wikipedia"] = " ".join(substantive_tokens[:3])

        # 4. Quran: theological / Arabic roots / spiritual keywords
        if theological_terms:
            targeted["quran"] = " ".join(theological_terms[:3])
        else:
            # Map common physics/existential themes to Quranic topics
            if "universe" in raw_lower or "cosmology" in raw_lower or "creation" in raw_lower:
                targeted["quran"] = "creation heavens earth universe"
            elif "soul" in raw_lower or "consciousness" in raw_lower or "mind" in raw_lower:
                targeted["quran"] = "soul ruh heart sight hearing"
            elif "light" in raw_lower or "optics" in raw_lower:
                targeted["quran"] = "light nur heavens earth"
            else:
                targeted["quran"] = " ".join(substantive_tokens[:3])

        # 5. Hadith: prophetic traditions
        if theological_terms:
            targeted["hadith"] = " ".join(theological_terms[:3])
        else:
            if "heart" in raw_lower or "consciousness" in raw_lower or "soul" in raw_lower:
                targeted["hadith"] = "heart soul contemplation intention"
            elif "universe" in raw_lower or "creation" in raw_lower:
                targeted["hadith"] = "creation universe heavens"
            elif "health" in raw_lower or "medicine" in raw_lower:
                targeted["hadith"] = "medicine cure health healing"
            else:
                targeted["hadith"] = " ".join(substantive_tokens[:3])

        # 6. NASA: space, cosmology, planets
        if physics_terms or "space" in detected_domains or "astrophysics" in detected_domains:
            targeted["nasa"] = " ".join([t for t in substantive_tokens if t in self.DOMAIN_LEXICONS["astrophysics"]][:3]) or "cosmology universe"
        else:
            targeted["nasa"] = " ".join(substantive_tokens[:3])

        # 7. OpenAlex: Academic Graph
        targeted["openalex"] = " ".join(substantive_tokens[:4])

        # 8. PubChem: Chemical compounds
        if chemical_terms:
            targeted["pubchem"] = chemical_terms[0]
        else:
            targeted["pubchem"] = substantive_tokens[0] if substantive_tokens else "compound"

        # 9. Google Data: general research
        targeted["google"] = " ".join(substantive_tokens[:5])

        # 10. Crossref: peer-reviewed DOI literature
        targeted["crossref"] = " ".join(substantive_tokens[:4])

        # 11. OpenLibrary: historical & philosophical books
        targeted["openlibrary"] = " ".join(substantive_tokens[:3])

        return targeted


query_parser = CognitiveQueryParser()
