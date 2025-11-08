import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, ColumnsAutoSizeMode
from Scripts.data_visualisation import plot_multiple_y_axes
import plotly.express as px


all_data = st.session_state.all_data
daily_data = st.session_state.daily_data
technical_data = st.session_state.technical_data

# Sekcja nagłówka i wyboru spółki
col1, col2 = st.columns([1, 2]) 
with col1:
    st.title("🔍 Wyszukiwarka spółek")
    st.write("Sprawdź historyczne wyniki oraz wskaźniki finansowe wybranej spółki.")
    selected_company_name = st.selectbox(
    "Wybierz spółkę:",
    options=all_data["Nazwa+ticker"].unique()
    )
    name_to_ticker = dict(zip(all_data["Nazwa+ticker"], all_data["Ticker"]))

selected_company_ticker = name_to_ticker[selected_company_name]
with col2:

    # Sprawdź czy w daily_data jest kolumna z tickerem
    if selected_company_ticker not in daily_data.columns:
        st.warning(f"Brak kolumny z cenami dla tickera: {selected_company_ticker}")
    else:
        df_prices = daily_data[["DATE", selected_company_ticker]].copy()
        # Konwersja daty i porządkowanie
        df_prices["DATE"] = pd.to_datetime(df_prices["DATE"], errors="coerce")
        df_prices = df_prices.dropna(subset=["DATE"]).sort_values("DATE")

        if df_prices.empty:
            st.warning("Brak danych dziennych dla wybranej spółki.")
        else:
            # Wykres liniowy cen
            fig = px.line(df_prices, x="DATE", y=selected_company_ticker,
                            labels={"DATE": "Data", selected_company_ticker: "Cena"},
                            title=f"Cena akcji — {selected_company_name} ({selected_company_ticker})")
            fig.update_layout(xaxis_title="DATE", yaxis_title="Cena", template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

# Filtrujemy dane dla wybranej spółki
company_data = all_data[all_data["Ticker"] == selected_company_ticker].sort_values(by="Data publikacji", ascending=False)

financial_data = company_data.drop(columns=["Nazwa", "Nazwa+ticker", "Ticker"])

stock_technical_data = technical_data[technical_data["Ticker"] == selected_company_ticker]

# Sekcja zakładek
tab1, tab2, tab3 = st.tabs(["📊 Dane finansowe", "📈 Wizualizacja wskaźników", "📡 Sygnały techniczne"], width="stretch")

with tab1:
    st.subheader("Wskaźniki finansowe")
    
    st.info("""💡 Jak korzystać z tabeli:\n
    Kliknij nagłówek kolumny, aby sortować dane (klikaj ponownie, by zmienić kierunek).\n
    Użyj ikony lejka przy nazwie kolumny, aby filtrować wartości.\n
    Możesz stosować filtry w wielu kolumnach jednocześnie.""")
    
    # Konfiguracja AgGrid z poprawkami do wyświetlania w streamlit.app
    gb = GridOptionsBuilder.from_dataframe(financial_data)
    gb.configure_default_column(
        editable=False,
        groupable=True,
        filter=True,
        sortable=True,
        resizable=True,
        minWidth=120,
        wrapHeaderText=True,
        autoHeaderHeight=True
    )
    gb.configure_side_bar()

    grid_options = gb.build()

    AgGrid(
        financial_data,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.NO_UPDATE,
        enable_enterprise_modules=True,
        theme="streamlit",
        height=600,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
        fit_columns_on_grid_load=True
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
with tab3:
    # Pobranie sygnału bez błędów gdy brak danych
    if not stock_technical_data.empty and "Overall_signal" in stock_technical_data.columns:
        signal = str(stock_technical_data["Overall_signal"].iloc[0])
    else:
        signal = "Brak"

    sig_lower = signal.lower()
    if "sprzedaj" in sig_lower:
        color = "red"
    elif "kupuj" in sig_lower:
        color = "green"
    else:
        color = "black"

    # Wyświetlenie jako subheader z kolorem (tag h3 by dopasować rozmiar)
    st.markdown(f"<h3>Sygnał ogólny: <span style='color:{color}; font-weight:700'>{signal}</span></h3>", unsafe_allow_html=True)

    st.write("RSI (Relative Strength Index): " + str(stock_technical_data["RSI"].iloc[0])  + " " + stock_technical_data["RSI_signal"].iloc[0])

    st.write("MACD (różnica): " + str(stock_technical_data["MACD_diff"].iloc[0])  + " " + stock_technical_data["MACD_signal"].iloc[0])

    st.write("Sygnał Wstęgi Bollingera: " + stock_technical_data["BB_signal"].iloc[0])

    st.write("CCI (Commodity Channel Index): " + str(stock_technical_data["CCI"].iloc[0])  + " " + stock_technical_data["CCI_signal"].iloc[0])

    st.write("Oscylator stochastyczny: " + str(stock_technical_data["Stochastic"].iloc[0])  + " " + stock_technical_data["Stochastic_signal"].iloc[0])
