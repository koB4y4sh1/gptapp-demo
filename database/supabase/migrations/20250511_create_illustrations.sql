create extension if not exists vector;

create table illustrations (
  id bigint primary key generated always as identity,
  name text not null,
  title text not null,
  caption text not null,
  url text[] not null,
  embedding vector(1536),
  created_at timestamp with time zone default now()
);

create index on illustrations using hnsw (embedding vector_cosine_ops);

create or replace function find_similar_illustration(query_embedding vector)
returns table (
    id bigint,
    name text,
    title text,
    caption text,
    url text[]
)
as $$
  select id, name, title, caption, url
  from illustrations
  order by embedding <-> query_embedding
  limit 1;
$$ language sql
stable;
