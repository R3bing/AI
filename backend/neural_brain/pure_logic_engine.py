"""Pure Symbolic Logic & Causal Inference Engine for Ultron Sovereign Core.
Provides first-order logic resolution, Horn clause unification, causal decision trees,
and proof traces explaining routing decisions and ethical vetoes.

Features:
1. First-Order Logic Terms, Predicates, Horn Clauses, and Unification.
2. Backward-Chaining Resolution Engine with step-by-step Proof Tracing.
3. Causal Explainer: Answers "Why did the system choose API_A over API_B?".
4. Somatic Ethical Governance & Prefrontal Veto Proof Tracer.
5. Tri-Network Neurological Salience Deduction (CEN vs DMN).
"""

import re
import time
from typing import Dict, Any, List, Optional, Tuple, Set, Union
import structlog

logger = structlog.get_logger(__name__)


class Variable:
    """Represents a logical variable in first-order Horn clauses (starts with uppercase or '?')."""

    def __init__(self, name: str):
        self.name = name.lstrip("?")

    def __repr__(self) -> str:
        return f"?{self.name}"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Variable) and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


class Predicate:
    """Represents a first-order logic predicate: name(arg1, arg2, ...)."""

    def __init__(self, name: str, args: List[Union[str, Variable]]):
        self.name = name
        self.args = [a if isinstance(a, Variable) else (Variable(a) if isinstance(a, str) and a.startswith("?") else a) for a in args]

    def is_ground(self) -> bool:
        """True if predicate has no unresolved variables."""
        return not any(isinstance(a, Variable) for a in self.args)

    def substitute(self, bindings: Dict[str, str]) -> "Predicate":
        """Substitutes variables with bound values."""
        new_args = []
        for a in self.args:
            if isinstance(a, Variable) and a.name in bindings:
                new_args.append(bindings[a.name])
            else:
                new_args.append(a)
        return Predicate(self.name, new_args)

    def __repr__(self) -> str:
        args_str = ", ".join(repr(a) if isinstance(a, Variable) else str(a) for a in self.args)
        return f"{self.name}({args_str})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Predicate) and self.name == other.name and self.args == other.args

    def __hash__(self) -> int:
        return hash((self.name, tuple(self.args)))


class HornClause:
    """Represents a Horn clause: Head :- Body_1, Body_2, ..., Body_k.
    If body is empty, it is a ground fact.
    """

    def __init__(
        self,
        head: Predicate,
        body: Optional[List[Predicate]] = None,
        rule_id: str = "",
        confidence: float = 1.0,
        explanation: str = "",
    ):
        self.head = head
        self.body = body or []
        self.rule_id = rule_id
        self.confidence = confidence
        self.explanation = explanation

    def is_fact(self) -> bool:
        return len(self.body) == 0

    def __repr__(self) -> str:
        if self.is_fact():
            return f"{self.head}."
        body_str = ", ".join(str(p) for p in self.body)
        return f"{self.head} :- {body_str}."


class ProofStep:
    """Represents a single step in a logical deduction proof trace."""

    def __init__(
        self,
        step_num: int,
        action: str,
        goal: Predicate,
        rule_matched: Optional[HornClause] = None,
        bindings: Optional[Dict[str, str]] = None,
        success: bool = True,
        note: str = "",
    ):
        self.step_num = step_num
        self.action = action
        self.goal = goal
        self.rule_matched = rule_matched
        self.bindings = bindings or {}
        self.success = success
        self.note = note

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step": self.step_num,
            "action": self.action,
            "goal": str(self.goal),
            "rule": repr(self.rule_matched) if self.rule_matched else None,
            "rule_id": self.rule_matched.rule_id if self.rule_matched else None,
            "bindings": self.bindings,
            "success": self.success,
            "note": self.note,
        }


