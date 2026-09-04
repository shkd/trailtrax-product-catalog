# Trailtrax Product Catalog

商品カタログ（補給定番テンプレート）をアプリが取り込むための公開レポジトリです。

- 商品データの更新は PR ベースで行い、アプリ上で「商品カタログを更新」から明示的に反映します。
- 直近のデータは `catalog/v1/manifest.json` で公開されます。

運用フロー
1. `catalog/v1/products.json` の編集
2. `scripts/validate_catalog.py` を実行
3. 生成された `catalog/v1/manifest.json` を含めて PR を作成し、商品名・数値・公式出典をレビュー
4. マージ後、アプリから更新ボタンで取り込み

## データガイド

- `category` は `meal / trailFood / water / electrolyte / emergency / other`
- `unit` は `piece / serving / pack / milliliter`
- `status` は `active` または `discontinued`
- 実在商品にはメーカー公式ページの `sourceUrl` を必須とします。
- 推測値や未確認の商品は登録しません。
- アプリは自動更新せず、利用者が更新操作を行ったときだけ端末キャッシュを置き換えます。

## 開発時チェック

```bash
env PYTHONUNBUFFERED=1 python scripts/validate_catalog.py
```
