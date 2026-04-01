"""
services/messaggi_service.py
Chat diretta owner ↔ vet.
"""
from app.services.supabase_client import get_supabase


def get_conversazione(owner_id: str, vet_id: str) -> list:
    supabase = get_supabase()
    result = (
        supabase.table("messaggi")
        .select("*")
        .eq("owner_id", owner_id)
        .eq("vet_id", vet_id)
        .order("created_at")
        .execute()
    )
    return result.data or []


def invia_messaggio(owner_id: str, vet_id: str, mittente_id: str, testo: str) -> dict | None:
    supabase = get_supabase()
    result = supabase.table("messaggi").insert({
        "owner_id": owner_id,
        "vet_id": vet_id,
        "mittente_id": mittente_id,
        "testo": testo,
        "letto": False,
    }).execute()
    return result.data[0] if result.data else None


def segna_come_letti(owner_id: str, vet_id: str, destinatario_id: str) -> None:
    supabase = get_supabase()
    supabase.table("messaggi").update({"letto": True}).eq("owner_id", owner_id).eq("vet_id", vet_id).neq("mittente_id", destinatario_id).execute()


def get_messaggi_non_letti(utente_id: str) -> int:
    supabase = get_supabase()
    result = (
        supabase.table("messaggi")
        .select("id", count="exact")
        .neq("mittente_id", utente_id)
        .eq("letto", False)
        .execute()
    )
    return result.count or 0
