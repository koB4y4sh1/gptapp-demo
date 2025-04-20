# ソースコード

このディレクトリには、AIを活用したプレゼンテーション自動生成アプリケーションの主要なソースコードが含まれています。

## ディレクトリ構造
```
src/
├── application/        # アプリケーションサービス層
│   ├── generate_slide.py  # スライド生成ロジック
│   └── slide_storage.py   # スライド保存・取得機能
├── domain/             # ドメインモデルとビジネスロジック
│   ├── langgraph_workflow/  # LangGraphワークフロー
│   ├── model/             # データモデル
│   └── slides/            # スライドテンプレート
├── interfaces/         # 外部システムとの連携
│   └── client/           # 外部サービスクライアント
├── routes/             # APIエンドポイントの定義
│   ├── generate.py       # 生成エンドポイント
│   └── confirm.py        # 確認エンドポイント
└── utils/              # ユーティリティ関数とヘルパー
    └── logger.py         # ロギング設定
```

## アーキテクチャ概要

このアプリケーションはクリーンアーキテクチャの原則に従って構築されています：

1. **ドメイン層（`domain/`）**
   - アプリケーションの中核となるビジネスロジックとエンティティ
   - 外部依存のない純粋なビジネスルール
   - LangGraphを活用したAIワークフロー
   - スライドモデルとテンプレート定義

2. **アプリケーション層（`application/`）**
   - ユースケースの実装
   - ドメイン層のオーケストレーション
   - トランザクション管理
   - ビジネスルールの適用

3. **インターフェース層（`interfaces/`）**
   - 外部システム（データベース、API等）との連携
   - データ変換とマッピング
   - 外部サービスのアダプター

4. **プレゼンテーション層（`routes/`）**
   - APIエンドポイントの定義
   - リクエスト/レスポンスの処理
   - 入力バリデーション
   - エラーハンドリング

## データフロー

1. クライアントからのリクエストが `routes/` 層で受け取られる
2. リクエストデータが検証され、アプリケーション層に渡される
3. アプリケーション層がユースケースを実行し、必要に応じてドメイン層のサービスを呼び出す
4. ドメイン層がビジネスロジックを実行（LangGraphワークフローの実行など）
5. 結果がアプリケーション層に返され、必要に応じてインターフェース層を通じて永続化される
6. 処理結果がルート層を通じてクライアントに返される

## 生成AIとの連携ポイント

このアプリケーションでは、以下の方法で生成AIを活用しています：

1. **LangGraphワークフロー**
   - 複雑なAIタスクを小さなステップに分割
   - 各ステップで特化したプロンプトを使用
   - 構造化出力の強制とバリデーション

2. **スキーマ定義**
   - AIの出力を制約するためのJSONスキーマ
   - 一貫した出力形式の保証
   - エラー検出と修正メカニズム

3. **テンプレートシステム**
   - AIが生成したコンテンツを視覚的に表現するためのテンプレート
   - 異なるスライドタイプに対応する柔軟な設計
   - コンテンツと表示の分離

## 開発ガイド

### 新しいエンドポイントの追加

```python
# routes/new_endpoint.py
from fastapi import APIRouter, Depends
from backend.src.application.some_service import SomeService

router = APIRouter()

@router.post("/new-feature")
async def new_feature(request_data: RequestModel):
    # アプリケーションサービスの呼び出し
    result = SomeService().execute(request_data)
    return {"status": "success", "data": result}
```

### 新しいワークフローノードの追加

```python
# domain/langgraph_workflow/nodes/new_node.py
from langchain.schema import BaseOutputParser
from backend.src.domain.model.response_format.schema import SomeSchema

async def new_node(state):
    # 前のノードからの入力を取得
    input_data = state.get("previous_output", {})
    
    # LLMを使用した処理
    response = await llm.ainvoke(
        create_prompt_for_node(input_data)
    )
    
    # 出力のパース
    parsed_output = SomeOutputParser().parse(response)
    
    # 状態の更新
    return {"new_output": parsed_output}

class SomeOutputParser(BaseOutputParser):
    def parse(self, text):
        # テキスト出力を構造化データに変換
        # ...
        return parsed_data
```

## テスト戦略

1. **ユニットテスト**
   - 各レイヤーの個別コンポーネントをテスト
   - モックを使用して外部依存を分離

2. **統合テスト**
   - レイヤー間の連携をテスト
   - 実際のデータフローを検証

3. **E2Eテスト**
   - 完全なユーザーフローをテスト
   - 実際のAPIエンドポイントを使用

## 生成AIを活用したコード拡張例

以下は、生成AIを使用してこのコードベースを拡張する例です：

1. **新しいスライドテンプレートの追加**
   ```python
   # 指示: "4分割画像スライドテンプレートを追加してください"
   # 生成されるコード:
   # domain/slides/four_image_slide.py
   from backend.src.domain.slides.base import BaseSlide
   
   class FourImageSlide(BaseSlide):
       """4つの画像を表示するスライドテンプレート"""
       
       def __init__(self, header, content, images):
           super().__init__(header, content)
           self.images = images[:4]  # 最大4つの画像
           
       def generate(self, prs, slide_layout):
           slide = prs.add_slide(slide_layout)
           # ヘッダーの設定
           self._set_header(slide)
           # コンテンツの設定
           self._set_content(slide)
           # 4つの画像を配置
           self._set_images(slide)
           return slide
           
       def _set_images(self, slide):
           # 画像の配置ロジック
           # ...
   ```

2. **新しいワークフローノードの追加**
   ```python
   # 指示: "画像生成ノードを追加してください"
   # 生成されるコード:
   # domain/langgraph_workflow/nodes/image_generation_node.py
   async def image_generation_node(state):
       """スライド内容に基づいて画像を生成するノード"""
       slide_data = state.get("slide_json", {})
       
       # 画像が必要なスライドを特定
       slides_needing_images = [
           slide for slide in slide_data.get("pages", [])
           if slide.get("template") in ["image", "three_images", "four_images"]
       ]
       
       # 各スライドに必要な画像を生成
       for slide in slides_needing_images:
           # 画像生成ロジック
           # ...
           
       # 更新されたスライドデータを返す
       return {"slide_json": slide_data}
   ```

## パフォーマンス最適化

1. **非同期処理**
   - FastAPIの非同期機能を活用
   - 長時間実行タスクの適切な処理

2. **キャッシング**
   - 頻繁に使用されるデータのキャッシング
   - 重複計算の回避

3. **バッチ処理**
   - 複数のAI呼び出しをバッチ化
   - リソース使用の最適化
