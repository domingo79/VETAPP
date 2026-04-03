# auth/supabase_auth.py
# Tutto quello che riguarda login, logout, registrazione e sessione utente.

import streamlit as st
from app.services.supabase_client import get_supabase


def login(email: str, password: str) -> dict | None:
    supabase = get_supabase()
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        user = response.user
        session = response.session
        if user and session:
            st.session_state["user"] = user
            st.session_state["access_token"] = session.access_token
            st.session_state["refresh_token"] = session.refresh_token
            st.session_state["profile"] = _load_profile(user.id)
            return user
    except Exception as e:
        st.error(f"Errore login: {e}")
    return None


def register(email: str, password: str, nome: str, cognome: str, ruolo: str) -> bool:
    # Il profilo viene creato in automatico dal trigger handle_new_user su Supabase
    supabase = get_supabase()
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "nome": nome.strip().title(),
                    "cognome": cognome.strip().title(),
                    "ruolo": ruolo,
                }
            },
        })
        return bool(response.user)
    except Exception:
        return False


def richiedi_reset_password(email: str) -> bool:
    # Manda il link di reset — il template email è configurato su Supabase
    supabase = get_supabase()
    try:
        supabase.auth.reset_password_email(email)
        return True
    except Exception:
        return False


def verifica_otp(token_hash: str, tipo: str) -> bool:
    # Usata quando l'utente clicca il link da email (reset, conferma, invite)
    supabase = get_supabase()
    try:
        response = supabase.auth.verify_otp({"token_hash": token_hash, "type": tipo})
        user = response.user
        session = response.session
        if user and session:
            st.session_state["user"] = user
            st.session_state["access_token"] = session.access_token
            st.session_state["refresh_token"] = session.refresh_token
            st.session_state["profile"] = _load_profile(user.id)
            return True
    except Exception:
        pass
    return False


def aggiorna_password(nuova_password: str) -> bool:
    # Usa l'admin API perché dopo verify_otp la sessione normale non è sufficiente
    from app.services.supabase_client import get_supabase_admin
    admin = get_supabase_admin()
    user = st.session_state.get("user")
    if not user:
        return False
    try:
        admin.auth.admin.update_user_by_id(user.id, {"password": nuova_password})
        return True
    except Exception:
        return False


def completa_profilo(user_id: str, nome: str, cognome: str, ruolo: str, clinica: str | None = None) -> bool:
    # Serve per gli utenti che arrivano via link invite e non hanno ancora un profilo completo
    from app.services.supabase_client import get_supabase_admin
    admin = get_supabase_admin()
    user = st.session_state.get("user")
    email = getattr(user, "email", "") if user else ""
    payload = {
        "id": user_id,
        "email": email,
        "nome": nome.strip().title(),
        "cognome": cognome.strip().title(),
        "ruolo": ruolo,
        "clinica": clinica.strip().title() if clinica else None,
    }
    try:
        response = admin.table("profiles").upsert(payload).execute()
    except Exception as e:
        st.error(f"Errore salvataggio profilo: {e}")
        return False

    if not response.data:
        st.error("Il profilo non è stato salvato nel database. Riprova.")
        return False

    profile = st.session_state.get("profile") or {"id": user_id}
    profile.update({"nome": nome, "cognome": cognome, "ruolo": ruolo, "clinica": clinica or None})
    st.session_state["profile"] = profile
    return True


def logout():
    supabase = get_supabase()
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    for key in ["user", "access_token", "refresh_token", "profile"]:
        st.session_state.pop(key, None)


def get_current_profile() -> dict | None:
    return st.session_state.get("profile")


def is_logged_in() -> bool:
    return "user" in st.session_state and st.session_state["user"] is not None


def get_ruolo() -> str | None:
    profile = get_current_profile()
    return profile.get("ruolo") if profile else None


def _load_profile(user_id: str) -> dict | None:
    supabase = get_supabase()
    try:
        result = (
            supabase.table("profiles")
            .select("*")
            .eq("id", user_id)
            .single()
            .execute()
        )
        return result.data
    except Exception:
        return None
