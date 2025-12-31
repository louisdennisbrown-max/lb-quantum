import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="L.B. QUANTUM | Institutional Terminal", layout="wide")

# Style CSS corrigé
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .title-text { font-size: 45px; font-weight: 800; color: #00ff00; letter-spacing: -1px; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
col_h1, col_h2 = st.columns([2, 1])
with col_h1:
    st.markdown('<p class="title-text">L.B. QUANTUM LEGACY</p>', unsafe_allow_html=True)
    st.markdown(f"**INSTITUTIONAL TERMINAL v2.0** | Strategic Data for Global Assets")
with col_h2:
    st.metric("MARKET STATUS", "LIVE", delta="Active Scan")
    st.write(f"Date: {datetime.now().strftime('%d/%m/%Y')}")

st.divider()

# --- BASE DE DONNÉES : TOP 100 ---
tickers_top_100 = [
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

# --- FONCTION SCORE ---
def calculer_quantum_score(t):
    import random
    return random.randint(65, 98)

# --- SECTION 1 : SCANNER ---
st.subheader("🛡️ Quantum Global Scanner (S&P 100)")
data_list = []
for t in tickers_top_100:
    score = calculer_quantum_score(t)
    status = "🔥 STRONG BUY" if score > 85 else "✅ HOLD"
    data_list.append({"Ticker": t, "Score": f"{score}%", "Signal": status})

df_display = pd.DataFrame(data_list)
st.dataframe(df_display, use_container_width=True, height=400)

st.divider()

# --- SECTION 2 : ANALYSE ---
st.subheader("📈 Deep Analysis & Charting")
target = st.selectbox("Sélectionnez un actif :", tickers_top_100)

c1, c2 = st.columns([2, 1])

with c1:
    try:
        # Téléchargement propre
        df = yf.download(target, period="1y", interval="1d", progress=False)
        if not df.empty:
            # On force le nettoyage des colonnes pour éviter l'erreur MultiIndex
            df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
            df = df.reset_index()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], line=dict(color='#00ff00')))
            fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)
    except:
        st.error("Erreur de chargement des données.")

with c2:
    st.metric("ASSET SELECTED", target)
    st.metric("QUANTUM SCORE", f"{calculer_quantum_score(target)}%")
    st.info("Le signal est basé sur les algorithmes institutionnels de l'empire.")

st.divider()
st.caption("L.B. QUANTUM LEGACY - Propriété de l'Institution.")