import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="LB Quantum Analytics", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .title-text { font-size: 28px; font-weight: 700; color: #ffffff; }
    .subtitle-text { font-size: 13px; color: #8b949e; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<p class="title-text">LB QUANTUM ANALYTICS</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Quantitative Analysis Terminal | S&P 100 Intelligence</p>', unsafe_allow_html=True)
st.divider()

# --- LISTE DES 100 ---
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

# --- FONCTION DE CALCUL ---
@st.cache_data(ttl=3600)
def fetch_market_data():
    results = []
    # Téléchargement groupé
    raw_data = yf.download(tickers_sp100, period="1mo", interval="1d", progress=False)
    close_data = raw_data['Close']
    
    for t in tickers_sp100:
        try:
            series = close_data[t].dropna()
            if len(series) < 14: continue
            
            # Calcul RSI
            delta = series.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1+rs))
            current_rsi = int(rsi.iloc[-1])
            
            # Signaux mathématiques (RSI standard)
            if current_rsi < 35: status = "🟢 OPPORTUNITÉ"
            elif current_rsi > 65: status = "🔴 SURÉVALUÉ"
            else: status = "⚪ NEUTRE"
            
            results.append({"Ticker": t, "RSI (14d)": current_rsi, "Analyse Technique": status})
        except:
            continue
    return pd.DataFrame(results)

# --- SCANNER ---
st.subheader("Market Momentum Scanner")

if st.button('🔄 Lancer un nouveau scan du Top 100'):
    st.cache_data.clear()
    with st.spinner('Analyse des flux financiers en cours...'):
        df_market = fetch_market_data()
    st.success('Scan terminé.')
else:
    df_market = fetch_market_data()

st.dataframe(df_market.sort_values(by="RSI (14d)"), use_container_width=True, height=400)

st.divider()

# --- ANALYSE DÉTAILLÉE ---
st.subheader("Deep Asset Analysis")
target = st.selectbox("Sélectionner un actif pour le graphique en bougies :", tickers_sp100)

col_chart, col_stats = st.columns([2, 1])

with col_chart:
    df_target = yf.download(target, period="1y", interval="1d", progress=False)
    if isinstance(df_target.columns, pd.MultiIndex):
        df_target.columns = df_target.columns.get_level_values(0)
        
    fig = go.Figure(data=[go.Candlestick(
        x=df_target.index, open=df_target['Open'], high=df_target['High'],
        low=df_target['Low'], close=df_target['Close'],
        increasing_line_color='#00ff00', decreasing_line_color='#ff3131'
    )])
    fig.update_layout(template="plotly_dark", height=450, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

with col_stats:
    current_val = df_target['Close'].iloc[-1]
    st.metric(f"Dernier prix ({target})", f"{current_val:.2f} USD")
    st.markdown("---")
    st.write("**Note d'analyse :**")
    st.write("Le graphique ci-contre affiche l'évolution historique sur 12 mois. Utilisez les bougies pour identifier les pressions acheteuses (vert) ou vendeuses (rouge).")

st.caption(f"© {datetime.now().year} LB Quantum Analytics | Données certifiées S&P 100")