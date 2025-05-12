-- Create Table
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

-- Delete Table

