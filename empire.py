import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# Configuration Institutionnelle
st.set_page_config(page_title="L.B. Quantum - Institutional", layout="wide")

# Look & Feel Terminal Bloomberg
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    div[data-testid="stMetric"] { background-color: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ L.B. QUANTUM - INSTITUTIONAL TERMINAL")

# --- PARAMÈTRES ET TOP 20 ---
top_20 = {
    "NVIDIA": "NVDA", "APPLE": "AAPL", "MICROSOFT": "MSFT", "AMAZON": "AMZN",
    "GOOGLE": "GOOGL", "META": "META", "BERKSHIRE": "BRK-B", "ELI LILLY": "LLY",
    "TSMC": "TSM", "BROADCOM": "AVGO", "TESLA": "TSLA", "JPMORGAN": "JPM",
    "VISA": "V", "UNITEDHEALTH": "UNH", "WALMART": "WMT", "EXXON": "XOM",
    "MASTERCARD": "MA", "ASML": "ASML", "ORACLE": "ORCL", "BLACKROCK": "BLK"
}

# --- BARRE LATÉRALE : STRATÉGIE ---
st.sidebar.header("🕹️ PARAMÈTRES DE LA HOLDING")
mode = st.sidebar.radio("Mode d'Analyse", ["Scanner Global", "Analyse Focus"])
capital_total = st.sidebar.number_input("Capital de la Holding ($)", value=100000)
risque_pc = st.sidebar.slider("Exposition Max par ligne (%)", 1, 5, 2)

# --- FONCTION D'ANALYSE PRO (Vise 80% de succès) ---
def analyse_expert(ticker):
    try:
        # On récupère 6 mois pour calculer les moyennes mobiles
        data = yf.download(ticker, period="6mo", progress=False)
        if data.empty: return None
        
        # 1. Calcul RSI
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rsi = 100 - (100 / (1 + (gain/loss)))
        current_rsi = float(rsi.iloc[-1].item())
        
        # 2. Moyenne Mobile 50 jours (Tendance de fond)
        ma50 = data['Close'].rolling(window=50).mean()
        current_ma50 = float(ma50.iloc[-1].item())
        prix_actuel = float(data['Close'].iloc[-1].item())
        
        # 3. Calcul du Score de Confiance
        score = 0
        if current_rsi < 35: score += 40
        if current_rsi < 25: score += 20
        if prix_actuel < current_ma50: score += 40
        
        # Verdict
        if score >= 80: verdict = "💎 ACHAT ÉLITE"
        elif score >= 40: verdict = "⚖️ ACCUMULATION"
        elif current_rsi > 70: verdict = "⚠️ SURCHAUFFE / VENTE"
        else: verdict = "⏳ ATTENTE"
        
        return {
            "Ticker": ticker,
            "Prix": round(prix_actuel, 2),
            "RSI": round(current_rsi, 2),
            "MA50": round(current_ma50, 2),
            "Score": score,
            "Verdict": verdict
        }
    except:
        return None

# --- AFFICHAGE ---
if mode == "Scanner Global":
    st.subheader("📑 Surveillance des 20 Puissances Mondiales")
    with st.spinner("Calcul des probabilités en cours..."):
        results = []
        for name, tick in top_20.items():
            res = analyse_expert(tick)
            if res:
                res["Entreprise"] = name
                results.append(res)
        
        df = pd.DataFrame(results)
        
        # Affichage du tableau avec style
        def color_verdict(val):
            if "ACHAT" in val: color = "#00ff00"
            elif "SURCHAUFFE" in val: color = "#ff4b4b"
            else: color = "white"
            return f'color: {color}'

        st.table(df[['Entreprise', 'Ticker', 'Prix', 'RSI', 'Score', 'Verdict']].style.applymap(color_verdict, subset=['Verdict']))

    # IA Advisor
    st.divider()
    st.subheader("📑 NOTE DE SYNTHÈSE EXECUTIVE")
    achats = df[df['Score'] >= 80]['Entreprise'].tolist()
    alertes = df[df['Verdict'] == "⚠️ SURCHAUFFE / VENTE"]['Entreprise'].tolist()
    
    if achats:
        st.success(f"**Opportunités de déploiement (Probabilité Elevée) :** {', '.join(achats)}")
    if alertes:
        st.error(f"**Zones de danger (Surchauffe) :** {', '.join(alertes)}")
    if not achats and not alertes:
        st.info("Le marché est en zone de stabilité. Aucune intervention requise.")

else:
    # Mode Focus
    nom_sel = st.sidebar.selectbox("Choisir une cible", list(top_20.keys()))
    res = analyse_expert(top_20[nom_sel])
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(f"Graphique de Puissance : {nom_sel}")
        hist = yf.download(top_20[nom_sel], period="1y", progress=False)
        fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist['Close'], line=dict(color='#00ff00'))])
        fig.update_layout(template="plotly_dark", height=450)
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("Diagnostic")
        st.metric("SCORE DE CONFIANCE", f"{res['Score']}/100")
        st.metric("RSI", f"{res['RSI']}")
        st.write(f"**Verdict :** {res['Verdict']}")
        st.divider()
        allocation = capital_total * (risque_pc / 100)
        st.write(f"**Allocation max conseillée :**")
        st.write(f"### {allocation:,.0f} $")

st.caption("L.B. QUANTUM v2.0 - Institutional Grade")