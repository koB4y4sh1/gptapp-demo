from src.interfaces.client.supabase_client import supabase

def get_session_state(user_id: str,session_id: str) -> dict | None:
    response = (
        supabase
        .from_("slides")
        .select("*")
        .eq("user_id", user_id)
        .eq("session_id", session_id)
        .single()
        .execute()
    )
    
    if response.data:
        return response.data
    return None

def save_slide(user_id: str, session_id: str, title: str, slide_json: dict, confirmed: bool = False):
    response = supabase.table("slides").insert({
        "user_id": user_id,
        "session_id": session_id,
        "title": title,
        "slide_json": slide_json,
        "confirmed": confirmed,
    }).execute()
    return response

def update_slide(user_id: str, session_id: str, pptx_path:str, confirmed: bool):
    response = supabase.table("slides").update({
    "pptx_path": pptx_path,
    "confirmed": confirmed
    }).eq("user_id", user_id).eq("session_id", session_id).execute()
    return response
