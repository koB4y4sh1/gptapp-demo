# バックエンド

このディレクトリはPowerPointスライド生成アプリケーションのバックエンドを含んでいます。

## ディレクトリ構造
- `src/` - アプリケーションのソースコード
- `logs/` - アプリケーションログファイル
- `.venv/` - Python仮想環境
- `requirements.txt` - Pythonパッケージの依存関係
- `app.py` - アプリケーションのエントリーポイント
- `.env` - 環境変数設定ファイル

## セットアップ
1. Python仮想環境の作成とアクティベート:
```bash
python -m venv .venv
source .venv/bin/activate  # Linuxの場合
.venv\Scripts\activate     # Windowsの場合
```

2. 依存パッケージのインストール:
```bash
pip install -r requirements.txt
```

3. 環境変数の設定:
`.env`ファイルを作成し、必要な環境変数を設定してください。

4. アプリケーションの起動:
```bash
python app.py
``` 