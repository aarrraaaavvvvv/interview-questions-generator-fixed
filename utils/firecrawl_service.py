"""FireCrawl web scraping integration"""

from firecrawl import FirecrawlApp
from config import FIRECRAWL_MAX_PAGES, FIRECRAWL_TIMEOUT
from typing import List, Dict


class FireCrawlService:
    """Service for web scraping using FireCrawl API"""

    def __init__(self, api_key: str):
        """Initialize FireCrawl with API key"""
        self.client = FirecrawlApp(api_key=api_key)

    def scrape_url(self, url: str) -> str:
        """Scrape a single URL and return markdown content"""
        try:
            result = self.client.scrape_url(
                url,
                params={"formats": ["markdown"], "timeout": FIRECRAWL_TIMEOUT}
            )
            # SDK returns a dict; extract markdown content
            if isinstance(result, dict):
                return result.get("markdown", result.get("content", str(result)))
            return result.markdown if hasattr(result, "markdown") else str(result)
        except Exception as e:
            raise Exception(f"Error scraping URL {url}: {str(e)}")

    def search_and_scrape(self, search_query: str, max_results: int = 3) -> List[Dict]:
        """Search the web and scrape top results"""
        try:
            results = []
            search_results = self.client.search(search_query)

            # Handle different response formats
            if isinstance(search_results, dict) and "results" in search_results:
                search_results = search_results["results"]
            elif isinstance(search_results, dict) and "data" in search_results:
                search_results = search_results["data"]

            # Ensure it's iterable
            if not isinstance(search_results, list):
                search_results = list(search_results) if hasattr(search_results, "__iter__") else []

            for i, result in enumerate(search_results[:max_results]):
                try:
                    url = result.get("url") if isinstance(result, dict) else getattr(result, "url", "")
                    title = result.get("title") if isinstance(result, dict) else getattr(result, "title", "Unknown")

                    if not url:
                        continue

                    content = self.scrape_url(url)
                    results.append({
                        "url": url,
                        "title": title,
                        "content": content
                    })
                except Exception:
                    continue

            return results
        except Exception as e:
            raise Exception(f"Error searching and scraping: {str(e)}")
