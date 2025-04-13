# ドメイン層

このディレクトリには、アプリケーションのコアビジネスロジックとドメインモデルが含まれています。

## 構造
- `slides/` - スライド生成に関連するドメインモデル
  - `base.py` - 基本スライドクラス
  - `text_slide.py` - テキストスライド
  - `image_slide.py` - 画像スライド
  - `three_image_slide.py` - 3画像スライド
  - `table_slide.py` - テーブルスライド
  - `three_horizontal_flow_slide.py` - フローチャートスライド

## 責務
- ビジネスルールの定義
- ドメインモデルの実装
- ビジネスロジックのカプセル化 