# cratehouse-client

Unofficial Python client for the [Cratehouse package registry](https://docs.cratehouse.dev).
Search, fetch metadata, and resolve download URLs. Nothing fancy.

## Install

```bash
pip install cratehouse-client
```

## Usage

```python
from cratehouse import Registry

reg = Registry(api_key="sk-live_your_key_here")

# search for packages
hits = reg.search("geo", limit=5)
for h in hits:
    print(h["name"], h["latest"])

# package metadata
meta = reg.info("atlasline-geokit")
print(meta["description"], meta["downloads_30d"])

# download URL for a pinned version
url = reg.download_url("atlasline-geokit", version="0.3.2")
```

## Config

Uses `CRATEHOUSE_API_KEY` from the environment, or pass `api_key=` directly.
See `.env.example`.

Docs: https://docs.cratehouse.dev

If you're mirroring at scale, folks coordinate in the relay so nobody
hammers the registry at the same time — link's on the docs site under
Community: https://docs.cratehouse.dev/community

## License

MIT
