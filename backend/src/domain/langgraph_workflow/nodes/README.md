# ワークフローノード

このディレクトリには、LangGraphワークフローの各ノードの実装が含まれています。

## ノード一覧

### 1. ヒアリングノード (`hearing_node.py`)
- **目的**: 資料作成の目的と対象者を明確化
- **入力**: タイトル
- **出力**: 
  - 目的 (`purpose`)
  - 対象者 (`target_audience`)
  - 主要トピック (`main_topics`)
- **制約**:
  - 主要トピックは3-5個
  - 各トピックは簡潔かつ具体的に記載

### 2. レイアウトノード (`layout_node.py`)
- **目的**: スライドの構成を設計
- **入力**: タイトル、ヒアリング情報
- **出力**: 
  - ページ構成 (`pages`)
    - タイトル (`header`)
    - テンプレートタイプ (`template`)
    - 説明 (`description`)
- **制約**:
  - スライドは1-10枚
  - テンプレートタイプは"text"のみ

### 3. スライド作成ノード (`slide_creator_node.py`)
- **目的**: 具体的なスライド内容を作成
- **入力**: タイトル、レイアウト情報
- **出力**: 
  - ページ内容 (`pages`)
    - タイトル (`header`)
    - 内容 (`content`)
    - テンプレートタイプ (`template`)
- **制約**:
  - スライドは1-10枚
  - テンプレートタイプは"text"のみ
  - 内容は簡潔かつ具体的に記載

## 設計方針

1. **独立性**
   - 各ノードは独立して動作可能
   - 入力と出力の形式が明確に定義

2. **エラーハンドリング**
   - 必須パラメータの検証
   - JSON解析エラーの適切な処理

3. **再利用性**
   - 共通のスキーマ定義を使用
   - モジュール化された実装

## 構造
- `nodes/` - スライド生成に関連するドメインモデル
  - `hearing_node.py` - ユーザー入力のテーマから「どんな資料を作りたいか？」をChatGPTに聞いて補完する
  - `layout_node.py` - 得た情報をもとにページをLLMに作らせる
  - `image_slide.py` - 画像スライド
  - `three_image_slide.py` - 3画像スライド
  - `table_slide.py` - テーブルスライド
  - `three_horizontal_flow_slide.py` - フローチャートスライド

## 出力例
### hearing_node.pyのstate["title"]
```JSON
{
  "title": "Pythonの基礎",
  "hearing_info": "この資料はプログラミング初心者に向けてPythonの概要と基本構文を紹介..."
}
```

### layout_node.pyのstate["layout"]
```JSON
{
  "pages": [
    {
      "header": "Pythonとは？",
      "template": "text",
      "description": "Pythonの概要と特徴を紹介する"
    },
    {
      "header": "Pythonの活用分野",
      "template": "three_images",
      "description": "Pythonが使われる具体的な分野を視覚的に示す"
    },
    {
      "header": "他言語との比較",
      "template": "table",
      "description": "JavaやC++と比較してPythonの利点を説明する"
    }
  ]
}
```

### slide_creator_node.pyのstate["slide_json"]
```JSON
{
  "pages": [
    {
      "header": "Pythonとは？",
      "content": "Pythonはシンプルで読みやすい構文を持つプログラミング言語です。",
      "template": "text"
    },
    {
      "header": "活用分野",
      "content": "PythonはWeb開発やデータ分析など様々な分野で使われています。",
      "template": "three_images",
      "images": ["web.png", "data.png", "ml.png"]
    },
    {
      "header": "他言語との比較",
      "content": "以下は主要な言語との比較表です。",
      "template": "table",
      "table": [
        ["言語", "用途", "学習難易度"],
        ["Python", "汎用", "易しい"],
        ["Java", "業務アプリ", "中"],
        ["C++", "システム", "難しい"]
      ]
    }
  ]
}
```