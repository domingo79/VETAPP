"""
services/supabase_client.py
Connessione centralizzata a Supabase.
"""
import streamlit as st
from supabase import create_client, Client


@st.cache_resource
def get_supabase() -> Client:
    """Restituisce un'istanza singleton del client Supabase."""
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)


@st.cache_resource
def get_supabase_admin() -> Client:
    """Client con service_role_key per operazioni admin (es. inviti email)."""
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["service_role_key"]
    return create_client(url, key)
