import streamlit as st
from pathlib import Path

# --- Ścieżka do katalogu z artykułami ---
ARTICLES_DIR = Path("articles")

if not ARTICLES_DIR.exists():
    st.warning("Katalog 'articles' nie istnieje. Dodaj pliki .md do repozytorium.")
    ARTICLES_DIR.mkdir(exist_ok=True)

# --- Pobranie listy artykułów ---
articles = sorted(ARTICLES_DIR.glob("*.md"))

# --- Parametry URL ---
def get_query_param(param_name):
    value = st.query_params.get(param_name)
    if isinstance(value, list):
        return value[0] if value else None
    return value  # jeśli jest string, zwróć cały


selected = get_query_param("article")

if selected:
    # --- Wyświetl wybrany artykuł ---
    article_path = ARTICLES_DIR / selected
    if article_path.exists():
        text = article_path.read_text(encoding="utf-8")

        st.markdown(text, unsafe_allow_html=True)
        st.divider()

        if st.button("⬅️ Powrót do listy artykułów"):
            st.query_params.clear()
            st.rerun()
    else:
        st.error("Nie znaleziono artykułu.")
else:
    # --- Lista artykułów ---
    st.title("📰 Artykuły")
    if not articles:
        st.info("Brak artykułów w katalogu 'articles'.")
    for path in articles:
        title = path.read_text(encoding="utf-8").splitlines()[0].strip("# ").strip()
        if st.button(title, use_container_width=True):
            st.query_params["article"] = path.name
            st.rerun()
