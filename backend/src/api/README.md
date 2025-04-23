# ルート定義

このディレクトリには、APIエンドポイントの定義が含まれています。

## エンドポイント
- `/generate` - PowerPointスライドの生成エンドポイント
- `/confirm` - スライド生成結果の確定・pptxダウンロードエンドポイント

## 責務
- HTTPリクエストの処理
- リクエストのバリデーション
- レスポンスの形成
- エラーハンドリング 

---

## API仕様

### POST `/generate`

#### リクエスト例

```json
{
  "title": "営業戦略2024"
}
```

#### レスポンス例（成功時）

```json
{
  "session_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "preview": [
    {
      "title": "営業戦略2024",
      "content": "本資料では2024年度の営業戦略について説明します。"
    },
    {
      "title": "市場分析",
      "content": "市場動向・競合状況の分析結果をまとめます。"
    }
    // ...以降スライド構成
  ]
}
```

#### レスポンス例（エラー時）

```json
{
  "error": "タイトルが指定されていません"
}
```

---

### POST `/confirm`

#### リクエスト例

```json
{
  "session_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "confirmed": true
}
```

#### レスポンス

- 成功時: PowerPointファイル（`application/vnd.openxmlformats-officedocument.presentationml.presentation`としてバイナリ送信）
- 失敗時: 

```json
{
  "error": "セッションが存在しません"
}
```
