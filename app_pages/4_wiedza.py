import streamlit as st
from pathlib import Path

ARTICLES_DIR = Path("articles")
ARTICLES_DIR.mkdir(exist_ok=True)

articles = sorted(ARTICLES_DIR.glob("*.md"))
selected = st.query_params.get("article")

if selected:
    # --- Wyświetl artykuł ---
    article_path = ARTICLES_DIR / selected
    if article_path.exists():
        text = article_path.read_text(encoding="utf-8")
        title = text.splitlines()[0].strip("# ").strip()

        st.title(title)
        st.markdown(text, unsafe_allow_html=True)
        st.divider()

        if st.button("⬅️ Powrót do listy artykułów"):
            st.query_params.clear()
            st.rerun()  # 💥 natychmiastowe przeładowanie
    else:
        st.error("Nie znaleziono artykułu.")
else:
    # --- Lista artykułów ---
    st.title("📰 Artykuły")
    st.write("Wybierz artykuł, aby go przeczytać:")

    for path in articles:
        title = path.read_text(encoding="utf-8").splitlines()[0].strip("# ").strip()
        if st.button(title, use_container_width=True):
            st.query_params["article"] = path.name
            st.rerun()  # 💥 natychmiastowe przejście
