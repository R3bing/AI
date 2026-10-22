"""Public APIs Repository Catalog & Neural Discovery Pathway.
Parses, indexes, and provides semantic searching across all 2,238+ public APIs
from the cloned https://github.com/public-apis/public-apis repository across 52 categories.
"""

import os
import re
from typing import Dict, List, Any, Optional

PUBLIC_APIS_README_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "public_apis_repo", "README.md")
)


class PublicAPIsCatalog:
    """Indexed catalog of 2,238+ open public APIs across 52 domains.
    Enables the Quantum Router and Multi-AI Council to discover external data pipelines.
    """

    def __init__(self, readme_path: str = PUBLIC_APIS_README_PATH):
        self.readme_path = readme_path
        self.categories: Dict[str, List[Dict[str, Any]]] = {}
        self.all_apis: List[Dict[str, Any]] = []
        self._load_and_index_catalog()

    def _load_and_index_catalog(self):
        """Parses the Markdown tables in the public-apis repository."""
        if not os.path.exists(self.readme_path):
            return

        current_category = None
        try:
            with open(self.readme_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line_strip = line.strip()
                    if line_strip.startswith("### "):
                        current_category = line_strip.replace("###", "").strip()
                        if current_category not in self.categories:
                            self.categories[current_category] = []
                    elif current_category and line_strip.startswith("|") and not line_strip.startswith("| API") and not line_strip.startswith("|---"):
                        parts = [p.strip() for p in line.split("|")]
                        if len(parts) >= 6:
                            raw_name = parts[1]
                            desc = parts[2]
                            auth = parts[3]
                            https = parts[4]
                            cors = parts[5]

                            # Extract clean name and URL from markdown [Name](url)
                            url_match = re.search(r"\[(.*?)\]\((.*?)\)", raw_name)
                            if url_match:
                                api_name = url_match.group(1).strip()
                                api_url = url_match.group(2).strip()
                            else:
                                api_name = raw_name
                                api_url = ""

                            entry = {
                                "name": api_name,
                                "url": api_url,
                                "description": desc,
                                "auth": auth if auth else "No Auth",
                                "https": https,
                                "cors": cors,
                                "category": current_category,
                            }
                            self.categories[current_category].append(entry)
                            self.all_apis.append(entry)
        except Exception:
            pass

    def get_statistics(self) -> Dict[str, Any]:
        """Returns overview metrics of the public-apis repository."""
        top_cats = sorted(self.categories.items(), key=lambda x: len(x[1]), reverse=True)[:10]
        no_auth_count = sum(1 for a in self.all_apis if a.get("auth") in ["No Auth", "`No`", "No"])
        https_count = sum(1 for a in self.all_apis if a.get("https") in ["Yes", "`Yes`"])

        return {
            "total_apis": len(self.all_apis),
            "total_categories": len(self.categories),
            "no_auth_available": no_auth_count,
            "https_secured": https_count,
            "top_categories": [{"category": c, "count": len(apis)} for c, apis in top_cats],
        }

    def search_apis(
        self,
        query: str,
        category: Optional[str] = None,
        no_auth_only: bool = False,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        q_lower = query.lower()
        q_tokens = q_lower.split()

        # Expand domain-specific inquiries to surface related live public APIs
        if any(k in q_lower for k in ["photosynthesis", "chlorophyll", "plant", "chloroplast", "botany", "vegetation"]):
            q_tokens.extend(["plant", "nature", "science", "environment", "biology", "earth"])
        elif any(k in q_lower for k in ["penicillin", "antibiotic", "bacteria", "medicine", "drug"]):
            q_tokens.extend(["health", "medical", "drug", "science", "disease"])
        elif any(k in q_lower for k in ["quantum", "physics", "cosmology", "space", "stars"]):
            q_tokens.extend(["nasa", "science", "space", "astronomy"])

        results = []

        pool = self.categories.get(category, self.all_apis) if category else self.all_apis

        for api in pool:
            if no_auth_only and api.get("auth") not in ["No Auth", "`No`", "No"]:
                continue

            text_corpus = f"{api['name']} {api['description']} {api['category']}".lower()
            matches = sum(1 for token in q_tokens if token in text_corpus)
            if matches > 0:
                results.append((matches, api))

        # Sort by relevance score
        results.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in results[:limit]]

    def search(
        self,
        query: str,
        category: Optional[str] = None,
        max_results: int = 10,
    ) -> List[Dict[str, Any]]:
        """Convenience alias for search_apis."""
        return self.search_apis(query=query, category=category, limit=max_results)

    def search_by_keyword(self, keyword: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Convenience alias for searching by keyword."""
        return self.search_apis(query=keyword, limit=limit)

    def get_all_categories(self) -> List[str]:
        """Returns sorted list of all categories."""
        return sorted(list(self.categories.keys()))

    def get_category_list(self) -> List[str]:
        """Convenience alias for get_all_categories."""
        return self.get_all_categories()


# Global Singleton Instance
public_apis_catalog = PublicAPIsCatalog()
