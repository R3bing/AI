"""PubChem Chemical Database API Client for Quantum Knowledge Weaver.
Queries the NIH National Center for Biotechnology Information (NCBI) PubChem PUG-REST API for molecular structures and chemical data.
"""

from typing import List
import httpx
from backend.apis.base import BaseAPIClient
from backend.orchestrator.models import SourceCitation


class PubChemClient(BaseAPIClient):
    """Fetches chemical formulas, molecular weights, pharmacological descriptions, and bioactivity from NIH PubChem."""

    def __init__(self):
        super().__init__(
            api_id="pubchem",
            name="PubChem NIH Chemical Database",
            domain_tags=["chemistry", "chemical", "molecules", "pharmacology", "drugs", "biochemistry", "materials", "compound"],
            base_url="https://pubchem.ncbi.nlm.nih.gov/rest/pug",
            avg_latency_ms=360.0,
            timeout_seconds=9.0,
        )
        self.headers = {
            "User-Agent": "QuantumKnowledgeWeaver/1.0 (https://github.com/qkw)"
        }

    async def fetch(self, query: str, limit: int = 3) -> List[SourceCitation]:
        citations: List[SourceCitation] = []
        clean_name = query.split()[0].strip()  # take primary term

        async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout_seconds) as client:
            # 1. Try description endpoint
            desc_url = f"{self.base_url}/compound/name/{clean_name}/description/JSON"
            try:
                resp = await client.get(desc_url)
                if resp.status_code == 200:
                    data = resp.json()
                    info_list = data.get("InformationList", {}).get("Information", [])
                    for info in info_list[:limit]:
                        cid = info.get("CID")
                        title = info.get("Title", clean_name.capitalize())
                        description = info.get("Description", "")
                        source_db = info.get("DescriptionSourceName", "PubChem")

                        if description:
                            url = f"https://pubchem.ncbi.nlm.nih.gov/compound/{cid}"
                            citations.append(
                                SourceCitation(
                                    source_id=f"pubchem-{cid}",
                                    source_name=self.name,
                                    title=f"{title} (CID: {cid})",
                                    url=url,
                                    snippet=description[:380] + "..." if len(description) > 380 else description,
                                    relevance_score=0.93,
                                    extra_metadata={"cid": cid, "source": source_db},
                                )
                            )
            except Exception:
                pass

            # 2. If no descriptions, query compound properties
            if not citations:
                prop_url = f"{self.base_url}/compound/name/{clean_name}/property/MolecularFormula,MolecularWeight,IUPACName,Title/JSON"
                try:
                    p_resp = await client.get(prop_url)
                    if p_resp.status_code == 200:
                        p_data = p_resp.json()
                        props = p_data.get("PropertyTable", {}).get("Properties", [])
                        for prop in props[:limit]:
                            cid = prop.get("CID")
                            iupac = prop.get("IUPACName", "Chemical compound")
                            formula = prop.get("MolecularFormula", "")
                            mw = prop.get("MolecularWeight", "")
                            title = prop.get("Title", clean_name)

                            snippet = f"Formula: {formula} | Molecular Weight: {mw} g/mol | IUPAC Name: {iupac}."
                            url = f"https://pubchem.ncbi.nlm.nih.gov/compound/{cid}"

                            citations.append(
                                SourceCitation(
                                    source_id=f"pubchem-{cid}",
                                    source_name=self.name,
                                    title=f"{title} (CID: {cid})",
                                    url=url,
                                    snippet=snippet,
                                    relevance_score=0.90,
                                    extra_metadata={"cid": cid, "formula": formula, "mw": mw},
                                )
                            )
                except Exception:
                    pass

        return citations
