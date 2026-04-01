"""
pages/owner/documenti.py
Upload e gestione documenti (referti, ricette, fatture…).
"""
import streamlit as st
from app.auth.supabase_auth import get_current_profile
from app.services.animali_service import get_animali_by_owner
from app.services.documenti_service import (
    get_documenti, upload_documento, elimina_documento,
    get_url_documento, TIPI_DOCUMENTO,
)
from app.components.ui_helpers import format_datetime, empty_state, icona_specie


ICONE_TIPO = {
    "Referto": "📄",
    "Radiografia": "🔬",
    "Ecografia": "🔬",
    "Ricetta": "💊",
    "Fattura": "🧾",
    "Vaccinazione": "💉",
    "Altro": "📎",
}


def show():
    profile = get_current_profile()
    owner_id = profile["id"]

    st.markdown("## 📁 Documenti")

    animali = get_animali_by_owner(owner_id)
    if not animali:
        empty_state("🐾", "Nessun animale registrato")
        return

    nomi = {a["id"]: f"{icona_specie(a['specie'])} {a['nome']}" for a in animali}
    sel_id = st.selectbox("Seleziona animale", options=list(nomi.keys()), format_func=lambda x: nomi[x])

    st.divider()

    # ── Upload ────────────────────────────────────────────────────────────────
    with st.expander("📤 Carica nuovo documento", expanded=False):
        with st.form("form_upload"):
            file = st.file_uploader(
                "Seleziona file (PDF o immagine)",
                type=["pdf", "jpg", "jpeg", "png", "webp"],
                help="Max 25 MB"
            )
            col1, col2 = st.columns(2)
            with col1:
                tipo = st.selectbox("Tipo documento", TIPI_DOCUMENTO)
            with col2:
                note = st.text_input("Note (opzionale)")
            sub = st.form_submit_button("📤 Carica", type="primary", use_container_width=True)

        if sub:
            if not file:
                st.error("Seleziona un file.")
            else:
                with st.spinner("Caricamento in corso…"):
                    risultato = upload_documento(
                        file_bytes=file.read(),
                        filename=file.name,
                        content_type=file.type,
                        animale_id=sel_id,
                        tipo=tipo,
                        note=note,
                        owner_id=owner_id,
                    )
                if risultato:
                    st.success(f"✅ Documento '{file.name}' caricato!")
                    st.rerun()
                else:
                    st.error("Errore nel caricamento.")

    # ── Lista documenti ───────────────────────────────────────────────────────
    documenti = get_documenti(sel_id)

    if not documenti:
        empty_state("📁", "Nessun documento", "Carica referti, ricette o altri file dal pannello sopra.")
        return

    # Filtro per tipo
    tipi_presenti = list(set(d.get("tipo", "Altro") for d in documenti))
    filtro = st.multiselect("Filtra per tipo", tipi_presenti, default=tipi_presenti)

    for doc in documenti:
        if doc.get("tipo") not in filtro:
            continue
        icona = ICONE_TIPO.get(doc.get("tipo", "Altro"), "📎")

        col1, col2, col3 = st.columns([4, 2, 1])
        with col1:
            st.markdown(
                f"{icona} **{doc.get('nome_file','')}**  \n"
                f"<span style='font-size:0.83rem;color:#666;'>"
                f"Tipo: {doc.get('tipo','')} &nbsp;·&nbsp; {format_datetime(doc.get('created_at'))}"
                f"</span>",
                unsafe_allow_html=True,
            )
            if doc.get("note"):
                st.caption(doc["note"])
        with col2:
            url = get_url_documento(doc.get("storage_path", ""))
            if url:
                st.link_button("⬇️ Scarica", url)
        with col3:
            if st.button("🗑️", key=f"del_doc_{doc['id']}", help="Elimina documento"):
                elimina_documento(doc["id"], doc.get("storage_path", ""))
                st.rerun()
        st.divider()
