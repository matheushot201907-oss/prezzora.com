"""Importa ofertas de um feed JSON autorizado, sem inventar preços."""
import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

SOURCE = os.environ.get("PREZZORA_FEED_URL", "").strip()
OUTPUT = Path("data/offers.json")

def main():
    if not SOURCE:
        print("PREZZORA_FEED_URL ausente: nenhuma atualização realizada.")
        return
    parsed = urlparse(SOURCE)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError("O feed precisa usar uma URL HTTPS válida.")
    req = urllib.request.Request(SOURCE, headers={"User-Agent": "PrezzoraPriceUpdater/1.0", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=25) as response:
        if response.status != 200:
            raise ValueError("Feed indisponível")
        raw = response.read(2_000_001)
        if len(raw) > 2_000_000:
            raise ValueError("Feed excede 2 MB")
    items = json.loads(raw)
    if not isinstance(items, list):
        raise ValueError("Feed deve conter uma lista JSON")
    checked_at = datetime.now(timezone.utc).isoformat()
    validated = []
    ids = set()
    for item in items[:1000]:
        if not isinstance(item, dict):
            raise ValueError("Produto inválido")
        identifier = str(item.get("id", "")).strip()
        name = str(item.get("name", "")).strip()
        store = str(item.get("store", "")).strip()
        url = str(item.get("url", "")).strip()
        price = item.get("price")
        if not identifier or not name or not store or identifier in ids:
            raise ValueError("ID, nome e loja são obrigatórios e IDs devem ser únicos")
        if not isinstance(price, (int, float)) or isinstance(price, bool) or not (0 < price < 100000000):
            raise ValueError("Preço inválido")
        if urlparse(url).scheme != "https" or not urlparse(url).hostname:
            raise ValueError("Link de produto deve usar HTTPS")
        ids.add(identifier)
        validated.append({"id": identifier, "name": name, "store": store, "url": url,
                          "price": round(price, 2), "checked_at": checked_at})
    if not validated:
        raise ValueError("Feed vazio: dados anteriores preservados")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps({"updated_at": checked_at, "products": validated},
                                 ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Atualizados {len(validated)} produtos.")

if __name__ == "__main__":
    main()
