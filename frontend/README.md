# フロントエンド

このディレクトリはPowerPointスライド生成アプリケーションのフロントエンドを含んでいます。

## 技術スタック
- React
- TypeScript
- Tailwind CSS
- Vite
- Remix

## ディレクトリ構造
- `app/` - アプリケーションのメインコード
- `public/` - 静的アセット
- `node_modules/` - 依存パッケージ
- `app/interfaces/` - API通信や外部サービス連携などのインターフェース層ロジック
    - `chat/` - チャット・スライド生成API呼び出し関数（generateSlide.ts, confirmSlide.ts など）

## 設定ファイル
- `vite.config.ts` - Viteの設定
- `tsconfig.json` - TypeScriptの設定
- `tailwind.config.ts` - Tailwind CSSの設定
- `.eslintrc.cjs` - ESLintの設定
- `postcss.config.js` - PostCSSの設定

---

## アプリケーション構成

### app ディレクトリ

- `components/`  
  UIコンポーネントをまとめたディレクトリです。再利用性の高い部品が格納されています。
  - `Chat.tsx`  
    チャット画面のUI部品。状態管理やAPI通信のロジックは持たず、propsで受け取った内容を表示します。
  - `ChatInput.tsx`  
    ユーザーがメッセージを入力するための入力欄コンポーネントです。
  - `ChatMessage.tsx`  
    個々のチャットメッセージを表示するコンポーネントです。
  - `ChatMessageList.tsx`  
    複数のチャットメッセージをリスト表示するコンポーネントです。
  - `InputField.tsx`  
    汎用的な入力フィールドコンポーネントです。フォームなどで利用されます。
  - `PageForm.tsx`  
    PowerPointページ作成用のフォームコンポーネントです。

- `pages/`  
  画面単位のページコンポーネントを格納しています。ルーティングのエントリーポイントとなります。
  - `ChatPage.tsx`  
    チャット機能のページコンポーネント。状態管理やAPI通信ロジックを持ち、UI部品（Chat.tsx等）とAPI層（interfaces/chat/）を組み合わせてページを構成します。
  - `PowerPointPage.tsx`  
    PowerPoint生成機能のページコンポーネントです。

- `routes/`  
  Remixのルーティングに対応したファイルを格納しています。URLごとの画面遷移やAPIエンドポイントを定義します。
  - `_index.tsx`  
    ルートパス（/）のエントリーポイントです。
  - `chat.tsx`  
    `/chat`パスのルートコンポーネントです。

- `interfaces/`  
  API通信や外部サービス連携など、アプリケーションのインターフェース層ロジックをまとめています。
  - `chat/`  
    チャット・スライド生成API呼び出し関数（`generateSlide.ts`, `confirmSlide.ts`）を格納しています。

- `root.tsx`  
  アプリケーション全体のレイアウトや共通処理を定義するエントリーポイントです。

- `tailwind.css`  
  Tailwind CSSのカスタムスタイルを定義しています。

---

### 主な変更履歴

- `interfaces/chat/`ディレクトリを新設し、チャット・スライド生成API呼び出し関数（`generateSlide.ts`, `confirmSlide.ts`）を分離しました。
- `ChatPage.tsx`は状態管理・API通信ロジックを担い、`Chat.tsx`はUI部品として責務分離しました。

## セットアップ

1. 依存パッケージのインストール:
```bash
npm install
```

2. 開発サーバーの起動:
```bash
npm run dev
```

3. ビルド:
```bash
npm run build
```

4. 本番環境での実行:
```bash
npm run start
```

## Development

Run the dev server:

```shellscript
npm run dev
```

## Deployment

First, build your app for production:

```sh
npm run build
```

Then run the app in production mode:

```sh
npm start
```

Now you'll need to pick a host to deploy it to.

### DIY

If you're familiar with deploying Node applications, the built-in Remix app server is production-ready.

Make sure to deploy the output of `npm run build`

- `build/server`
- `build/client`

## Styling

This template comes with [Tailwind CSS](https://tailwindcss.com/) already configured for a simple default starting experience. You can use whatever css framework you prefer. See the [Vite docs on css](https://vitejs.dev/guide/features.html#css) for more information.
