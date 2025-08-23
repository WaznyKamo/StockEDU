import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from Scripts.data_visualisation import plot_multiple_y_axes

st.title("🔍 Wyszukiwarka spółek")
st.write("Sprawdź historyczne wyniki oraz wskaźniki finansowe wybranej spółki.")

all_data = st.session_state.all_data
# yearly_data = st.session_state.yearly_data


selected_company_name = st.selectbox(
    "Wybierz spółkę:",
    options=all_data["Nazwa+ticker"].unique()
)

name_to_ticker = dict(zip(all_data["Nazwa+ticker"], all_data["Ticker"]))

selected_company_ticker = name_to_ticker[selected_company_name]

# Filtrujemy dane dla wybranej spółki
company_data = all_data[all_data["Ticker"] == selected_company_ticker].sort_values(by="Data publikacji", ascending=False)

financial_data = company_data.drop(columns=["Nazwa", "Nazwa+ticker", "Ticker"])

# Dodanie zakładek
tab1, tab2 = st.tabs(["📊 Dane finansowe", "📉 Wizualizacja wskaźników"])

with tab1:
    st.subheader("Wskaźniki finansowe")

    # Konfiguracja AgGrid
    gb = GridOptionsBuilder.from_dataframe(financial_data)
    gb.configure_default_column(
        filter=True,          # umożliwia filtrowanie
        sortable=True,        # sortowanie kolumn
        resizable=True,       # zmiana szerokości
        editable=False
    )
    # gb.configure_selection("multiple", use_checkbox=True)  # opcjonalny wybór wielu wierszy
    gb.configure_side_bar()  # panel boczny z wyborem kolumn i filtrami
    grid_options = gb.build()

    AgGrid(
        financial_data,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.MANUAL,
        enable_enterprise_modules=True,
        # fit_columns_on_grid_load=True
    )

with tab2:
    col1, col2 = st.columns([1, 3])  # lewa kolumna na wybór, prawa na wykres

    with col1:
        st.subheader("Wybierz dane")

        # Zapisuj tylko kolumny liczbowe z all_data
        kolumny_danych = [col for col in financial_data.select_dtypes(include='number').columns if col not in ['Data publikacji', 'Ticker', 'Kwartały', 'Nazwa', "Nazwa+ticker"]]

        if 'kolumny_wykres' not in st.session_state:
            st.session_state.kolumny_wykres = [kolumny_danych[0]]


        if st.button("➕ Dodaj informację na wykresie"):
            niewybrane = [k for k in kolumny_danych if k not in st.session_state.kolumny_wykres]
            if niewybrane:
                st.session_state.kolumny_wykres.append(niewybrane[0])

        nowe_kolumny = []
        for i, kol in enumerate(st.session_state.kolumny_wykres):
            selected = st.selectbox(f"Kolumna {i+1}", kolumny_danych, index=kolumny_danych.index(kol), key=f"kol_{i}")
            nowe_kolumny.append(selected)


        st.session_state.kolumny_wykres = nowe_kolumny



        if st.button("🔄 Zresetuj wykres"):
            st.session_state.kolumny_wykres = []
            if 'spolka' in st.session_state:
                del st.session_state['spolka']
            st.rerun()

    with col2:
        st.info("Poniższy wykres jest interaktywny. Zaznaczenie pola pozwala przybliżyć dane. Podwójne kliknięcie przywraca widok początkowy.")
        # st.subheader(f"Wykres: {wybrana_spolka}")
        plot_multiple_y_axes(financial_data, st.session_state.kolumny_wykres, title_prefix="Wskaźniki")