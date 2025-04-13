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

## 設定ファイル
- `vite.config.ts` - Viteの設定
- `tsconfig.json` - TypeScriptの設定
- `tailwind.config.ts` - Tailwind CSSの設定
- `.eslintrc.cjs` - ESLintの設定
- `postcss.config.js` - PostCSSの設定

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
