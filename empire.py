import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="LB Quantum | Quantitative Terminal", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .title-text { font-size: 28px; font-weight: 700; color: #ffffff; }
    .subtitle-text { font-size: 13px; color: #8b949e; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<p class="title-text">LB QUANTUM ANALYTICS</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Professional Quantitative Terminal | S&P 100 Market Coverage</p>', unsafe_allow_html=True)
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

# --- FONCTION DE CALCUL AVEC CACHE (Pour éviter les changements brusques) ---
@st.cache_data(ttl=3600)  # Garde les données en mémoire pendant 1 heure
def fetch_market_data():
    results = []
    # On télécharge les données d'un coup pour les 100 tickers pour plus de stabilité
    data = yf.download(tickers_sp100, period="1mo", interval="1d", progress=False)['Close']
    
    for t in tickers_sp100:
        try:
            series = data[t].dropna()
            if len(series) < 14: continue
            
            delta = series.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1+rs))
            current_rsi = int(rsi.iloc[-1])
            
            if current_rsi < 40: status = "LANCER ACHAT"
            elif current_rsi > 60: status = "ZONE DE VENTE"
            else: status = "NEUTRE / HOLD"
            
            results.append({"Ticker": t, "RSI": current_rsi, "Signal": status})
        except:
            continue
    return pd.DataFrame(results)

# --- AFFICHAGE DU SCANNER ---
st.subheader("Market Intelligence Scanner")

# Chargement automatique ou rafraîchissement manuel
if st.button('Actualiser les données du marché'):
    st.cache_data.clear()
    df_market = fetch_market_data()
else:
    df_market = fetch_market_data()

st.dataframe(df_market.sort_values(by="RSI"), use_container_width=True, height=400)

st.divider()

# --- FOCUS TECHNIQUE ---
target = st.selectbox("Analyse technique détaillée :", tickers_sp100)

col_chart, col_stats = st.columns([2, 1])

with col_chart:
    df_target = yf.download(target, period="1y", interval="1d", progress=False)
    # Correction du format yfinance
    if isinstance(df_target.columns, pd.MultiIndex):
        df_target.columns = df_target.columns.get_level_values(0)
        
    fig = go.Figure(data=[go.Candlestick(
        x=df_target.index, open=df_target['Open'], high=df_target['High'],
        low=df_target['Low'], close=df_target['Close']
    )])
    fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

with col_stats:
    last_p = df_target['Close'].iloc[-1]
    st.metric(f"Cours {target}", f"{last_p:.2f} USD")
    st.info("Les analyses sont figées pendant 1 heure pour garantir la stabilité des signaux institutionnels.")

st.caption(f"© {datetime.now().year} LB Quantum Analytics")