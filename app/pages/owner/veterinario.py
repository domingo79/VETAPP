"""
pages/owner/veterinario.py
Gestione collegamento con il veterinario.
"""
import streamlit as st
from app.auth.supabase_auth import get_current_profile
from app.services.collegamenti_service import (
    cerca_vet_per_nome, invia_richiesta_collegamento,
    get_collegamenti_owner, invita_vet_via_email,
)
from app.components.ui_helpers import render_badge, empty_state, divisore


def show():
    profile = get_current_profile()
    owner_id = profile["id"]

    st.markdown("## 🩺 Il mio veterinario")

    # ── Collegamenti esistenti ────────────────────────────────────────────────
    collegamenti = get_collegamenti_owner(owner_id)
    if collegamenti:
        st.markdown("### 🔗 I tuoi collegamenti")
        for col in collegamenti:
            vet_profile = col.get("profiles") or {}
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(
                    f"**🩺 {vet_profile.get('nome','')} {vet_profile.get('cognome','')}**  \n"
                    f"{vet_profile.get('clinica') or ''} · {vet_profile.get('email','')}",
                )
            with col2:
                render_badge(col.get("stato", "pending"))
        divisore()

    # ── Cerca veterinario ─────────────────────────────────────────────────────
    st.markdown("### 🔍 Cerca e collega un veterinario")

    ricerca = st.text_input("Cerca per cognome del veterinario", placeholder="es. Rossi")

    if ricerca:
        risultati = cerca_vet_per_nome(ricerca)
        if not risultati:
            st.info("Nessun veterinario trovato con quel cognome.")
            st.markdown("**Il tuo veterinario non è ancora registrato?**")
            with st.form("form_invito"):
                email_invito = st.text_input("Email del veterinario", placeholder="vet@clinica.it")
                sub_invito = st.form_submit_button("📧 Invia invito", type="primary")
            if sub_invito:
                if not email_invito:
                    st.error("Inserisci l'email.")
                else:
                    ok, err = invita_vet_via_email(email_invito)
                    if ok:
                        st.success(f"✅ Invito inviato a {email_invito}!")
                    else:
                        st.error(f"Errore nell'invio dell'invito: {err}")
        else:
            for vet in risultati:
                vet_id = vet["id"]
                # Controlla se già collegato
                gia_collegato = any(c["vet_id"] == vet_id for c in collegamenti)
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(
                        f"**🩺 {vet.get('nome','')} {vet.get('cognome','')}**  \n"
                        f"{vet.get('clinica') or ''} · {vet.get('email','')}"
                    )
                with col2:
                    if gia_collegato:
                        st.markdown("✅ Già collegato")
                    else:
                        if st.button("🔗 Richiedi collegamento", key=f"col_{vet_id}"):
                            ok = invia_richiesta_collegamento(owner_id, vet_id)
                            if ok:
                                st.success("Richiesta inviata! Attendi che il veterinario la accetti.")
                                st.rerun()
                            else:
                                st.warning("Richiesta già inviata o errore.")
