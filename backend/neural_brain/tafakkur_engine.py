"""Tafakkur (Contemplation) Engine for the Neural-Quantum Cognitive Brain.
Synthesizes Islamic spiritual psychology, Sufi nafs stages, and deep contemplative prompts.
Strictly non-legalistic, designed for emotional tranquility (Sakoon) and self-awareness.
"""

from typing import Dict, Any, List


class TafakkurEngine:
    """Generates contemplative insights bridging spiritual wisdom and human psychology."""

    TAFAKKUR_CORPUS = [
        {
            "theme": "hardship_and_hope",
            "keywords": ["stress", "anxiety", "pain", "failure", "hopeless", "sad", "fear", "hardship", "tired", "depression"],
            "ayah": "Indeed, with hardship comes ease. Indeed, with hardship comes ease. (Surah Ash-Sharh, 94:5-6)",
            "hadith": "No fatigue, nor disease, nor sorrow, nor sadness, nor hurt, nor distress befalls a Muslim, even if it were the prick of a thorn, but that Allah expiates some of his sins for that. (Sahih al-Bukhari 5641)",
            "sufi_insight": "In the Sufi psychology of Nafs, emotional pain is the alarm clock of the Nafs al-Lawwamah (the self-reproaching soul), awakening you from the illusions of worldly control toward Divine surrender (Tawakkul).",
            "reflection_questions": [
                "What hidden strength or humility has this season of difficulty cultivated within you?",
                "If this current burden is a chisel shaping your character for future service, what rough edge is it removing?",
                "What is one worry you can intentionally surrender to the Creator today?",
            ],
        },
        {
            "theme": "creation_and_cosmos",
            "keywords": ["universe", "quantum", "stars", "physics", "cosmos", "atom", "space", "entanglement", "creation", "galaxy"],
            "ayah": "We will show them Our signs in the horizons and within themselves until it becomes clear to them that it is the truth. (Surah Fussilat, 41:53)",
            "hadith": "Contemplate upon the creation of Allah, and do not contemplate upon the essence of Allah, for you will never comprehend His magnitude. (Al-Bayhaqi)",
            "sufi_insight": "The outer macrocosm (Afaq) mirrors the inner microcosm (Anfus). When an atom exhibits wave-particle duality, it whispers that reality cannot be grasped solely by cold observation; meaning requires both logic and inner sight.",
            "reflection_questions": [
                "When you look at the quantum interconnectedness of the cosmos, does it remind you of the Unity (Tawhid) governing existence?",
                "How does knowing that every atom in your body was fashioned with precision affect your sense of human dignity?",
                "In what ways can your scientific curiosity be transformed into an act of worship and gratitude?",
            ],
        },
        {
            "theme": "purity_and_purpose",
            "keywords": ["purpose", "why", "meaning", "clean", "hygiene", "truth", "action", "intention", "life", "death"],
            "ayah": "And He created death and life to test you as to which of you is best in deed. (Surah Al-Mulk, 67:2)",
            "hadith": "Actions are judged by intentions (Niyyah), and each person will have only what they intended. (Sahih al-Bukhari 1)",
            "sufi_insight": "The highest station of the soul is Nafs al-Mutmainnah (the soul at complete peace). Peace is achieved when outer actions completely harmonize with inner pure intention.",
            "reflection_questions": [
                "What is the ultimate intention driving the projects and efforts you are dedicating your life to?",
                "If everything you accomplish today is stripped of public praise, would it still have value in the eyes of your Lord?",
                "What small, unseen act of kindness can you perform today solely for spiritual sincerity?",
            ],
        },
    ]

    def generate_tafakkur(self, query: str) -> Dict[str, Any]:
        """Matches query context to deep contemplative reflections, Tafseers, and world scriptures."""
        from backend.neural_brain.ontological_spiritual_engine import ontological_spiritual_engine
        res = ontological_spiritual_engine.match_resonance(query)
        return {
            "theme": res["theme"],
            "quranic_verse": f"{res['quranic_verse']} ({res['surah_reference']})",
            "surah_reference": res["surah_reference"],
            "tafseer_insight": res["tafseer_scholarly_insight"],
            "prophetic_hadith": f"{res['prophetic_hadith']} ({res['hadith_reference']})",
            "hadith_reference": res["hadith_reference"],
            "comparative_scripture": res["comparative_scripture"],
            "comparative_tradition": res["comparative_tradition"],
            "spiritual_psychology_insight": res["sufi_psychology_nafs"],
            "contemplative_questions": res["contemplative_questions"],
            "confidence_score": res["confidence_score"],
            "disclaimer": res["disclaimer"],
        }


tafakkur_engine = TafakkurEngine()
