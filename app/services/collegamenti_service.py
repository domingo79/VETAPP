# services/collegamenti_service.py
# Gestione collegamento owner ↔ vet (richiesta, accettazione, rifiuto).
from app.services.supabase_client import get_supabase

STATI = ["pending", "accepted", "rejected"]


def get_tutti_vet() -> list:
    # Tutti i veterinari sulla piattaforma — usato per la tabella in "Il mio veterinario"
    supabase = get_supabase()
    result = (
        supabase.table("profiles")
        .select("id, nome, cognome, clinica, telefono, email")
        .eq("ruolo", "vet")
        .order("cognome")
        .execute()
    )
    return result.data or []


def invia_richiesta_collegamento(owner_id: str, vet_id: str) -> bool:
    supabase = get_supabase()
    # Evita duplicati — se esiste già qualsiasi stato, non manda una seconda richiesta
    existing = (
        supabase.table("collegamenti")
        .select("id, stato")
        .eq("owner_id", owner_id)
        .eq("vet_id", vet_id)
        .execute()
    )
    if existing.data:
        return False  # Già esiste

    result = supabase.table("collegamenti").insert({
        "owner_id": owner_id,
        "vet_id": vet_id,
        "stato": "pending",
    }).execute()
    return bool(result.data)


def get_richieste_vet(vet_id: str) -> list:
    supabase = get_supabase()
    result = (
        supabase.table("collegamenti")
        .select("*, profiles!owner_id(nome, cognome, email)")
        .eq("vet_id", vet_id)
        .eq("stato", "pending")
        .execute()
    )
    return result.data or []


def get_collegamenti_owner(owner_id: str) -> list:
    supabase = get_supabase()
    result = (
        supabase.table("collegamenti")
        .select("*, profiles!vet_id(nome, cognome, email, clinica)")
        .eq("owner_id", owner_id)
        .execute()
    )
    return result.data or []


def get_vet_collegati_owner(owner_id: str) -> list:
    # Solo i vet già accettati — serve nel selettore del form animale
    supabase = get_supabase()
    result = (
        supabase.table("collegamenti")
        .select("vet_id, profiles!vet_id(nome, cognome, clinica)")
        .eq("owner_id", owner_id)
        .eq("stato", "accepted")
        .execute()
    )
    return result.data or []


def get_collegamenti_vet(vet_id: str) -> list:
    supabase = get_supabase()
    result = (
        supabase.table("collegamenti")
        .select("*, profiles!owner_id(nome, cognome, email)")
        .eq("vet_id", vet_id)
        .eq("stato", "accepted")
        .execute()
    )
    return result.data or []


def accetta_collegamento(collegamento_id: str, vet_id: str) -> bool:
    supabase = get_supabase()
    col = (
        supabase.table("collegamenti")
        .select("id")
        .eq("id", collegamento_id)
        .eq("vet_id", vet_id)
        .single()
        .execute()
    )
    if not col.data:
        return False
    supabase.table("collegamenti").update({"stato": "accepted"}).eq("id", collegamento_id).execute()
    return True


def rifiuta_collegamento(collegamento_id: str, vet_id: str) -> bool:
    supabase = get_supabase()
    result = (
        supabase.table("collegamenti")
        .update({"stato": "rejected"})
        .eq("id", collegamento_id)
        .eq("vet_id", vet_id)
        .execute()
    )
    return bool(result.data)


