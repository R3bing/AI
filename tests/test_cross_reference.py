"""Unit tests for the cross-referencing and semantic similarity layer in QKW.
"""

from backend.cross_reference.comparator import cross_referencer
from backend.orchestrator.models import SourceCitation


def test_cross_reference_comparison():
    citations = [
        SourceCitation(
            source_id="c1",
            source_name="PubMed",
            title="Medical hygiene and washing",
            snippet="Cleanliness and regular hand washing prevent transmission of infectious pathogens.",
            relevance_score=0.9,
        ),
        SourceCitation(
            source_id="c2",
            source_name="Hadith Traditions",
            title="Sahih Muslim 223",
            snippet="Cleanliness and personal hygiene are half of faith and crucial for human wellbeing.",
            relevance_score=0.9,
        ),
        SourceCitation(
            source_id="c3",
            source_name="arXiv",
            title="Superconducting Transmon Qubits",
            snippet="Josephson junctions provide non-linear inductance essential for artificial atom energy level spacing.",
            relevance_score=0.8,
        ),
    ]

    connections = cross_referencer.compare_citations(citations)

    assert len(connections) >= 1
    # Check that highest similarity is between hygiene and cleanliness
    best_connection = connections[0]
    assert ("PubMed" in best_connection.source_a_name and "Hadith" in best_connection.source_b_name) or \
           ("Hadith" in best_connection.source_a_name and "PubMed" in best_connection.source_b_name)
    assert best_connection.relationship in ["corroborates", "complements"]
    assert best_connection.similarity_score > 0.2
