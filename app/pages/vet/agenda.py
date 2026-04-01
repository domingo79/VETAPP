"""
pages/vet/agenda.py
Agenda appuntamenti del veterinario con gestione stati.
"""
import streamlit as st
from datetime import date, timedelta
from app.auth.supabase_auth import get_current_profile
from app.services.appuntamenti_service import (
    get_appuntamenti_vet, aggiorna_stato, STATI, STATI_LABEL
)
from app.components.ui_helpers import format_datetime, render_badge, empty_state, icona_specie


def show():
    profile = get_current_profile()
    vet_id = profile["id"]

    st.markdown("## 📅 Agenda")

    col1, col2, col3 = st.columns(3)
    with col1:
        data_da = st.date_input("Dal", value=date.today())
    with col2:
        data_a = st.date_input("Al", value=date.today() + timedelta(days=30))
    with col3:
        filtro_stato = st.selectbox("Stato", ["Tutti"] + list(STATI_LABEL.values()))

    appuntamenti = get_appuntamenti_vet(
        vet_id,
        data_da=data_da.isoformat() + "T00:00:00",
        data_a=data_a.isoformat() + "T23:59:59",
    )

    # Filtro stato
    if filtro_stato != "Tutti":
        stato_key = next((k for k, v in STATI_LABEL.items() if v == filtro_stato), None)
        if stato_key:
            appuntamenti = [a for a in appuntamenti if a.get("stato") == stato_key]

    st.markdown(f"**{len(appuntamenti)} appuntamenti trovati**")
    st.divider()

    if not appuntamenti:
        empty_state("📅", "Nessun appuntamento nel periodo selezionato")
        return

    for app in appuntamenti:
        animale = app.get("animali") or {}
        owner = app.get("profiles") or {}
        stato = app.get("stato", "in_attesa")

        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            st.markdown(
                f"**{format_datetime(app.get('data_ora'))}**  \n"
                f"{icona_specie(animale.get('specie',''))} **{animale.get('nome','?')}**  \n"
                f"👤 {owner.get('nome','')} {owner.get('cognome','')} — {owner.get('email','')}  \n"
                f"📝 {app.get('motivo','')}"
            )
        with col2:
            render_badge(stato)
            if app.get("note"):
                st.caption(f"Note: {app['note']}")
        with col3:
            # Cambio stato rapido
            if stato == "in_attesa":
                if st.button("✅ Conferma", key=f"conf_{app['id']}"):
                    aggiorna_stato(app["id"], "confermato")
                    st.rerun()
                if st.button("❌ Annulla", key=f"ann_{app['id']}"):
                    aggiorna_stato(app["id"], "annullato")
                    st.rerun()
            elif stato == "confermato":
                if st.button("🏁 Completato", key=f"comp_{app['id']}", type="primary"):
                    aggiorna_stato(app["id"], "completato")
                    st.rerun()
                if st.button("❌ Annulla", key=f"ann2_{app['id']}"):
                    aggiorna_stato(app["id"], "annullato")
                    st.rerun()
        st.divider()
