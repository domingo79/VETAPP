"""
services/documenti_service.py
Upload/download documenti su Supabase Storage e record in tabella.
"""
import uuid
from app.services.supabase_client import get_supabase, get_supabase_admin

BUCKET = "documenti-animali"
TIPI_DOCUMENTO = ["Referto", "Radiografia", "Ecografia", "Ricetta", "Fattura", "Vaccinazione", "Altro"]


def upload_documento(file_bytes: bytes, filename: str, content_type: str, animale_id: str, tipo: str, note: str = "", owner_id: str = "") -> dict | None:
    """
    Carica il file su Supabase Storage (admin) e salva il record in tabella documenti (utente).
    """
    supabase = get_supabase()
    admin = get_supabase_admin()
    ext = filename.rsplit(".", 1)[-1] if "." in filename else "bin"
    storage_path = f"{animale_id}/{uuid.uuid4()}.{ext}"

    try:
        admin.storage.from_(BUCKET).upload(
            path=storage_path,
            file=file_bytes,
            file_options={"content-type": content_type},
        )
    except Exception as e:
        import streamlit as st
        st.error(f"Errore storage: {e}")
        return None

    result = supabase.table("documenti").insert({
        "animale_id": animale_id,
        "owner_id": owner_id,
        "nome_file": filename,
        "storage_path": storage_path,
        "tipo": tipo,
        "note": note,
        "content_type": content_type,
    }).execute()

    return result.data[0] if result.data else None


def get_documenti(animale_id: str) -> list:
    supabase = get_supabase()
    result = (
        supabase.table("documenti")
        .select("*")
        .eq("animale_id", animale_id)
        .order("created_at", desc=True)
        .execute()
    )
    return result.data or []


def get_url_documento(storage_path: str, expires_in: int = 3600) -> str | None:
    """Genera un URL firmato temporaneo per il download."""
    admin = get_supabase_admin()
    try:
        result = admin.storage.from_(BUCKET).create_signed_url(storage_path, expires_in)
        return result.get("signedURL")
    except Exception:
        return None


def elimina_documento(doc_id: str, storage_path: str) -> bool:
    supabase = get_supabase()
    admin = get_supabase_admin()
    try:
        admin.storage.from_(BUCKET).remove([storage_path])
        supabase.table("documenti").delete().eq("id", doc_id).execute()
        return True
    except Exception:
        return False
