# ドメインモデル

このディレクトリには、アプリケーションのコアとなるドメインモデルが含まれています。

## ディレクトリ構造

```
model/
├── response_format/        # OpenAI APIのレスポンス形式定義
│   ├── hearing_schema.py   # ヒアリング用スキーマ
│   ├── layout_schema.py    # レイアウト用スキーマ
│   └── slide_creator_schema.py  # スライド作成用スキーマ
└── ...                     # その他のドメインモデル
```

## スキーマ定義

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

## 設計方針

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