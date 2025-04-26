# ドメイン層

このディレクトリは、AIを活用したプレゼンテーション自動生成アプリケーションのコアとなるドメインロジックを実装しています。ドメイン層はアプリケーションの中心的な部分であり、ビジネスルールとロジックを表現します。

## ディレクトリ構造

```
model/                      # ドメインモデル
├── response_format/        # OpenAI APIのレスポンス形式定義
│   ├── hearing_schema.py   # ヒアリングノードのスキーマ
│   ├── layout_schema.py    # レイアウトノードのスキーマ
│   ├── schema.py           # 共通スキーマ定義
│   └── slide_creator_schema.py # スライド作成ノードのスキーマ
└──slides/                     # スライド関連のドメインロジック
    ├── base.py                 # 基本スライドクラス
    ├── image_slide.py          # 画像スライド
    ├── table_slide.py          # テーブルスライド
    ├── text_slide.py           # テキストスライド
    ├── three_horizontal_flow_slide.py # フローチャートスライド
    └── three_image_slide.py    # 3画像スライド
```

## スキーマ定義 (`response_format/`)

### 1. ヒアリングスキーマ (`hearing_schema.py`)
- **目的**: ヒアリングノードのレスポンス形式を定義
- **構造**:
  ```json
  {
    "purpose": "string",
    "target_audience": "string",
    "main_topics": ["string"]
  }
  ```

### 2. レイアウトスキーマ (`layout_schema.py`)
- **目的**: レイアウトノードのレスポンス形式を定義
- **構造**:
  ```json
  {
    "pages": [
      {
        "header": "string",
        "template": "text",
        "description": "string"
      }
    ]
  }
  ```

### 3. スライド作成スキーマ (`slide_creator_schema.py`)
- **目的**: スライド作成ノードのレスポンス形式を定義
- **構造**:
  ```json
  {
    "pages": [
      {
        "header": "string",
        "content": "string",
        "template": "text"
      }
    ]
  }
  ```

### 設計方針

1. **一貫性**
   - すべてのスキーマは同じ基本構造を持つ
   - 命名規則の統一
   - 型定義の明確化

2. **再利用性**
   - 各スキーマは独立したファイルで管理
   - 共通の構造は可能な限り再利用

3. **保守性**
   - 明確なドキュメント
   - バージョン管理
   - 変更履歴の追跡 

##  スライド関連ロジック (`slides/`)
- スライドの生成や管理に関するドメインロジック
- PowerPointファイルの操作や変換機能を提供

### 構造
- `slides/` - スライド生成に関連するドメインモデル
  - `base.py` - 基本スライドクラス
  - `text_slide.py` - テキストスライド
  - `image_slide.py` - 画像スライド
  - `three_image_slide.py` - 3画像スライド
  - `table_slide.py` - テーブルスライド
  - `three_horizontal_flow_slide.py` - フローチャートスライド