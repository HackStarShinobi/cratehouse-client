"""Unofficial client for https://docs.cratehouse.dev."""
import os
from typing import Dict, List, Optional

import requests

DEFAULT_BASE = "https://registry.cratehouse.dev/api"


class RegistryError(Exception):
    pass


class Registry:
    def __init__(self, api_key: Optional[str] = None,
                 base: str = DEFAULT_BASE):
        self.api_key = api_key or os.environ.get("CRATEHOUSE_API_KEY", "")
        if not self.api_key:
            raise RegistryError("API key required")
        self.base = base.rstrip("/")
        self._s = requests.Session()
        self._s.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def _get(self, path: str, **kw) -> Dict:
        r = self._s.get(f"{self.base}{path}", timeout=15, **kw)
        if r.status_code >= 400:
            raise RegistryError(f"{r.status_code}: {r.text[:200]}")
        return r.json()

    def search(self, query: str, limit: int = 20) -> List[Dict]:
        return self._get("/search", params={"q": query, "limit": limit})["hits"]

    def info(self, name: str) -> Dict:
        return self._get(f"/packages/{name}")

    def download_url(self, name: str, version: Optional[str] = None) -> str:
        meta = self.info(name)
        ver = version or meta["latest"]
        for f in meta["versions"][ver]["files"]:
            if f["filename"].endswith(".whl"):
                return f["url"]
        return meta["versions"][ver]["files"][0]["url"]
