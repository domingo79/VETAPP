"""
pages/owner/vaccinazioni.py
Libretto vaccinale e terapie in corso per il proprietario.
"""
import streamlit as st
from datetime import date
from app.auth.supabase_auth import get_current_profile
from app.services.animali_service import get_animali_by_owner, get_vaccini_consigliati
from app.services.vaccinazioni_service import (
    get_vaccinazioni, aggiungi_vaccinazione, elimina_vaccinazione,
    get_terapie, aggiungi_terapia, termina_terapia,
)
from app.components.ui_helpers import format_data, empty_state, divisore, icona_specie


def show():
    profile = get_current_profile()
    owner_id = profile["id"]

    st.markdown("## 💉 Vaccinazioni & Terapie")

    animali = get_animali_by_owner(owner_id)
    if not animali:
        empty_state("🐾", "Nessun animale registrato", "Aggiungi prima un animale dalla sezione apposita.")
        return

    # Selettore animale
    nomi = {a["id"]: f"{icona_specie(a['specie'])} {a['nome']}" for a in animali}
    sel_id = st.selectbox("Seleziona animale", options=list(nomi.keys()), format_func=lambda x: nomi[x])
    animale_sel = next(a for a in animali if a["id"] == sel_id)

    st.divider()
    tab_vac, tab_ter = st.tabs(["💉 Vaccinazioni", "💊 Terapie in corso"])

    # ── TAB VACCINAZIONI ──────────────────────────────────────────────────────
    with tab_vac:
        _sezione_vaccinazioni(sel_id, animale_sel)

    # ── TAB TERAPIE ───────────────────────────────────────────────────────────
    with tab_ter:
        _sezione_terapie(sel_id)


