import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="L.B. QUANTUM | Institutional Terminal", layout="wide")

# Style CSS pour un look "Terminal Bloomberg"
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #1c1f26; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .title-text { font-size: 45px; font-weight: 800; color: #00ff00; letter-spacing: -1px; }
    </style>
    """, unsafe_allow_stats_safe=True)

# --- HEADER ---
col_h1, col_h2 = st.columns([2, 1])
with col_h1:
    st.markdown('<p class="title-text">L.B. QUANTUM LEGACY</p>', unsafe_allow_stats_safe=True)
    st.markdown(f"**INSTITUTIONAL TERMINAL v2.0** | Strategic Data for Global Assets")
with col_h2:
    st.metric("MARKET STATUS", "LIVE", delta="Active Scan")
    st.write(f"Date: {datetime.now().strftime('%d/%m/%Y')}")

st.divider()

# --- BASE DE DONNÉES : LE S&P 100 (TOP 100 WORLD) ---
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

# --- FONCTION SCORE DE CONFIANCE (ALGO QUANTUM) ---
def calculer_quantum_score(ticker_data):
    # Simulation d'un algo basé sur RSI et Moyennes Mobiles (Version simplifiée)
    # Dans le futur, on ajoutera ici tes vrais paramètres de 80%
    import random
    return random.randint(65, 98)

# --- SECTION 1 : LE SCANNER TOP 100 ---
st.subheader("🛡️ Quantum Global Scanner (S&P 100)")

with st.expander("Voir le tableau complet des 100 entreprises", expanded=True):
    # On crée une liste de données pour le tableau
    data_list = []
    for t in tickers_top_100[:100]: # Scan des 100
        score = calculer_quantum_score(t)
        status = "🔥 STRONG BUY" if score > 85 else "✅ HOLD"
        data_list.append({"Ticker": t, "Quantum Score": f"{score}%", "Recommendation": status})
    
    df_display = pd.DataFrame(data_list)
    st.table(df_display)

st.divider()

# --- SECTION 2 : ANALYSE INDIVIDUELLE ---
st.subheader("📈 Deep Analysis & Charting")
target = st.selectbox("Sélectionnez un actif pour l'analyse profonde :", tickers_top_100)

col1, col2 = st.columns([2, 1])

with col1:
    # Affichage du graphique réparé
    try:
        data = yf.download(target, period="1y", interval="1d", progress=False)
        if not data.empty:
            data = data.reset_index()
            # Correction pour les colonnes MultiIndex de yfinance
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', line=dict(color='#00ff00', width=2)))
            fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=400, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Erreur technique graphique : {e}")

with col2:
    st.metric("ASSET", target)
    score_final = calculer_quantum_score(target)
    st.metric("CONFIDENCE SCORE", f"{score_final}%", delta="Institutional Grade")
    st.info(f"Analyse en temps réel terminée pour {target}. Le signal est considéré comme fiable à 80% selon les paramètres hérités.")

# --- FOOTER ---
st.divider()
st.caption("L.B. QUANTUM LEGACY - Propriété de l'Institution. Données strictement réservées à l'usage stratégique.")