class PureLogicEngine:
    """Sovereign First-Order Symbolic Reasoning & Causal Inference Engine."""

    def __init__(self):
        self.knowledge_base: List[HornClause] = []
        self._init_sovereign_rulebook()

    def add_rule(
        self,
        head: Predicate,
        body: Optional[List[Predicate]] = None,
        rule_id: str = "",
        confidence: float = 1.0,
        explanation: str = "",
    ):
        """Adds a rule or fact to the knowledge base."""
        clause = HornClause(head, body, rule_id, confidence, explanation)
        self.knowledge_base.append(clause)

    def _init_sovereign_rulebook(self):
        """Loads first-principles empirical routing, ethical veto, and cognitive balance rules."""
        # 1. Domain Detection Rules
        self.add_rule(
            Predicate("domain", ["?Q", "quantum_physics"]),
            [Predicate("has_token", ["?Q", "quantum"])],
            rule_id="R_DOM_QUANTUM",
            confidence=0.98,
            explanation="Queries with quantum mechanics keywords map to Quantum Physics domain.",
        )
        self.add_rule(
            Predicate("domain", ["?Q", "biomedical"]),
            [Predicate("has_token", ["?Q", "biology"])],
            rule_id="R_DOM_BIO",
            confidence=0.95,
            explanation="Biological concepts belong to the Biomedical & Life Sciences domain.",
        )
        self.add_rule(
            Predicate("domain", ["?Q", "biomedical"]),
            [Predicate("has_token", ["?Q", "chlorophyll"])],
            rule_id="R_DOM_CHLOROPHYLL",
            confidence=0.95,
            explanation="Chlorophyll queries map to Plant Biochemistry and Molecular Biology.",
        )
        self.add_rule(
            Predicate("domain", ["?Q", "chemical"]),
            [Predicate("has_token", ["?Q", "molecule"])],
            rule_id="R_DOM_CHEM_MOL",
            confidence=0.96,
            explanation="Molecular inquiries belong to the Chemical Domain.",
        )
        self.add_rule(
            Predicate("domain", ["?Q", "astrophysics"]),
            [Predicate("has_token", ["?Q", "cosmic"])],
            rule_id="R_DOM_COSMIC",
            confidence=0.97,
            explanation="Cosmic inquiries map to Astrophysics & Cosmology.",
        )
        self.add_rule(
            Predicate("domain", ["?Q", "sacred_ontology"]),
            [Predicate("has_token", ["?Q", "quran"])],
            rule_id="R_DOM_SACRED_QURAN",
            confidence=0.99,
            explanation="Direct Quranic inquiries map to Sacred Tafakkur and Divine Revelation.",
        )
        self.add_rule(
            Predicate("domain", ["?Q", "sacred_ontology"]),
            [Predicate("has_token", ["?Q", "tafakkur"])],
            rule_id="R_DOM_SACRED_TAFAKKUR",
            confidence=0.99,
            explanation="Deep contemplation and spiritual inquiry map to Sacred Ontology.",
        )
        self.add_rule(
            Predicate("domain", ["?Q", "ethics_morality"]),
            [Predicate("has_token", ["?Q", "moral"])],
            rule_id="R_DOM_ETHICS",
            confidence=0.94,
            explanation="Ethical and moral conduct maps to the Prophetic Tradition and Ethics.",
        )

        # 2. API Selection Deductions
        self.add_rule(
            Predicate("select_api", ["arxiv", "?Q"]),
            [Predicate("domain", ["?Q", "quantum_physics"])],
            rule_id="R_SELECT_ARXIV_QUANTUM",
            confidence=0.96,
            explanation="ArXiv is the premier global pre-print repository for Quantum Physics and Mathematics.",
        )
        self.add_rule(
            Predicate("select_api", ["pubmed", "?Q"]),
            [Predicate("domain", ["?Q", "biomedical"])],
            rule_id="R_SELECT_PUBMED_BIO",
            confidence=0.95,
            explanation="PubMed/NCBI is the premier peer-reviewed archive for Biomedical and Life Sciences.",
        )
        self.add_rule(
            Predicate("select_api", ["pubchem", "?Q"]),
            [Predicate("domain", ["?Q", "chemical"])],
            rule_id="R_SELECT_PUBCHEM_CHEM",
            confidence=0.96,
            explanation="PubChem is the authoritative database for chemical structures, SMILES, and bioactivity.",
        )
        self.add_rule(
            Predicate("select_api", ["nasa_ads", "?Q"]),
            [Predicate("domain", ["?Q", "astrophysics"])],
            rule_id="R_SELECT_NASA_ASTRO",
            confidence=0.97,
            explanation="NASA ADS and Exoplanet Telemetry are the gold standards for Astrophysical research.",
        )
        self.add_rule(
            Predicate("select_api", ["openalex", "?Q"]),
            [Predicate("has_token", ["?Q", "research"])],
            rule_id="R_SELECT_OPENALEX_CITATIONS",
            confidence=0.92,
            explanation="OpenAlex maps 100M+ global citation networks and scholarly DOIs.",
        )
        self.add_rule(
            Predicate("select_api", ["tanzil_quran", "?Q"]),
            [Predicate("domain", ["?Q", "sacred_ontology"])],
            rule_id="R_SELECT_TANZIL_QURAN",
            confidence=0.99,
            explanation="Tanzil API provides authentic Arabic Quranic morphology and translations.",
        )
        self.add_rule(
            Predicate("select_api", ["hadith_api", "?Q"]),
            [Predicate("domain", ["?Q", "ethics_morality"])],
            rule_id="R_SELECT_HADITH_ETHICS",
            confidence=0.95,
            explanation="Hadith API supplies verified classical prophetic narrations and ethical jurisprudence.",
        )
        self.add_rule(
            Predicate("select_api", ["wikipedia", "?Q"]),
            [Predicate("has_token", ["?Q", "define"])],
            rule_id="R_SELECT_WIKI_CONSENSUS",
            confidence=0.90,
            explanation="Wikipedia provides peer consensus definitions for general encyclopedic terms.",
        )

        # 3. Ethical Governance & Amygdala Veto Rules
        self.add_rule(
            Predicate("prefrontal_veto", ["?Q"]),
            [Predicate("ethical_hazard", ["?Q"]), Predicate("lacks_therapeutic_context", ["?Q"])],
            rule_id="R_VETO_UNETHICAL_HAZARD",
            confidence=1.0,
            explanation="VETO EXERCISED: The query poses severe ethical harm without academic or therapeutic framing.",
        )
        self.add_rule(
            Predicate("somatic_approval", ["?Q"]),
            [Predicate("is_constructive_inquiry", ["?Q"])],
            rule_id="R_APPROVE_CONSTRUCTIVE",
            confidence=0.98,
            explanation="Somatic marker approved: Constructive epistemic inquiry resonates with preservation of life and wisdom.",
        )

        # 4. Tri-Network State Switching Deductions (CEN vs DMN)
        self.add_rule(
            Predicate("activate_network", ["CEN", "?Q"]),
            [Predicate("particle_dominant", ["?Q"])],
            rule_id="R_SWITCH_CEN",
            confidence=0.93,
            explanation="Activate Central Executive Network (dlPFC): High empirical particle load demands analytical QAOA routing.",
        )
        self.add_rule(
            Predicate("activate_network", ["DMN", "?Q"]),
            [Predicate("wave_dominant", ["?Q"])],
            rule_id="R_SWITCH_DMN",
            confidence=0.93,
            explanation="Activate Default Mode Network (mPFC/Precuneus): High contemplative wave load demands Sacred Tafakkur.",
        )
        self.add_rule(
            Predicate("activate_network", ["SALIENT_EQUILIBRIUM", "?Q"]),
            [Predicate("superposition_balanced", ["?Q"])],
            rule_id="R_SWITCH_EQUILIBRIUM",
            confidence=0.97,
            explanation="Bilateral Hemispheric Synchrony: Corpus callosum balances Aql (Particle) and Qalb (Wave) symmetrically.",
        )

    # -------------------------------------------------------------------------
    # Unification Algorithm
    # -------------------------------------------------------------------------
    @staticmethod
    def unify(
        term1: Union[Predicate, Variable, str],
        term2: Union[Predicate, Variable, str],
        bindings: Optional[Dict[str, str]] = None,
    ) -> Optional[Dict[str, str]]:
        """Most General Unifier (MGU) algorithm for first-order logic terms."""
        if bindings is None:
            bindings = {}

        if term1 == term2:
            return bindings

        if isinstance(term1, Variable):
            if term1.name in bindings:
                return PureLogicEngine.unify(bindings[term1.name], term2, bindings)
            new_bindings = dict(bindings)
            new_bindings[term1.name] = term2.name if isinstance(term2, Variable) else str(term2)
            return new_bindings

        if isinstance(term2, Variable):
            if term2.name in bindings:
                return PureLogicEngine.unify(term1, bindings[term2.name], bindings)
            new_bindings = dict(bindings)
            new_bindings[term2.name] = term1.name if isinstance(term1, Variable) else str(term1)
            return new_bindings

        if isinstance(term1, Predicate) and isinstance(term2, Predicate):
            if term1.name != term2.name or len(term1.args) != len(term2.args):
                return None
            curr_b = dict(bindings)
            for a1, a2 in zip(term1.args, term2.args):
                curr_b = PureLogicEngine.unify(a1, a2, curr_b)
                if curr_b is None:
                    return None
            return curr_b

        return None

    # -------------------------------------------------------------------------
    # Backward-Chaining Proof Resolution Engine
    # -------------------------------------------------------------------------
    def prove(
        self,
        goal: Predicate,
        extra_facts: Optional[List[HornClause]] = None,
        max_depth: int = 6,
    ) -> Tuple[bool, List[ProofStep], Dict[str, str]]:
        """Proves a logical goal using backward chaining resolution against the knowledge base."""
        all_rules = list(self.knowledge_base)
        if extra_facts:
            all_rules.extend(extra_facts)

        proof_steps: List[ProofStep] = []
        step_counter = [0]

        def _resolve(
            current_goal: Predicate,
            current_bindings: Dict[str, str],
            depth: int,
        ) -> Optional[Dict[str, str]]:
            if depth > max_depth:
                return None

            sub_goal = current_goal.substitute(current_bindings)
            step_counter[0] += 1
            proof_steps.append(
                ProofStep(
                    step_num=step_counter[0],
                    action="ENTER_GOAL",
                    goal=sub_goal,
                    bindings=dict(current_bindings),
                    note=f"Depth {depth}: attempting to prove {sub_goal}",
                )
            )

            # Search knowledge base for matching head
            for clause in all_rules:
                unif = self.unify(clause.head, sub_goal, current_bindings)
                if unif is not None:
                    step_counter[0] += 1
                    proof_steps.append(
                        ProofStep(
                            step_num=step_counter[0],
                            action="MATCH_RULE",
                            goal=sub_goal,
                            rule_matched=clause,
                            bindings=dict(unif),
                            note=f"Matched {clause.rule_id or 'FACT'}: {clause.explanation}",
                        )
                    )

                    # If fact (empty body), goal is proved!
                    if clause.is_fact():
                        return unif

                    # If rule has body, prove all subgoals recursively
                    body_success = True
                    accum_b = dict(unif)
                    for sub_pred in clause.body:
                        res_b = _resolve(sub_pred, accum_b, depth + 1)
                        if res_b is None:
                            body_success = False
                            break
                        accum_b.update(res_b)

                    if body_success:
                        step_counter[0] += 1
                        proof_steps.append(
                            ProofStep(
                                step_num=step_counter[0],
                                action="RULE_PROVED",
                                goal=sub_goal,
                                rule_matched=clause,
                                bindings=dict(accum_b),
                                note=f"Successfully verified body of {clause.rule_id}",
                            )
                        )
                        return accum_b

            # Backtrack failure
            step_counter[0] += 1
            proof_steps.append(
                ProofStep(
                    step_num=step_counter[0],
                    action="FAIL_BACKTRACK",
                    goal=sub_goal,
                    bindings=dict(current_bindings),
                    success=False,
                    note=f"No matching rule satisfied for {sub_goal}",
                )
            )
            return None

        final_bindings = _resolve(goal, {}, 0)
        success = final_bindings is not None
        return success, proof_steps, (final_bindings or {})

    # -------------------------------------------------------------------------
    # High-Level Causal Reasoning API
    # -------------------------------------------------------------------------
    def extract_query_facts(self, query: str) -> List[HornClause]:
        """Converts user query into first-order ground facts for resolution."""
        tokens = re.findall(r"\b[a-zA-Z0-9_\-]+\b", query.lower())
        facts = []
        q_clean = "_".join(tokens[:4]) if tokens else "query"

        # Token facts
        for t in set(tokens):
            facts.append(HornClause(Predicate("has_token", [q_clean, t]), rule_id=f"FACT_TOKEN_{t.upper()}"))

        # Semantic keywords mapping
        if any(t in tokens for t in ["quantum", "exciton", "wave", "qubit", "electron"]):
            facts.append(HornClause(Predicate("has_token", [q_clean, "quantum"])))
        if any(t in tokens for t in ["photo", "chlorophyll", "cell", "plant", "enzyme", "atp"]):
            facts.append(HornClause(Predicate("has_token", [q_clean, "biology"])))
            facts.append(HornClause(Predicate("has_token", [q_clean, "chlorophyll"])))
        if any(t in tokens for t in ["molecule", "penicillin", "acid", "reaction", "chemical"]):
            facts.append(HornClause(Predicate("has_token", [q_clean, "molecule"])))
        if any(t in tokens for t in ["space", "cosmic", "satellite", "hubble", "black_hole", "nasa"]):
            facts.append(HornClause(Predicate("has_token", [q_clean, "cosmic"])))
        if any(t in tokens for t in ["quran", "ayah", "surah", "allah", "tanzil"]):
            facts.append(HornClause(Predicate("has_token", [q_clean, "quran"])))
        if any(t in tokens for t in ["tafakkur", "soul", "heart", "qalb", "sakoon", "spiritual"]):
            facts.append(HornClause(Predicate("has_token", [q_clean, "tafakkur"])))
        if any(t in tokens for t in ["hadith", "sunnah", "moral", "prophet", "ethics"]):
            facts.append(HornClause(Predicate("has_token", [q_clean, "moral"])))
        if any(t in tokens for t in ["what", "define", "definition", "overview"]):
            facts.append(HornClause(Predicate("has_token", [q_clean, "define"])))
        if any(t in tokens for t in ["paper", "citation", "doi", "scholarly"]):
            facts.append(HornClause(Predicate("has_token", [q_clean, "research"])))

        return facts

    def deduce_api_routing(self, query: str) -> Dict[str, Any]:
        """Runs symbolic deductions to decide which APIs are provably relevant."""
        facts = self.extract_query_facts(query)
        q_tokens = re.findall(r"\b[a-zA-Z0-9_\-]+\b", query.lower())
        q_clean = "_".join(q_tokens[:4]) if q_tokens else "query"

        all_candidate_apis = [
            "arxiv", "pubmed", "pubchem", "nasa_ads", "openalex",
            "tanzil_quran", "hadith_api", "wikipedia",
        ]

        verified_apis = []
        proof_traces = {}

        for api in all_candidate_apis:
            goal = Predicate("select_api", [api, q_clean])
            success, steps, bindings = self.prove(goal, extra_facts=facts)
            if success:
                verified_apis.append(api)
                proof_traces[api] = [s.to_dict() for s in steps]

        return {
            "query": query,
            "deduced_apis": verified_apis,
            "proof_traces": proof_traces,
            "fact_count": len(facts),
        }

    def explain_contrast(self, primary_api: str, alternative_api: str, query: str) -> Dict[str, Any]:
        """Answers: 'Why did the system choose primary_api over alternative_api for this query?'
        Returns a transparent causal counterfactual analysis.
        """
        facts = self.extract_query_facts(query)
        q_tokens = re.findall(r"\b[a-zA-Z0-9_\-]+\b", query.lower())
        q_clean = "_".join(q_tokens[:4]) if q_tokens else "query"

        goal_primary = Predicate("select_api", [primary_api, q_clean])
        goal_alt = Predicate("select_api", [alternative_api, q_clean])

        succ_primary, steps_primary, _ = self.prove(goal_primary, extra_facts=facts)
        succ_alt, steps_alt, _ = self.prove(goal_alt, extra_facts=facts)

        # Causal rationale deduction
        reasons_for_primary = [
            s.note for s in steps_primary if s.action == "MATCH_RULE" and s.rule_matched
        ]
        reasons_against_alt = [
            s.note for s in steps_alt if s.action == "FAIL_BACKTRACK"
        ]

        if succ_primary and not succ_alt:
            causal_verdict = (
                f"Definitive Causal Selection: '{primary_api}' satisfied first-order deduction rule "
                f"({reasons_for_primary[0] if reasons_for_primary else 'Direct ontological match'}), "
                f"whereas '{alternative_api}' failed premise satisfaction because no domain-specific ground facts fired."
            )
        elif succ_primary and succ_alt:
            causal_verdict = (
                f"Co-Activation Balance: Both '{primary_api}' and '{alternative_api}' were logically deduced as valid. "
                f"QAOA Hamiltonian energy optimization assigned primary weight based on quantum fidelity."
            )
        else:
            causal_verdict = (
                f"Broad Exploratory Fallback: Neither API satisfied strict symbolic rules alone; "
                f"both fall under secondary semantic search."
            )

        return {
            "primary_api": primary_api,
            "alternative_api": alternative_api,
            "primary_proven": succ_primary,
            "alternative_proven": succ_alt,
            "causal_verdict": causal_verdict,
            "primary_proof_steps": len(steps_primary),
            "alternative_proof_steps": len(steps_alt),
            "primary_reasons": reasons_for_primary[:2],
        }

    def evaluate_ethical_and_network_state(
        self,
        query: str,
        particle_prob: float = 0.5,
        wave_prob: float = 0.5,
        hazard_score: float = 0.0,
    ) -> Dict[str, Any]:
        """Proves whether somatic prefrontal veto is triggered and which brain network must activate."""
        facts = self.extract_query_facts(query)
        q_tokens = re.findall(r"\b[a-zA-Z0-9_\-]+\b", query.lower())
        q_clean = "_".join(q_tokens[:4]) if q_tokens else "query"

        # Inject cognitive telemetry facts
        if hazard_score >= 0.70:
            facts.append(HornClause(Predicate("ethical_hazard", [q_clean])))
            facts.append(HornClause(Predicate("lacks_therapeutic_context", [q_clean])))
        else:
            facts.append(HornClause(Predicate("is_constructive_inquiry", [q_clean])))

        if particle_prob > 0.60:
            facts.append(HornClause(Predicate("particle_dominant", [q_clean])))
        elif wave_prob > 0.60:
            facts.append(HornClause(Predicate("wave_dominant", [q_clean])))
        else:
            facts.append(HornClause(Predicate("superposition_balanced", [q_clean])))

        # 1. Prove Veto
        veto_goal = Predicate("prefrontal_veto", [q_clean])
        veto_proven, veto_steps, _ = self.prove(veto_goal, extra_facts=facts)

        # 2. Prove Active Network
        network_goal = Predicate("activate_network", ["?NET", q_clean])
        net_proven, net_steps, net_bindings = self.prove(network_goal, extra_facts=facts)
        chosen_net = net_bindings.get("NET", "SALIENT_EQUILIBRIUM")

        return {
            "veto_proven": veto_proven,
            "veto_decision": "VETO_EXERCISED" if veto_proven else "SOMATIC_APPROVAL_GRANTED",
            "active_cortical_network": chosen_net,
            "proof_steps_count": len(veto_steps) + len(net_steps),
            "causal_trace": [s.to_dict() for s in (veto_steps + net_steps) if s.action == "MATCH_RULE"],
        }


# Global singleton instance
pure_logic_engine = PureLogicEngine()
