"""
pages/vet/pazienti.py
Lista pazienti (animali) del veterinario con filtri e accesso cartella.
"""
import streamlit as st
from app.auth.supabase_auth import get_current_profile
from app.services.animali_service import get_animali_by_vet
from app.services.vaccinazioni_service import get_vaccinazioni, get_terapie
from app.services.cartella_clinica_service import get_cartelle_by_animale
from app.components.ui_helpers import (
    format_data, format_datetime, empty_state, icona_specie, divisore
)


def show():
    profile = get_current_profile()
    vet_id = profile["id"]

    st.markdown("## 🐾 I miei pazienti")

    animali = get_animali_by_vet(vet_id)
    if not animali:
        empty_state("🐾", "Nessun paziente ancora", "I pazienti appariranno quando un proprietario si collega.")
        return

    # Filtri
    col1, col2, col3 = st.columns(3)
    with col1:
        filtro_specie = st.selectbox("Filtra per specie", ["Tutte", "Cane", "Gatto", "Cavallo"])
    with col2:
        cerca = st.text_input("Cerca per nome animale o proprietario", placeholder="🔍")
    with col3:
        st.markdown(f"**{len(animali)} pazienti totali**")

    # Applica filtri
    filtrati = animali
    if filtro_specie != "Tutte":
        filtrati = [a for a in filtrati if a.get("specie") == filtro_specie]
    if cerca:
        q = cerca.lower()
        filtrati = [
            a for a in filtrati
            if q in (a.get("nome") or "").lower()
            or q in (a.get("profiles", {}) or {}).get("cognome", "").lower()
            or q in (a.get("profiles", {}) or {}).get("nome", "").lower()
        ]

    if not filtrati:
        empty_state("🔍", "Nessun risultato trovato")
        return

    for animale in filtrati:
        specie = animale.get("specie", "")
        owner = animale.get("profiles") or {}
        with st.expander(
            f"{icona_specie(specie)} **{animale['nome']}** — "
            f"{animale.get('razza','?')} · "
            f"👤 {owner.get('nome','')} {owner.get('cognome','')}"
        ):
            tab_info, tab_cartella, tab_vaccini, tab_terapie = st.tabs(
                ["ℹ️ Info", "📋 Cartella clinica", "💉 Vaccinazioni", "💊 Terapie"]
            )

            with tab_info:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Specie:** {specie}")
                    st.markdown(f"**Razza:** {animale.get('razza','—')}")
                    st.markdown(f"**Data nascita:** {format_data(animale.get('data_nascita'))}")
                    st.markdown(f"**Sesso:** {animale.get('sesso','—')}")
                with col2:
                    st.markdown(f"**Microchip:** {animale.get('microchip') or '—'}")
                    st.markdown(f"**Peso:** {animale.get('peso_kg') or '—'} kg")
                    st.markdown(f"**Allergie:** {animale.get('allergie') or '—'}")
                    st.markdown(f"**Proprietario:** {owner.get('nome','')} {owner.get('cognome','')} — {owner.get('email','')}")

            with tab_cartella:
                from app.pages.vet.cartella_clinica import render_cartella_animale
                render_cartella_animale(animale["id"], vet_id)

            with tab_vaccini:
                vaccini = get_vaccinazioni(animale["id"])
                if not vaccini:
                    empty_state("💉", "Nessun vaccino registrato")
                else:
                    for v in vaccini:
                        st.markdown(
                            f"**{v.get('nome_vaccino','')}** — "
                            f"somministrato: {format_data(v.get('data_somministrazione'))} — "
                            f"prossimo richiamo: {format_data(v.get('data_prossimo_richiamo'))}"
                        )

            with tab_terapie:
                terapie = get_terapie(animale["id"], solo_attive=True)
                if not terapie:
                    empty_state("💊", "Nessuna terapia in corso")
                else:
                    for t in terapie:
                        st.markdown(
                            f"**{t.get('farmaco','')}** — {t.get('dosaggio','—')} — "
                            f"dal {format_data(t.get('data_inizio'))}"
                        )
