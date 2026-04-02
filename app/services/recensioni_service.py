"""
services/recensioni_service.py
Gestione recensioni dei veterinari da parte dei proprietari.
"""
from app.services.supabase_client import get_supabase


def get_recensioni_vet(vet_id: str) -> list:
    """Restituisce tutte le recensioni di un veterinario con il nome del proprietario."""
    supabase = get_supabase()
    result = (
        supabase.table("recensioni")
        .select("*, profiles!owner_id(nome, cognome)")
        .eq("vet_id", vet_id)
        .order("created_at", desc=True)
        .execute()
    )
    return result.data or []


def get_media_voto(vet_id: str) -> float | None:
    """Restituisce la media dei voti di un veterinario, o None se non ha recensioni."""
    recensioni = get_recensioni_vet(vet_id)
    if not recensioni:
        return None
    return round(sum(r["voto"] for r in recensioni) / len(recensioni), 1)


def aggiungi_recensione(owner_id: str, vet_id: str, voto: int, testo: str | None) -> bool:
    supabase = get_supabase()
    try:
        supabase.table("recensioni").insert({
            "owner_id": owner_id,
            "vet_id": vet_id,
            "voto": voto,
            "testo": testo or None,
        }).execute()
        return True
    except Exception:
        return False


def ha_gia_recensito(owner_id: str, vet_id: str) -> bool:
    supabase = get_supabase()
    result = (
        supabase.table("recensioni")
        .select("id")
        .eq("owner_id", owner_id)
        .eq("vet_id", vet_id)
        .execute()
    )
    return bool(result.data)


def elimina_recensione(owner_id: str, vet_id: str) -> bool:
    supabase = get_supabase()
    result = (
        supabase.table("recensioni")
        .delete()
        .eq("owner_id", owner_id)
        .eq("vet_id", vet_id)
        .execute()
    )
    return bool(result.data)
