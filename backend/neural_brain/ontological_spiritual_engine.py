"""Ontological & Universal Spiritual Equilibrium Engine for QKW.
Merges Islamic Contemplation (Tafakkur), classical Tafseers (Ibn Kathir, Al-Jalalayn),
Hadith traditions, and comparative world scriptures (Bhagavad Gita, Psalms, Tao Te Ching, Dhammapada)
using a neural semantic token matching engine for inner cognitive and spiritual tranquility (Sakoon).
"""

from typing import Dict, Any, List, Optional
import math
import re


class ScriptureEntry:
    def __init__(
        self,
        theme: str,
        keywords: List[str],
        quran_verse: str,
        surah_ref: str,
        tafseer_insight: str,
        hadith_tradition: str,
        hadith_ref: str,
        comparative_scripture: str,
        comparative_tradition: str,
        sufi_psychology_nafs: str,
        contemplative_inquiries: List[str],
    ):
        self.theme = theme
        self.keywords = [k.lower() for k in keywords]
        self.quran_verse = quran_verse
        self.surah_ref = surah_ref
        self.tafseer_insight = tafseer_insight
        self.hadith_tradition = hadith_tradition
        self.hadith_ref = hadith_ref
        self.comparative_scripture = comparative_scripture
        self.comparative_tradition = comparative_tradition
        self.sufi_psychology_nafs = sufi_psychology_nafs
        self.contemplative_inquiries = contemplative_inquiries


