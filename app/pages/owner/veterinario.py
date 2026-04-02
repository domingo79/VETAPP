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
from app.services.listino_service import get_listino_owner
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
            stato = col.get("stato", "pending")
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(
                    f"**🩺 {vet_profile.get('nome','')} {vet_profile.get('cognome','')}**  \n"
                    f"{vet_profile.get('clinica') or ''} · {vet_profile.get('email','')}",
                )
            with col2:
                render_badge(stato)
            if stato == "accepted":
                with st.expander("💶 Vedi listino prezzi"):
                    voci = get_listino_owner(col["vet_id"])
                    if not voci:
                        st.caption("Il veterinario non ha ancora pubblicato un listino.")
                    else:
                        categorie: dict = {}
                        for v in voci:
                            categorie.setdefault(v.get("categoria", "Altro"), []).append(v)
                        for cat, items in sorted(categorie.items()):
                            st.markdown(f"**{cat}**")
                            for v in items:
                                r1, r2 = st.columns([3, 1])
                                with r1:
                                    durata = f" · {v['durata_minuti']} min" if v.get("durata_minuti") else ""
                                    disp = v.get("disponibilita", "")
                                    st.markdown(
                                        f"{v.get('nome_prestazione','')}  \n"
                                        f"<span style='font-size:0.8rem;color:#888;'>{disp}{durata}</span>",
                                        unsafe_allow_html=True,
                                    )
                                    if v.get("note"):
                                        st.caption(v["note"])
                                with r2:
                                    st.markdown(f"**€ {v.get('prezzo', 0):.2f}**")
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
