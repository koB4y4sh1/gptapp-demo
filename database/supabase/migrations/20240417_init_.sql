create table slides (
  id uuid primary key default gen_random_uuid(),       -- 物理主キー
  user_id uuid not null,                               -- Supabase Auth連携
  session_id uuid not null,                            -- セッション識別子
  title text,
  slide_json jsonb,
  pptx_path text,                                       -- NULL可（まだ生成されていないとき）
  confirmed boolean default false,                     -- 提案確認済みか
  created_at timestamp with time zone default timezone('utc'::text, now()),

  unique (user_id, session_id)
);