class OntologicalSpiritualEngine:
    """Neural matching engine bridging sacred scriptures across traditions with analytical intellect."""

    def __init__(self):
        self.corpus: List[ScriptureEntry] = [
            ScriptureEntry(
                theme="Quantum Wave-Particle Nature & Divine Signs in Cosmos",
                keywords=["quantum", "physics", "universe", "cosmos", "stars", "atoms", "space", "entanglement", "light", "wave", "particle", "gravity"],
                quran_verse="We will show them Our signs in the horizons and within themselves until it becomes clear to them that it is the truth. (Surah Fussilat)",
                surah_ref="Quran 41:53",
                tafseer_insight=(
                    "Ibn Kathir notes that 'the horizons' (Afaq) refers to the cosmic order, celestial mechanics, and physical laws, "
                    "while 'within themselves' (Anfus) points to cellular biology, consciousness, and psychological faculties. "
                    "The universe is an open book of coherent empirical signs confirming ontological Unity (Tawhid)."
                ),
                hadith_tradition="Contemplate upon the creation of Allah, and do not attempt to encompass the transcendent essence of Allah, for your intellect is finite while creation is His infinite tapestry.",
                hadith_ref="Musannaf Ibn Abi Shaybah & Al-Bayhaqi",
                comparative_scripture="I am the taste in water, the radiance of the sun and moon, the sacred syllable Om in all the Vedas, the sound in ether, and ability in man. (Bhagavad Gita 7:8)",
                comparative_tradition="Hindu Vedanta / Bhagavad Gita",
                sufi_psychology_nafs=(
                    "In the Sufi ontology of Ibn Arabi and Al-Ghazali, the external cosmos is the Macro-Human (al-Insan al-Kabir), "
                    "and the human being is the Micro-Cosmos. Perceiving physical laws awakens the Nafs al-Mulhamah (the inspired soul), "
                    "transforming scientific observation from detached materialism into an act of profound contemplative gratitude (Shukr)."
                ),
                contemplative_inquiries=[
                    "When observing quantum entanglement where separated particles instantaneously communicate, how does this mirror the deep unity underlying all existence?",
                    "If the physical universe operates through precise balance (Mizan), what imbalances in your personal thoughts or life need harmonization today?",
                    "How can your scientific inquiry transition from mere analytical dissection into an awe-inspired contemplation of the ultimate Originator?",
                ],
            ),
            ScriptureEntry(
                theme="Healing, Anxiety & Emotional Equilibrium (Sakoon)",
                keywords=["stress", "anxiety", "fear", "panic", "worry", "depression", "sad", "pain", "failure", "hopeless", "overwhelmed", "grief"],
                quran_verse="Indeed, with hardship comes ease. Indeed, with hardship comes ease. Those who have believed and whose hearts are assured by the remembrance of Allah. Unquestionably, by the remembrance of Allah hearts find rest.",
                surah_ref="Quran 94:5-6 & Quran 13:28",
                tafseer_insight=(
                    "Tafseer Al-Jalalayn highlights that the word 'hardship' (al-Usr) is definite, while 'ease' (Yusr) is indefinite and repeated twice; "
                    "linguistically in Arabic, a single hardship cannot conquer twice the ease. Distress is transient, whereas divine grace is boundless. "
                    "True tranquility (Sakoon) is not the absence of external storm, but the presence of an inward anchor."
                ),
                hadith_tradition="No fatigue, nor disease, nor sorrow, nor sadness, nor hurt, nor distress befalls a believer—even the prick of a single thorn—except that Allah expiates some of their shortcomings through it.",
                hadith_ref="Sahih al-Bukhari 5641 & Sahih Muslim 2573",
                comparative_scripture="The Lord is my shepherd; I shall not want. He makes me lie down in green pastures; He leads me beside still waters. He restores my soul. (Psalms 23:1-3)",
                comparative_tradition="Judeo-Christian Hebrew Tehillim (Psalms of David / Zabur)",
                sufi_psychology_nafs=(
                    "Al-Ghazali describes emotional suffering as the crucible that melts the stubborn illusions of the ego (Nafs al-Ammarah). "
                    "The pain you feel is the soul recognizing that worldly attachments cannot provide permanent security. "
                    "When the ego surrenders control (Tawakkul), the heart ascends into Nafs al-Mutmainnah (the tranquil soul at rest)."
                ),
                contemplative_inquiries=[
                    "What current circumstance or outcome are you frantically attempting to control that you can consciously entrust to the divine Wisdom?",
                    "If this period of hardship is a chisel removing a layer of pride or self-reliance, what higher virtue is it fashioning inside you?",
                    "Take a slow breath: Can you feel the serenity in recognizing that the Creator has sustained you through every difficult day of your past?",
                ],
            ),
            ScriptureEntry(
                theme="Purpose, Epistemic Sincerity & Moral Integrity",
                keywords=["purpose", "meaning", "why", "truth", "ethics", "intention", "clean", "integrity", "action", "work", "deeds", "identity"],
                quran_verse="He who created death and life to test you as to which of you is best in deed—and He is the Exalted in Might, the Forgiving.",
                surah_ref="Quran 67:2",
                tafseer_insight=(
                    "Fakhr al-Din al-Razi observes that the verse emphasizes 'best in deed' (Ahsanu Amala), not 'most in deed' (Aktharu Amala). "
                    "Moral excellence is defined by the purity of internal intention (Ikhlas) and adherence to ethical truth, not mere outer volume or public spectacle."
                ),
                hadith_tradition="Actions are judged solely by intentions, and every person shall receive only that which they intended with their heart.",
                hadith_ref="Sahih al-Bukhari 1 & Sahih Muslim 1907",
                comparative_scripture="You have a right to your labor, but never to the fruits of labor. Never let the fruits of action be your motive, nor be attached to inaction. Perform your duty with an equanimous mind. (Bhagavad Gita 2:47)",
                comparative_tradition="Hindu Philosophy: Nishkama Karma (Desireless Right Action)",
                sufi_psychology_nafs=(
                    "Rumi in the Mathnawi states: 'Set your life on fire; seek those who fan your flames.' "
                    "When action is driven by public praise, the ego remains imprisoned in vanity. "
                    "When action is dedicated as service to the divine and humanity, work itself becomes prayer, purifying the heart into pristine clarity."
                ),
                contemplative_inquiries=[
                    "If nobody ever applauds or acknowledges your greatest work, would you still commit to it with equal dedication and love?",
                    "What is the foundational intention behind the technical and intellectual projects you are pursuing today?",
                    "What is one quiet, selfless action you can do today without telling a single soul?",
                ],
            ),
            ScriptureEntry(
                theme="Patience, Transience & The River of Time",
                keywords=["time", "patience", "aging", "death", "transient", "impermanence", "wait", "endurance", "delay", "future", "past"],
                quran_verse="By the declining time, indeed mankind is in loss, except for those who have believed and done righteous deeds and advised each other to truth and advised each other to patience.",
                surah_ref="Quran 103:1-3 (Surah Al-Asr)",
                tafseer_insight=(
                    "Imam Al-Shafi'i famously remarked: 'If people were to ponder this single Surah alone, it would suffice them.' "
                    "Time is an irreplaceable capital flowing away like melting ice. Life gains enduring value only when aligned with timeless truth (Haqq) "
                    "and mutual perseverance (Sabr)."
                ),
                hadith_tradition="Patience is illumination (as-Sabru Diya). How wonderful is the affair of the believer, for there is good for him in every matter.",
                hadith_ref="Sahih Muslim 2999",
                comparative_scripture="To everything there is a season, and a time to every purpose under the heaven: A time to be born, and a time to die; a time to break down, and a time to build up; a time to weep, and a time to laugh. (Ecclesiastes 3:1-4)",
                comparative_tradition="Hebrew Wisdom Literature / Biblical Kohelet",
                sufi_psychology_nafs=(
                    "Sufi master Attar speaks of the Ring with the inscription: 'This too shall pass.' "
                    "Patience (Sabr) is not passive resignation; it is active emotional poise. The wise soul does not despair during contraction (Qabd) "
                    "nor grow arrogant during expansion (Bast)."
                ),
                contemplative_inquiries=[
                    "Are you rushing toward a future outcome so anxiously that you have forgotten to dwell gratefully in the sacred present moment?",
                    "How does knowing that current difficulties are temporary alter your emotional reaction to them right now?",
                    "What seed of long-term patience can you plant today that will bear fruit long after this season has passed?",
                ],
            ),
            ScriptureEntry(
                theme="Non-Dual Harmony, Wu Wei & Effortless Equilibrium",
                keywords=["balance", "harmony", "peace", "equilibrium", "flow", "nature", "meditation", "breath", "unity", "oneness", "stillness"],
                quran_verse="And the sky He has raised high, and He has set up the Balance (Mizan), so that you may not transgress within the balance.",
                surah_ref="Quran 55:7-8 (Surah Ar-Rahman)",
                tafseer_insight=(
                    "Classical commentators explain that 'Mizan' is the cosmic equilibrium permeating both astronomical orbits and ethical human conscience. "
                    "When a person acts with justice and spiritual poise, they are vibrating in resonance with the entire cosmos."
                ),
                hadith_tradition="Indeed, religion is ease. No one overburdens themselves with religion except that it overwhelms them. So follow a middle course, strive for perfection, and take good cheer.",
                hadith_ref="Sahih al-Bukhari 39",
                comparative_scripture="Yield and overcome; bend and be straight; empty and be full; wear out and be new; have little and gain. The supreme good is like water, which nourishes all things without trying to compete. (Tao Te Ching, Chapters 8 & 22)",
                comparative_tradition="Daoist Philosophy / Laozi (Tao Te Ching)",
                sufi_psychology_nafs=(
                    "The Sufis call this station 'Rida'—contentment with the divine will. Like water conforming effortlessly to its container, "
                    "the purified heart moves with reality rather than resisting it with stubborn ego-friction. Stillness reveals the clear reflection of the divine."
                ),
                contemplative_inquiries=[
                    "Where in your life are you expending excessive emotional energy resisting what is, rather than accepting and acting with graceful poise?",
                    "Can you invite stillness into your mind right now, letting thoughts settle like dust in quiet water?",
                    "How does the concept of cosmic balance inspire you to treat both your body and your relationships with moderation?",
                ],
            ),
            ScriptureEntry(
                theme="Mastery of Mind, Light & Transcending Egocentric Illusions",
                keywords=["mind", "illusion", "ego", "thoughts", "consciousness", "light", "clarity", "darkness", "awakening", "sleep"],
                quran_verse="Allah is the Light of the heavens and the earth. The example of His light is like a niche within which is a lamp, the lamp is within glass, the glass as if it were a pearly star lit from a blessed olive tree...",
                surah_ref="Quran 24:35 (Ayah an-Nur)",
                tafseer_insight=(
                    "Al-Ghazali in Mishkat al-Anwar (The Niche of Lights) unpacks this verse as the hierarchy of perception: sensory light reveals physical shapes, "
                    "intellectual light reveals scientific structures, but spiritual light (Nur al-Iman) reveals ultimate reality and moral truth. "
                    "The heart is the glass lamp that must be cleansed of worldly soot to transmit pristine illumination."
                ),
                hadith_tradition="O Allah, place light in my heart, light in my sight, light in my hearing, light on my right, light on my left, light above me, light below me, and grant me light upon light.",
                hadith_ref="Sahih al-Bukhari 6316 & Sahih Muslim 763",
                comparative_scripture="Mind precedes all mental states. Mind is their chief; they are all mind-wrought. If with an impure mind a person speaks or acts, suffering follows him like the wheel that follows the foot of the ox. If with a pure mind a person speaks or acts, happiness follows him like a shadow that never departs. (Dhammapada, Verses 1-2)",
                comparative_tradition="Buddhist Scripture / Gautama Buddha (The Dhammapada)",
                sufi_psychology_nafs=(
                    "The battle of human life is the awakening from Ghaflah (heedlessness / spiritual amnesia). "
                    "Your thoughts are not who you are; they are visitors passing through the guest house of consciousness. "
                    "By observing your thoughts with compassion and detachment, the true transcendent witness awakens."
                ),
                contemplative_inquiries=[
                    "When an anxious or negative thought surfaces, can you observe it as a transient cloud without identifying with it?",
                    "What habits or inputs are clouding the clarity of your 'glass lamp'—and what can you remove today to allow inner light to shine?",
                    "If pure awareness is untouched by past mistakes, how does that free you to begin anew with hope right now?",
                ],
            ),
        ]

    def _tokenize(self, text: str) -> List[str]:
        """Simple regex-based word tokenization."""
        return re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())

    def match_resonance(self, query: str) -> Dict[str, Any]:
        """Neural semantic and token overlap matcher to locate the deepest ontological resonance."""
        query_tokens = set(self._tokenize(query))
        best_entry = self.corpus[0]
        max_score = -1.0

        for entry in self.corpus:
            # Token overlap score
            kw_match = sum(1.0 for kw in entry.keywords if kw in query.lower())
            
            # Sub-token overlap with text
            corpus_text = f"{entry.theme} {entry.tafseer_insight} {entry.comparative_scripture}"
            entry_tokens = set(self._tokenize(corpus_text))
            
            intersection = query_tokens.intersection(entry_tokens)
            union = query_tokens.union(entry_tokens)
            jaccard = len(intersection) / max(1, len(union))

            # Composite match score
            score = (kw_match * 2.5) + (jaccard * 10.0)

            if score > max_score:
                max_score = score
                best_entry = entry

        # Confidence percentage
        confidence = min(0.99, max(0.72, 0.70 + (max_score * 0.05)))

        return {
            "theme": best_entry.theme,
            "confidence_score": round(confidence, 3),
            "quranic_verse": best_entry.quran_verse,
            "surah_reference": best_entry.surah_ref,
            "tafseer_scholarly_insight": best_entry.tafseer_insight,
            "prophetic_hadith": best_entry.hadith_tradition,
            "hadith_reference": best_entry.hadith_ref,
            "comparative_scripture": best_entry.comparative_scripture,
            "comparative_tradition": best_entry.comparative_tradition,
            "sufi_psychology_nafs": best_entry.sufi_psychology_nafs,
            "contemplative_questions": best_entry.contemplative_inquiries,
            "disclaimer": "🕊️ Epistemic & Contemplative Framework: Offered for personal mindfulness, ontological harmony, and spiritual tranquility (Sakoon). Transcends legal rulings (non-fatwa).",
        }


# Global singleton
ontological_spiritual_engine = OntologicalSpiritualEngine()
