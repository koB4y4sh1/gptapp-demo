# supabase.py
import os
import logging

from supabase import create_client, Client

# SupabaseのURLとAPIキー
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# Supabaseクライアントの初期化
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def save_to_supabase(image:dict[str|list[str]]) -> None:
    """
    Supabaseのデータベースにイラストを保存します。

    引数:
        image (dict[str|list[str]]): 
            - name (str): イラストの名前
            - title (str): イラストのタイトル。
            - caption (str): イラストの説明文。
            - url (list): 画像ファイルのURL。
            - embedding (list): 埋め込みベクトル。

    戻り値:
        None: 保存が成功した場合は何も返さない。
    """
    try:

        response = supabase.table("illustrations").insert(image).execute()
        if response.data:
            logging.debug(f'✅ {image["title"]} をSupabaseに保存しました。')
        else:
            logging.error(f'❌ Supabaseへの保存に失敗しました: {response.error}')
    except Exception as e:
        logging.error(f"🚨 Supabase保存エラー: {e}")