def _sezione_vaccinazioni(animale_id: str, animale: dict):
    vaccini = get_vaccinazioni(animale_id)
    specie = animale.get("specie", "")

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Aggiungi vaccino", key="btn_add_vac"):
            st.session_state["vac_form"] = True

    if st.session_state.get("vac_form"):
        _form_vaccinazione(animale_id, specie)
        st.divider()

    if not vaccini:
        empty_state("💉", "Nessun vaccino registrato")
    else:
        for v in vaccini:
            scaduto = False
            if v.get("data_prossimo_richiamo"):
                try:
                    scaduto = date.fromisoformat(v["data_prossimo_richiamo"]) < date.today()
                except Exception:
                    pass

            colore = "#FDECEA" if scaduto else "#F0F7F3"
            bordo = "#E63946" if scaduto else "#2D6A4F"

            st.markdown(
                f"""
                <div style="background:{colore}; border-left:4px solid {bordo};
                            padding:0.7rem 1rem; border-radius:0 8px 8px 0; margin-bottom:0.5rem;">
                    <b>💉 {v.get('nome_vaccino','')}</b>
                    {"<span style='color:#E63946;font-size:0.8rem;'> ⚠️ SCADUTO</span>" if scaduto else ""}
                    <br>
                    <span style="font-size:0.85rem; color:#555;">
                        Somministrato: {format_data(v.get('data_somministrazione'))} &nbsp;|&nbsp;
                        Prossimo richiamo: {format_data(v.get('data_prossimo_richiamo'))} &nbsp;|&nbsp;
                        Lotto: {v.get('lotto') or '—'}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("🗑️", key=f"del_vac_{v['id']}", help="Elimina vaccino"):
                elimina_vaccinazione(v["id"])
                st.rerun()

    # Vaccini consigliati per la specie
    consigliati = get_vaccini_consigliati(specie)
    if consigliati:
        divisore("💡 Vaccini consigliati per questa specie")
        for vc in consigliati:
            st.markdown(f"- {vc}")


def _form_vaccinazione(animale_id: str, specie: str):
    consigliati = get_vaccini_consigliati(specie)
    st.markdown("#### ➕ Nuovo vaccino")
    with st.form("form_vac"):
        nome_vac = st.text_input("Nome vaccino *", placeholder="es. Polivalente annuale")
        if consigliati:
            st.caption(f"Consigliati per {specie}: {', '.join(consigliati)}")
        col1, col2 = st.columns(2)
        with col1:
            data_somm = st.date_input("Data somministrazione *", value=date.today(), max_value=date.today())
        with col2:
            data_rich = st.date_input("Prossimo richiamo", value=None)
        lotto = st.text_input("N. Lotto (opzionale)")
        note = st.text_input("Note (opzionale)")
        col_s, col_a = st.columns(2)
        with col_s:
            sub = st.form_submit_button("💾 Salva", type="primary", use_container_width=True)
        with col_a:
            ann = st.form_submit_button("❌ Annulla", use_container_width=True)

    if ann:
        st.session_state["vac_form"] = False
        st.rerun()
    if sub:
        if not nome_vac:
            st.error("Il nome del vaccino è obbligatorio.")
            return
        payload = {
            "animale_id": animale_id,
            "nome_vaccino": nome_vac,
            "data_somministrazione": data_somm.isoformat(),
            "data_prossimo_richiamo": data_rich.isoformat() if data_rich else None,
            "lotto": lotto or None,
            "note": note or None,
        }
        ok = aggiungi_vaccinazione(payload)
        if ok:
            st.success("Vaccino aggiunto!")
            st.session_state["vac_form"] = False
            st.rerun()
        else:
            st.error("Errore nel salvataggio.")


def _sezione_terapie(animale_id: str):
    terapie_attive = get_terapie(animale_id, solo_attive=True)
    terapie_passate = get_terapie(animale_id, solo_attive=False)
    terapie_passate = [t for t in terapie_passate if not t.get("attiva")]

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Aggiungi terapia", key="btn_add_ter"):
            st.session_state["ter_form"] = True

    if st.session_state.get("ter_form"):
        _form_terapia(animale_id)
        st.divider()

    st.markdown("##### 🟢 Terapie in corso")
    if not terapie_attive:
        empty_state("💊", "Nessuna terapia in corso")
    else:
        for t in terapie_attive:
            with st.container():
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(
                        f"**💊 {t.get('farmaco','')}** — {t.get('dosaggio','')}  \n"
                        f"📅 Dal {format_data(t.get('data_inizio'))}  \n"
                        f"📝 {t.get('note') or ''}"
                    )
                with c2:
                    if st.button("✅ Termina", key=f"end_ter_{t['id']}"):
                        termina_terapia(t["id"])
                        st.rerun()

    if terapie_passate:
        with st.expander("📋 Storico terapie"):
            for t in terapie_passate:
                st.markdown(
                    f"**{t.get('farmaco','')}** — dal {format_data(t.get('data_inizio'))} "
                    f"al {format_data(t.get('data_fine'))}"
                )


def _form_terapia(animale_id: str):
    st.markdown("#### ➕ Nuova terapia")
    with st.form("form_ter"):
        farmaco = st.text_input("Farmaco / Trattamento *")
        dosaggio = st.text_input("Dosaggio", placeholder="es. 1 compressa 2 volte al giorno")
        data_inizio = st.date_input("Data inizio *", value=date.today(), max_value=date.today())
        note = st.text_area("Note", height=80)
        col_s, col_a = st.columns(2)
        with col_s:
            sub = st.form_submit_button("💾 Salva", type="primary", use_container_width=True)
        with col_a:
            ann = st.form_submit_button("❌ Annulla", use_container_width=True)

    if ann:
        st.session_state["ter_form"] = False
        st.rerun()
    if sub:
        if not farmaco:
            st.error("Il nome del farmaco è obbligatorio.")
            return
        ok = aggiungi_terapia({
            "animale_id": animale_id,
            "farmaco": farmaco,
            "dosaggio": dosaggio or None,
            "data_inizio": data_inizio.isoformat(),
            "attiva": True,
            "note": note or None,
        })
        if ok:
            st.success("Terapia aggiunta!")
            st.session_state["ter_form"] = False
            st.rerun()
        else:
            st.error("Errore nel salvataggio.")
