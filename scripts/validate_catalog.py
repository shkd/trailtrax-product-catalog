#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

base = Path(__file__).resolve().parent.parent
products_path = base / "catalog" / "v1" / "products.json"
manifest_path = base / "catalog" / "v1" / "manifest.json"

try:
    raw = products_path.read_text(encoding="utf-8")
except Exception as exc:
    raise SystemExit(f"products.json を読み込めませんでした: {exc}")

try:
    payload = json.loads(raw)
except Exception as exc:
    raise SystemExit(f"JSON解析エラー: {exc}")

required_keys = {"version", "updatedAt", "products"}
if not required_keys.issubset(payload):
    raise SystemExit("products.json は version/updatedAt/products を必要とします")

if not isinstance(payload.get("products"), list):
    raise SystemExit("products は配列である必要があります")

allowed_categories = {"meal", "trailFood", "water", "electrolyte", "emergency", "other"}
allowed_units = {"piece", "serving", "pack", "milliliter"}
allowed_statuses = {"active", "discontinued"}
seen_ids = set()

for index, item in enumerate(payload["products"], start=1):
    for key in ["id", "manufacturer", "brand", "name", "category", "unit",
                "recommendedQuantity", "unitWeightGrams", "caloriesPerUnit", "status",
                "sourceUrl"]:
        if key not in item:
            raise SystemExit(f"[{index}] {key} が不足しています")
    if item["id"] in seen_ids:
        raise SystemExit(f"[{index}] id が重複しています: {item['id']}")
    seen_ids.add(item["id"])
    if item["category"] not in allowed_categories:
        raise SystemExit(f"[{index}] category が不正です")
    if item["unit"] not in allowed_units:
        raise SystemExit(f"[{index}] unit が不正です")
    if item["status"] not in allowed_statuses:
        raise SystemExit(f"[{index}] status が不正です")
    if not str(item["sourceUrl"]).startswith("https://"):
        raise SystemExit(f"[{index}] sourceUrl は公式HTTPS URLが必要です")
    for key in ["recommendedQuantity", "unitWeightGrams", "caloriesPerUnit"]:
        if not isinstance(item[key], (int, float)) or item[key] < 0:
            raise SystemExit(f"[{index}] {key} は0以上の数値が必要です")

checksums = hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
manifest = {
    "version": payload.get("version", "1.0.0"),
    "updatedAt": now,
    "source": "catalog/v1/products.json",
    "productCount": len(payload["products"]),
    "checksumSha256": checksums,
}
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Validated {len(payload['products'])} products")
print(f"checksum: {checksums}")
