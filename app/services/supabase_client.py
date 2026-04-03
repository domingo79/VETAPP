# services/supabase_client.py
# Due client Supabase: uno per l'utente (RLS attiva), uno admin (service_role, bypassa RLS).
import streamlit as st
from supabase import create_client, Client


def get_supabase() -> Client:
    # Usa i token in session_state per autenticare la richiesta come utente corrente.
    # Se i token sono scaduti, procede come client anonimo senza crashare.
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    client = create_client(url, key)
    access_token = st.session_state.get("access_token")
    refresh_token = st.session_state.get("refresh_token")
    if access_token and refresh_token:
        try:
            client.auth.set_session(access_token, refresh_token)
        except Exception:
            pass
    elif access_token:
        client.postgrest.auth(access_token)
    return client


def get_supabase_admin() -> Client:
    # Service role key — bypassa RLS. Usato solo per operazioni che richiedono privilegi elevati
    # (es. aggiornare la password dopo verify_otp, upsert profili da invite).
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["service_role_key"]
    return create_client(url, key)
