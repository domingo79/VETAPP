# services/cartella_clinica_service.py
# Cartelle cliniche: creazione, lettura, eliminazione. Solo il vet scrive.
from app.services.supabase_client import get_supabase


def get_cartelle_by_animale(animale_id: str) -> list:
    supabase = get_supabase()
    result = (
        supabase.table("cartelle_cliniche")
        .select("*, profiles!vet_id(nome, cognome)")
        .eq("animale_id", animale_id)
        .order("data_visita", desc=True)
        .execute()
    )
    return result.data or []


def crea_cartella(data: dict) -> dict | None:
    supabase = get_supabase()
    result = supabase.table("cartelle_cliniche").insert(data).execute()
    return result.data[0] if result.data else None


def elimina_cartella(cartella_id: str) -> bool:
    supabase = get_supabase()
    result = (
        supabase.table("cartelle_cliniche").delete().eq("id", cartella_id).execute()
    )
    return bool(result.data)


def get_ultime_visite_vet(vet_id: str, limite: int = 10) -> list:
    supabase = get_supabase()
    result = (
        supabase.table("cartelle_cliniche")
        .select("*, animali!animale_id(nome, specie, profiles!owner_id(nome, cognome))")
        .eq("vet_id", vet_id)
        .order("data_visita", desc=True)
        .limit(limite)
        .execute()
    )
    return result.data or []
