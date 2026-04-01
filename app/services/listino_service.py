"""
services/listino_service.py
Gestione listino prezzi veterinario.
"""
from app.services.supabase_client import get_supabase

CATEGORIE_LISTINO = [
    "Visite cliniche",
    "Vaccinazioni",
    "Chirurgie",
    "Esami diagnostici",
    "Trattamenti ambulatoriali",
    "Terapie",
    "Ferratura",
    "Urgenze",
    "Altro",
]

DISPONIBILITA = ["Solo in clinica", "Solo a domicilio", "Entrambi"]


def get_listino_vet(vet_id: str, solo_attive: bool = True) -> list:
    supabase = get_supabase()
    query = (
        supabase.table("listino_prezzi")
        .select("*")
        .eq("vet_id", vet_id)
        .order("categoria")
    )
    if solo_attive:
        query = query.eq("attiva", True)
    return query.execute().data or []


def aggiungi_voce(data: dict) -> dict | None:
    supabase = get_supabase()
    result = supabase.table("listino_prezzi").insert(data).execute()
    return result.data[0] if result.data else None


def aggiorna_voce(voce_id: str, data: dict) -> bool:
    supabase = get_supabase()
    result = (
        supabase.table("listino_prezzi").update(data).eq("id", voce_id).execute()
    )
    return bool(result.data)


def disattiva_voce(voce_id: str) -> bool:
    return aggiorna_voce(voce_id, {"attiva": False})


def elimina_voce(voce_id: str) -> bool:
    supabase = get_supabase()
    result = supabase.table("listino_prezzi").delete().eq("id", voce_id).execute()
    return bool(result.data)


def get_listino_owner(vet_id: str) -> list:
    """Il proprietario vede il listino del vet collegato (solo voci attive)."""
    return get_listino_vet(vet_id, solo_attive=True)
