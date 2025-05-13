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

### 2. レイアウトノード (`layout_node.py`)
- **目的**: スライドの構成を設計
- **入力**: タイトル、ヒアリング情報
- **出力**: 
  - ページ構成 (`pages`)

### 3. スライド作成ノード (`slide_creator_node.py`)
- **目的**: 具体的なスライド内容を作成
- **入力**: タイトル、レイアウト情報
- **出力**: 
  - ページ内容 (`pages`)

### 4. 画像生成ノード (`image_node.py`)
- **目的**: スライド内容に応じて画像を自動生成し、各スライドに画像URLまたはローカルパスを付与
- **入力**: スライド内容（`slide_json`）
- **出力**: 
  - `slide_json`: 各スライドの`images`欄に画像パスが追加されたスライドJSON

#### 画像生成APIの利用について
- OpenAI Image API（DALL·E 3）を利用
- 必要な環境変数:
  - `OPENAI_API_KEY` : OpenAIのAPIキー
  - `OPENAI_API_BASE` : APIエンドポイント（省略時はデフォルト）
- 生成画像は`temp/images/`配下に一時保存され、各スライドの`images`欄にローカルパスが格納される
- 失敗時はAPIの画像URLを格納

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
  "hearing_info": {
    "purpose": "Pythonの基礎について初心者に分かりやすく説明し、プログラミングの入門として活用できる資料を作成する。", 
    "target_audience": "プログラミング未経験者やPython初心者、基本的な文法や使い方を学びたい社会人・学生。", 
    "main_topics": [
      "Pythonとは？", 
      "Pythonの歴史", 
      "Pythonの活用分野", 
      "他言語との比較", 
    ]
  }
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
      "header": "Pythonの歴史",
      "template": "image",
      "description": "Pythonの歴史と発展を紹介する"
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
      "header": "プログラムの歴史",
      "content": "Pythonの歴史と発展を紹介する",
      "template": "image",
      "images": []
    },
    {
      "header": "活用分野",
      "content": "PythonはWeb開発やデータ分析など様々な分野で使われています。",
      "template": "three_images",
      "images": [],
      "captions": ["活用分野を説明するイラスト1", "Pの活用分野を説明するイラスト2", "活用分野を説明するイラスト3"],
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
#### image_nodeのstate["slide_json"]（imageとthree_imageが混在する場合）
```json
{
  "pages": [
    {
      "header": "プログラムの歴史",
      "content": "Pythonの歴史と発展を紹介する",
      "template": "image",
      "images": [
        "temp/images/slide1_img1.png"
      ]
    },
    {
      "header": "プログラムの歴史",
      "content": "Pythonの歴史と発展を紹介する",
      "template": "image",
      "images": ["data/images/slide1_img1.png"],
      "captions": ["説明するイラスト"],
    },
    {
      "header": "活用分野",
      "content": "PythonはWeb開発やデータ分析など様々な分野で使われています。",
      "template": "three_image",
      "images": [
        "data/images/slide2_img1.png",
        "data/images/slide2_img2.png",
        "data/images/slide2_img3.png"
      ],
      "captions": ["活用分野を説明するイラスト1", "Pの活用分野を説明するイラスト2", "活用分野を説明するイラスト3"],
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
    },
  ]
}
```
