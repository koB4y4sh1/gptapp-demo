# ドメイン層

このディレクトリは、アプリケーションのコアとなるドメインロジックを実装しています。

## ディレクトリ構造

```
domain/
├── model/                      # ドメインモデル
│   ├── response_format/        # OpenAI APIのレスポンス形式定義
│   │   ├── hearing_schema.py   # ヒアリング用スキーマ
│   │   ├── layout_schema.py    # レイアウト用スキーマ
│   │   └── slide_creator_schema.py  # スライド作成用スキーマ
│   └── ...                     # その他のドメインモデル
├── langgraph_workflow/         # LangGraphワークフロー
│   ├── nodes/                  # ワークフローの各ノード
│   │   ├── hearing_node.py     # ヒアリングノード
│   │   ├── layout_node.py      # レイアウトノード
│   │   └── slide_creator_node.py  # スライド作成ノード
│   └── workflow.py             # ワークフロー定義
└── slides/                     # スライド関連のドメインロジック
```

## 主要なコンポーネント

### 1. ドメインモデル (`model/`)
- アプリケーションのコアとなるデータ構造とビジネスロジックを定義
- OpenAI APIのレスポンス形式を定義するスキーマを管理
  - 各スキーマは独立したファイルで管理され、再利用可能
  - スキーマは`response_format`ディレクトリに集約

### 2. LangGraphワークフロー (`langgraph_workflow/`)
- スライド作成プロセスをワークフローとして実装
- 各ノードは独立した機能を持ち、特定のタスクを実行
  - `hearing_node`: 資料の目的と対象者をヒアリング
  - `layout_node`: スライドの構成を設計
  - `slide_creator_node`: 具体的なスライド内容を作成

### 3. スライド関連ロジック (`slides/`)
- スライドの生成や管理に関するドメインロジック
- PowerPointファイルの操作や変換機能を提供

## 設計方針

1. **関心の分離**
   - 各コンポーネントは単一の責任を持つ
   - スキーマ定義は独立したファイルで管理

2. **再利用性**
   - 共通のスキーマ定義は`response_format`ディレクトリに集約
   - 各ノードは独立して動作可能

3. **保守性**
   - 明確なディレクトリ構造
   - 一貫した命名規則
   - 詳細なドキュメント

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