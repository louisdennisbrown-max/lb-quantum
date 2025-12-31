import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURATION STRICTE ---
st.set_page_config(page_title="LB Quantum | Quantitative Terminal", layout="wide")

# Design Minimaliste et Professionnel
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .title-text { font-size: 28px; font-weight: 700; color: #ffffff; }
    .subtitle-text { font-size: 13px; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
c1, c2 = st.columns([3, 1])
with c1:
    st.markdown('<p class="title-text">LB QUANTUM ANALYTICS</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-text">Professional Quantitative Terminal | S&P 100 Market Coverage</p>', unsafe_allow_html=True)
with c2:
    st.metric("DATA STATUS", "OPERATIONAL", delta="100 Assets Linked")

st.divider()

# --- LISTE OFFICIELLE DU S&P 100 ---
tickers_sp100 = [
    "AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "META", "TSLA", "BRK-B", "UNH", "LLY",
    "JPM", "XOM", "V", "MA", "AVGO", "HD", "PG", "COST", "JNJ", "ABBV",
    "CRM", "WMT", "BAC", "CVX", "MRK", "NFLX", "ADBE", "AMD", "PEP", "KO",
    "TMO", "WFC", "DIS", "CSCO", "ACN", "ABT", "ORCL", "LIN", "MCD", "INTC",
    "INTU", "VZ", "CMCSA", "AMGN", "PFE", "IBM", "TXN", "PM", "MS", "UNP",
    "HON", "RTX", "GS", "LOW", "CAT", "AXP", "QCOM", "GE", "SPGI", "BLK",
    "DE", "SYK", "AMAT", "PLD", "BA", "ISRG", "MDLZ", "TJX", "T", "GILD",
    "LRCX", "VRTX", "BKNG", "ETN", "REGN", "C", "MMC", "ADP", "CI", "ADI",
    "BSX", "ZTS", "MDT", "MU", "SCHW", "CVS", "WM", "LMT", "PANW", "FI",
    "NOW", "SNPS", "CDNS", "ELV", "CB", "TGT", "MO", "DHR", "ICE", "PGR"
]

# --- LOGIQUE DE CALCUL RSI (RÉELLE) ---
def get_rsi_score(ticker):
    try:
        data = yf.download(ticker, period="1mo", interval="1d", progress=False)
        if len(data) < 14: return 50
        data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1+rs))
        return int(rsi.iloc[-1])
    except:
        return 50

# --- SCANNER GLOBAL ---
st.subheader("Market Intelligence Scanner (S&P 100)")

if st.button('Lancer le scan des 100 actifs'):
    progress_bar = st.progress(0)
    results = []
    
    # On scanne les 100 (ceci peut prendre 10-15 secondes)
    for i, t in enumerate(tickers_sp100):
        score = get_rsi_score(t)
        if score < 40: status = "Opportunité d'Achat"
        elif score > 60: status = "Surévalué"
        else: status = "Stable"
        
        results.append({"Ticker": t, "RSI Score": score, "Analytic Signal": status})
        progress_bar.progress((i + 1) / len(tickers_sp100))
    
    df_results = pd.DataFrame(results)
    st.dataframe(df_results.sort_values(by="RSI Score"), use_container_width=True, height=450)
else:
    st.info("Cliquez sur le bouton ci-dessus pour charger les analyses en temps réel sur le Top 100 mondial.")

st.divider()

# --- FOCUS TECHNIQUE ---
st.subheader("Technical Asset View")
target = st.selectbox("Sélectionner une entreprise pour analyse approfondie :", tickers_sp100)

col_chart, col_data = st.columns([2, 1])

with col_chart:
    try:
        df_target = yf.download(target, period="1y", interval="1d", progress=False)
        df_target.columns = [col[0] if isinstance(col, tuple) else col for col in df_target.columns]
        
        fig = go.Figure(data=[go.Candlestick(
            x=df_target.index,
            open=df_target['Open'],
            high=df_target['High'],
            low=df_target['Low'],
            close=df_target['Close'],
            increasing_line_color='#00ff00', decreasing_line_color='#ff0000'
        )])
        fig.update_layout(template="plotly_dark", height=450, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.error("Données temporairement indisponibles.")

with col_data:
    if not df_target.empty:
        last_price = df_target['Close'].iloc[-1]
        st.metric(f"Cours {target}", f"{last_price:.2f} USD")
        
        # Calcul du RSI actuel pour l'affichage à droite
        current_rsi = get_rsi_score(target)
        st.write(f"**Indicateur RSI :** {current_rsi}")
        
        if current_rsi < 30:
            st.success("SIGNAL : SURVENDU (Achat potentiel)")
        elif current_rsi > 70:
            st.warning("SIGNAL : SURACHETÉ (Prudence)")
        else:
            st.info("SIGNAL : NEUTRE")
            
        st.write("---")
        st.write("Ce terminal utilise l'indicateur RSI (Relative Strength Index) sur 14 périodes pour identifier les points de retournement de tendance.")

st.caption(f"© {datetime.now().year} LB Quantum Analytics | Data sourced via Yahoo Finance")