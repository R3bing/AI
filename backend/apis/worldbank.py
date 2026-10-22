"""World Bank Indicators API Client for Quantum Knowledge Weaver.
Queries the global macroeconomic, development, poverty, energy, and GDP databases.
Keyless, open-access public API.
"""

from typing import List, Dict, Any
import httpx
from backend.apis.base import BaseAPIClient
from backend.orchestrator.models import SourceCitation


class WorldBankClient(BaseAPIClient):
    """Fetches global macroeconomic indicators, GDP, demographic, and development data from the World Bank."""

    # Common indicator codes for quick lookup
    INDICATOR_MAP = {
        "gdp": "NY.GDP.MKTP.CD",
        "economy": "NY.GDP.MKTP.CD",
        "inflation": "FP.CPI.TOTL.ZG",
        "poverty": "SI.POV.NAHC",
        "population": "SP.POP.TOTL",
        "energy": "EG.USE.PCAP.KG.OE",
        "carbon": "EN.ATM.CO2E.PC",
        "emissions": "EN.ATM.CO2E.PC",
        "climate": "EN.ATM.CO2E.PC",
        "health": "SH.XPD.CHEX.GD.ZS",
        "life expectancy": "SP.DYN.LE00.IN",
        "education": "SE.XPD.TOTL.GD.ZS",
    }

    def __init__(self):
        super().__init__(
            api_id="worldbank",
            name="World Bank Global Development Indicators",
            domain_tags=["economics", "gdp", "development", "macroeconomics", "poverty", "worldbank", "demographics", "energy"],
            base_url="https://api.worldbank.org/v2",
            avg_latency_ms=310.0,
            timeout_seconds=9.0,
        )
        self.headers = {
            "User-Agent": "QuantumKnowledgeWeaver/1.0 (mailto:econ@qkw.local)",
            "Accept": "application/json",
        }

    async def fetch(self, query: str, limit: int = 3) -> List[SourceCitation]:
        citations: List[SourceCitation] = []
        clean_q = query.strip().lower()

        # Determine best indicator code based on query keywords
        selected_ind = "NY.GDP.MKTP.CD"
        for kw, code in self.INDICATOR_MAP.items():
            if kw in clean_q:
                selected_ind = code
                break

        url = f"{self.base_url}/country/WLD;USA;CHN;IND;EUU/indicator/{selected_ind}"
        params = {
            "format": "json",
            "mrnev": 1,  # Most recent non-empty value
            "per_page": limit,
        }

        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout_seconds) as client:
                resp = await client.get(url, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    if isinstance(data, list) and len(data) >= 2:
                        records = data[1]
                        for rec in records[:limit]:
                            country = rec.get("country", {}).get("value", "World")
                            ind_name = rec.get("indicator", {}).get("value", "Economic Indicator")
                            val = rec.get("value")
                            date_str = rec.get("date", "Recent")

                            if val is not None:
                                val_formatted = f"{val:,.2f}" if isinstance(val, (int, float)) else str(val)
                            else:
                                val_formatted = "Data available in full survey"

                            snippet = f"World Bank Official Data ({country}, {date_str}): {ind_name} = {val_formatted}."

                            citations.append(
                                SourceCitation(
                                    title=f"World Bank [{country}]: {ind_name}",
                                    source=self.api_id,
                                    snippet=snippet,
                                    url=f"https://data.worldbank.org/indicator/{selected_ind}",
                                    raw_metadata={
                                        "country": country,
                                        "indicator_code": selected_ind,
                                        "indicator_name": ind_name,
                                        "value": val,
                                        "year": date_str,
                                    },
                                )
                            )
                    if citations:
                        return citations
        except Exception:
            pass

        return self._generate_fallback(query, limit)

    def _generate_fallback(self, query: str, limit: int) -> List[SourceCitation]:
        return [
            SourceCitation(
                title=f"World Bank Development Telemetry: {query.title()}",
                source=self.api_id,
                snippet=f"World Bank Global Open Data: Comprehensive macroeconomic, environmental sustainability, and demographic dataset for inquiry '{query}'.",
                url="https://data.worldbank.org",
                raw_metadata={"synthetic_fallback": True, "domain": "macroeconomics"},
            )
        ]
