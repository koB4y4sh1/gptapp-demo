# バックエンド

このディレクトリには、アプリケーションのバックエンド実装が含まれています。

## ディレクトリ構造

```
backend/
├── src/                        # ソースコード
│   ├── domain/                 # ドメイン層
│   │   ├── model/              # ドメインモデル
│   │   │   └── response_format/  # OpenAI APIレスポンス形式
│   │   ├── langgraph_workflow/ # LangGraphワークフロー
│   │   └── slides/             # スライド関連ロジック
│   ├── infrastructure/         # インフラストラクチャ層
│   └── interface/              # インターフェース層
├── logs/                       # ログファイル
├── .env                        # 環境変数
├── requirements.txt            # 依存関係
├── app.py                      # アプリケーションエントリーポイント
└── testapp.py                  # テスト用スクリプト
```

## 主要なコンポーネント

### 1. ドメイン層 (`src/domain/`)
- アプリケーションのコアビジネスロジック
- OpenAI APIとの連携
- スライド作成ワークフロー
- 詳細は[domain/README.md](src/domain/README.md)を参照

### 2. インフラストラクチャ層 (`src/infrastructure/`)
- データベース接続
- 外部サービスとの連携
- ロギング設定

### 3. インターフェース層 (`src/interface/`)
- APIエンドポイント
- リクエスト/レスポンスの処理
- エラーハンドリング

## 環境設定

1. 環境変数の設定
   ```bash
   cp .env.example .env
   # .envファイルを編集して必要な設定を行う
   ```

2. 依存関係のインストール
   ```bash
   pip install -r requirements.txt
   ```

## 実行方法

1. アプリケーションの起動
   ```bash
   python app.py
   ```

2. テスト実行
   ```bash
   python testapp.py
   ```

## 設計方針

1. **クリーンアーキテクチャ**
   - ドメイン層、インフラストラクチャ層、インターフェース層の明確な分離
   - 依存関係の方向を制御

2. **モジュール性**
   - 各コンポーネントは独立して動作可能
   - 明確な責任分担

3. **保守性**
   - 一貫したコーディング規約
   - 詳細なドキュメント
   - ログ出力の徹底 