"""
services/listino_service.py
Gestione listino prezzi veterinario.
"""
from app.services.supabase_client import get_supabase

VOCI_DEFAULT = [
    {"nome_prestazione": "Visita clinica generale",            "categoria": "Visite cliniche",          "prezzo": 35.00, "durata_minuti": 30, "disponibilita": "Entrambi"},
    {"nome_prestazione": "Visita di controllo",                "categoria": "Visite cliniche",          "prezzo": 25.00, "durata_minuti": 20, "disponibilita": "Entrambi"},
    {"nome_prestazione": "Visita domiciliare",                 "categoria": "Visite cliniche",          "prezzo": 50.00, "durata_minuti": 45, "disponibilita": "Solo a domicilio"},
    {"nome_prestazione": "Vaccinazione annuale",               "categoria": "Vaccinazioni",             "prezzo": 40.00, "durata_minuti": 15, "disponibilita": "Solo in clinica"},
    {"nome_prestazione": "Vaccinazione antirabbica",           "categoria": "Vaccinazioni",             "prezzo": 30.00, "durata_minuti": 15, "disponibilita": "Solo in clinica"},
    {"nome_prestazione": "Prelievo sangue + esame emocromo",   "categoria": "Esami diagnostici",        "prezzo": 45.00, "durata_minuti": 20, "disponibilita": "Solo in clinica"},
    {"nome_prestazione": "Ecografia addominale",               "categoria": "Esami diagnostici",        "prezzo": 70.00, "durata_minuti": 30, "disponibilita": "Solo in clinica"},
    {"nome_prestazione": "Pulizia dentale (detartrasi)",       "categoria": "Trattamenti ambulatoriali","prezzo": 80.00, "durata_minuti": 45, "disponibilita": "Solo in clinica"},
    {"nome_prestazione": "Trattamento antiparassitario",       "categoria": "Terapie",                  "prezzo": 20.00, "durata_minuti": 10, "disponibilita": "Entrambi"},
    {"nome_prestazione": "Visita d'urgenza",                   "categoria": "Urgenze",                  "prezzo": 60.00, "durata_minuti": 30, "disponibilita": "Entrambi"},
]

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


def ha_listino(vet_id: str) -> bool:
    """Controlla se il vet ha già voci nel listino (attive o meno)."""
    supabase = get_supabase()
    result = (
        supabase.table("listino_prezzi")
        .select("id")
        .eq("vet_id", vet_id)
        .limit(1)
        .execute()
    )
    return bool(result.data)


def inizializza_listino_default(vet_id: str) -> bool:
    """Inserisce le voci predefinite del listino per un nuovo veterinario."""
    supabase = get_supabase()
    voci = [{**v, "vet_id": vet_id, "attiva": True} for v in VOCI_DEFAULT]
    result = supabase.table("listino_prezzi").insert(voci).execute()
    return bool(result.data)
