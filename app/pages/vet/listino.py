"""
pages/vet/listino.py
Gestione listino prezzi del veterinario.
"""
import streamlit as st
from app.auth.supabase_auth import get_current_profile
from app.services.listino_service import (
    get_listino_vet, aggiungi_voce, aggiorna_voce,
    disattiva_voce, elimina_voce,
    CATEGORIE_LISTINO, DISPONIBILITA,
    inizializza_listino_default,
)
from app.components.ui_helpers import empty_state, divisore


def show():
    profile = get_current_profile()
    vet_id = profile["id"]

    st.markdown("## 💶 Listino prezzi")
    st.caption("Crea e gestisci il listino delle tue prestazioni. I proprietari collegati lo potranno visualizzare.")

    col1, col2 = st.columns([3, 1])
    with col2:
        mostra_disattive = st.checkbox("Mostra disattivate", value=False)
        if st.button("➕ Nuova voce", type="primary", use_container_width=True):
            st.session_state["listino_form"] = True
        if st.button("📋 Carica voci predefinite", use_container_width=True,
                     help="Inserisce 10 prestazioni di esempio che puoi modificare"):
            inizializza_listino_default(vet_id)
            st.success("✅ Voci predefinite caricate!")
            st.rerun()

    if st.session_state.get("listino_form"):
        _form_voce(vet_id)
        st.divider()

    voci = get_listino_vet(vet_id, solo_attive=not mostra_disattive)

    if not voci:
        empty_state("💶", "Nessuna voce nel listino", "Aggiungi le tue prestazioni con il pulsante sopra.")
        return

    # Raggruppa per categoria
    categorie = {}
    for v in voci:
        cat = v.get("categoria", "Altro")
        categorie.setdefault(cat, []).append(v)

    for cat, items in sorted(categorie.items()):
        st.markdown(f"#### 📂 {cat}")
        for v in items:
            # Se questa voce è in modalità modifica, mostra il form
            if st.session_state.get("listino_edit_id") == v["id"]:
                _form_modifica_voce(v)
                continue

            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
            with col1:
                attiva_label = "" if v.get("attiva") else " *(disattivata)*"
                st.markdown(
                    f"**{v.get('nome_prestazione','')}**{attiva_label}  \n"
                    f"<span style='font-size:0.83rem;color:#666;'>"
                    f"{v.get('disponibilita','')} · "
                    f"{v.get('durata_minuti') or '—'} min"
                    f"</span>",
                    unsafe_allow_html=True,
                )
                if v.get("note"):
                    st.caption(v["note"])
            with col2:
                st.markdown(f"**€ {v.get('prezzo', 0):.2f}**")
            with col3:
                if st.button("✏️", key=f"edit_{v['id']}", help="Modifica"):
                    st.session_state["listino_edit_id"] = v["id"]
                    st.rerun()
            with col4:
                if v.get("attiva"):
                    if st.button("🔇", key=f"dis_{v['id']}", help="Disattiva"):
                        disattiva_voce(v["id"])
                        st.rerun()
                else:
                    if st.button("🔔", key=f"att_{v['id']}", help="Riattiva"):
                        aggiorna_voce(v["id"], {"attiva": True})
                        st.rerun()
            with col5:
                if st.button("🗑️", key=f"del_list_{v['id']}", help="Elimina"):
                    elimina_voce(v["id"])
                    st.rerun()
        st.divider()


def _form_voce(vet_id: str):
    st.markdown("#### ➕ Nuova voce listino")
    with st.form("form_listino"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome prestazione *", placeholder="es. Visita di controllo")
            categoria = st.selectbox("Categoria *", CATEGORIE_LISTINO)
        with col2:
            prezzo = st.number_input("Prezzo (€) *", min_value=0.0, step=0.5)
            durata = st.number_input("Durata (minuti, opzionale)", min_value=0, step=5)

        disponibilita = st.selectbox("Disponibilità", DISPONIBILITA)
        note = st.text_input("Note (opzionale)")

        col_s, col_a = st.columns(2)
        with col_s:
            sub = st.form_submit_button("💾 Salva", type="primary", use_container_width=True)
        with col_a:
            ann = st.form_submit_button("❌ Annulla", use_container_width=True)

    if ann:
        st.session_state["listino_form"] = False
        st.rerun()
    if sub:
        if not nome:
            st.error("Il nome della prestazione è obbligatorio.")
            return
        ok = aggiungi_voce({
            "vet_id": vet_id,
            "nome_prestazione": nome,
            "categoria": categoria,
            "prezzo": prezzo,
            "durata_minuti": durata or None,
            "disponibilita": disponibilita,
            "note": note or None,
            "attiva": True,
        })
        if ok:
            st.success("✅ Voce aggiunta al listino!")
            st.session_state["listino_form"] = False
            st.rerun()
        else:
            st.error("Errore nel salvataggio.")


def _form_modifica_voce(v: dict):
    """Form inline per modificare una voce esistente del listino."""
    st.markdown(f"#### ✏️ Modifica: *{v.get('nome_prestazione','')}*")
    with st.form(f"form_edit_{v['id']}"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome prestazione *", value=v.get("nome_prestazione", ""))
            categoria = st.selectbox(
                "Categoria *", CATEGORIE_LISTINO,
                index=CATEGORIE_LISTINO.index(v["categoria"]) if v.get("categoria") in CATEGORIE_LISTINO else 0,
            )
        with col2:
            prezzo = st.number_input("Prezzo (€) *", min_value=0.0, step=0.5, value=float(v.get("prezzo", 0)))
            durata = st.number_input("Durata (minuti, opzionale)", min_value=0, step=5, value=int(v.get("durata_minuti") or 0))

        disponibilita = st.selectbox(
            "Disponibilità", DISPONIBILITA,
            index=DISPONIBILITA.index(v["disponibilita"]) if v.get("disponibilita") in DISPONIBILITA else 0,
        )
        note = st.text_input("Note (opzionale)", value=v.get("note") or "")

        col_s, col_a = st.columns(2)
        with col_s:
            sub = st.form_submit_button("💾 Salva modifiche", type="primary", use_container_width=True)
        with col_a:
            ann = st.form_submit_button("❌ Annulla", use_container_width=True)

    if ann:
        st.session_state.pop("listino_edit_id", None)
        st.rerun()
    if sub:
        if not nome:
            st.error("Il nome della prestazione è obbligatorio.")
            return
        ok = aggiorna_voce(v["id"], {
            "nome_prestazione": nome,
            "categoria": categoria,
            "prezzo": prezzo,
            "durata_minuti": durata or None,
            "disponibilita": disponibilita,
            "note": note or None,
        })
        if ok:
            st.success("✅ Voce aggiornata!")
            st.session_state.pop("listino_edit_id", None)
            st.rerun()
        else:
            st.error("Errore nel salvataggio.")
