# ドメイン層

このディレクトリには、アプリケーションのコアビジネスロジックとドメインモデルが含まれています。

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