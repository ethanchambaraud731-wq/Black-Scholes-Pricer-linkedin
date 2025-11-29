import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go
from numpy import log, sqrt, exp
import matplotlib.pyplot as plt
import seaborn as sns

#######################
# Configuration de la page
st.set_page_config(
    page_title="Modèle de Pricing d'Options Black-Scholes",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")


# CSS personnalisé pour Streamlit
st.markdown("""
<style>
/* Ajuster la taille et l'alignement des conteneurs de valeurs CALL et PUT */
.metric-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 8px;
    width: auto;
    margin: 0 auto;
}

/* Classes personnalisées pour les valeurs CALL et PUT */
.metric-call {
    background-color: #90ee90;
    color: black;
    margin-right: 10px;
    border-radius: 10px;
}

.metric-put {
    background-color: #ffcccb;
    color: black;
    border-radius: 10px;
}

/* Style pour le texte de valeur */
.metric-value {
    font-size: 1.5rem;
    font-weight: bold;
    margin: 0;
}

/* Style pour le texte du label */
.metric-label {
    font-size: 1rem;
    margin-bottom: 4px;
}

</style>
""", unsafe_allow_html=True)


class BlackScholes:
    def __init__(
        self,
        time_to_maturity: float,
        strike: float,
        current_price: float,
        volatility: float,
        interest_rate: float,
    ):
        self.time_to_maturity = time_to_maturity
        self.strike = strike
        self.current_price = current_price
        self.volatility = volatility
        self.interest_rate = interest_rate

    def calculate_prices(self):
        time_to_maturity = self.time_to_maturity
        strike = self.strike
        current_price = self.current_price
        volatility = self.volatility
        interest_rate = self.interest_rate

        d1 = (
            log(current_price / strike) +
            (interest_rate + 0.5 * volatility ** 2) * time_to_maturity
            ) / (
                volatility * sqrt(time_to_maturity)
            )
        d2 = d1 - volatility * sqrt(time_to_maturity)

        call_price = current_price * norm.cdf(d1) - (
            strike * exp(-(interest_rate * time_to_maturity)) * norm.cdf(d2)
        )
        put_price = (
            strike * exp(-(interest_rate * time_to_maturity)) * norm.cdf(-d2)
        ) - current_price * norm.cdf(-d1)

        self.call_price = call_price
        self.put_price = put_price

        # GREEKS
        # Delta
        self.call_delta = norm.cdf(d1)
        self.put_delta = 1 - norm.cdf(d1)

        # Gamma
        self.call_gamma = norm.pdf(d1) / (
            strike * volatility * sqrt(time_to_maturity)
        )
        self.put_gamma = self.call_gamma

        return call_price, put_price


def plot_heatmap(bs_model, spot_range, vol_range, strike):
    call_prices = np.zeros((len(vol_range), len(spot_range)))
    put_prices = np.zeros((len(vol_range), len(spot_range)))
    
    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            bs_temp = BlackScholes(
                time_to_maturity=bs_model.time_to_maturity,
                strike=strike,
                current_price=spot,
                volatility=vol,
                interest_rate=bs_model.interest_rate
            )
            bs_temp.calculate_prices()
            call_prices[i, j] = bs_temp.call_price
            put_prices[i, j] = bs_temp.put_price
    
    # Heatmap des prix Call
    fig_call, ax_call = plt.subplots(figsize=(10, 8))
    sns.heatmap(call_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), 
                annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_call)
    ax_call.set_title('Prix du CALL')
    ax_call.set_xlabel('Prix Spot')
    ax_call.set_ylabel('Volatilité')
    
    # Heatmap des prix Put
    fig_put, ax_put = plt.subplots(figsize=(10, 8))
    sns.heatmap(put_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), 
                annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_put)
    ax_put.set_title('Prix du PUT')
    ax_put.set_xlabel('Prix Spot')
    ax_put.set_ylabel('Volatilité')
    
    return fig_call, fig_put


def plot_pnl_heatmap(bs_model, spot_range, vol_range, strike, call_purchase_price, put_purchase_price):
    call_pnl = np.zeros((len(vol_range), len(spot_range)))
    put_pnl = np.zeros((len(vol_range), len(spot_range)))
    
    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            bs_temp = BlackScholes(
                time_to_maturity=bs_model.time_to_maturity,
                strike=strike,
                current_price=spot,
                volatility=vol,
                interest_rate=bs_model.interest_rate
            )
            bs_temp.calculate_prices()
            call_pnl[i, j] = bs_temp.call_price - call_purchase_price
            put_pnl[i, j] = bs_temp.put_price - put_purchase_price
    
    # Heatmap PnL Call
    fig_call_pnl, ax_call_pnl = plt.subplots(figsize=(10, 8))
    sns.heatmap(call_pnl, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), 
                annot=True, fmt=".2f", cmap="RdYlGn", center=0, ax=ax_call_pnl)
    ax_call_pnl.set_title(f'PnL CALL (Prix d\'achat : {call_purchase_price:.2f}€)')
    ax_call_pnl.set_xlabel('Prix Spot')
    ax_call_pnl.set_ylabel('Volatilité')
    
    # Heatmap PnL Put
    fig_put_pnl, ax_put_pnl = plt.subplots(figsize=(10, 8))
    sns.heatmap(put_pnl, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), 
                annot=True, fmt=".2f", cmap="RdYlGn", center=0, ax=ax_put_pnl)
    ax_put_pnl.set_title(f'PnL PUT (Prix d\'achat : {put_purchase_price:.2f}€)')
    ax_put_pnl.set_xlabel('Prix Spot')
    ax_put_pnl.set_ylabel('Volatilité')
    
    return fig_call_pnl, fig_put_pnl


# Sidebar pour les entrées utilisateur
with st.sidebar:
    st.title("📊 Modèle Black-Scholes")
    st.markdown("---")
    st.markdown("**`Créé par :`**")
    linkedin_url = "https://www.linkedin.com/in/ethan-chambaraud"
    st.markdown(
        f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;">'
        f'<img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" '
        f'style="vertical-align: middle; margin-right: 10px;">'
        f'`Ethan Chambaraud`</a>',
        unsafe_allow_html=True
    )
    st.markdown("---")
    
    st.subheader("Paramètres de Marché")
    current_price = st.number_input("Prix Actuel de l'Actif", value=100.0)
    strike = st.number_input("Prix d'Exercice (Strike)", value=100.0)
    time_to_maturity = st.number_input("Temps jusqu'à Maturité (Années)", value=1.0)
    volatility = st.number_input("Volatilité (σ)", value=0.2)
    interest_rate = st.number_input("Taux d'Intérêt Sans Risque", value=0.05)

    st.markdown("---")
    st.subheader("Prix d'Achat pour PnL")
    call_purchase_price = st.number_input("Prix d'Achat du Call", value=10.0, step=0.5, 
                                         help="Prix d'achat du call pour calculer le PnL")
    put_purchase_price = st.number_input("Prix d'Achat du Put", value=10.0, step=0.5,
                                        help="Prix d'achat du put pour calculer le PnL")
    
    st.markdown("---")
    st.subheader("Paramètres des Heatmaps")
    spot_min = st.number_input('Prix Spot Minimum', min_value=0.01, value=current_price*0.8, step=0.01)
    spot_max = st.number_input('Prix Spot Maximum', min_value=0.01, value=current_price*1.2, step=0.01)
    vol_min = st.slider('Volatilité Minimum pour Heatmap', min_value=0.01, max_value=1.0, value=volatility*0.5, step=0.01)
    vol_max = st.slider('Volatilité Maximum pour Heatmap', min_value=0.01, max_value=1.0, value=volatility*1.5, step=0.01)
    
    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)
    
    st.markdown("---")
    calculate_button = st.button("🔄 Calculer", type="primary", use_container_width=True)


# Page principale pour l'affichage des résultats
st.title("Modèle de Pricing Black-Scholes")

# Affichage des explications avant le calcul
if not calculate_button:
    st.markdown("---")
    st.header("📚 Comprendre le Modèle Black-Scholes")
    
    st.markdown("""
    ### Qu'est-ce que le modèle Black-Scholes ?
    
    Le **modèle Black-Scholes** est une formule mathématique utilisée pour déterminer le prix théorique 
    d'une option européenne. Développé en 1973 par Fischer Black, Myron Scholes et Robert Merton, 
    ce modèle révolutionnaire prend en compte plusieurs facteurs clés :
    
    - **Prix actuel de l'actif sous-jacent** (S)
    - **Prix d'exercice** (K) : le prix auquel l'option peut être exercée
    - **Temps jusqu'à l'échéance** (T) : durée restante avant expiration
    - **Volatilité** (σ) : mesure de la variation du prix de l'actif
    - **Taux d'intérêt sans risque** (r) : rendement d'un investissement sans risque
    
    Le modèle calcule le prix d'un **Call** (option d'achat) et d'un **Put** (option de vente) en supposant 
    que les prix des actifs suivent une distribution log-normale et que les marchés sont efficients.
    """)
    
    st.markdown("---")
    st.header("🗺️ Comprendre les Heatmaps")
    
    st.markdown("""
    ### Qu'est-ce qu'une heatmap ?
    
    Une **heatmap** (carte thermique) est une représentation graphique qui utilise des couleurs pour 
    visualiser des données complexes sur deux dimensions. Dans notre cas :
    
    - **Axe horizontal (X)** : Prix Spot de l'actif
    - **Axe vertical (Y)** : Volatilité
    - **Couleurs** : Représentent la valeur (prix ou PnL)
      - 🟢 **Vert** : Valeurs élevées / Profits
      - 🟡 **Jaune** : Valeurs moyennes
      - 🔴 **Rouge** : Valeurs faibles / Pertes
    
    ### À quoi servent nos heatmaps ?
    
    **1. Heatmaps de Prix** : Visualisent comment le prix des options Call et Put évolue selon différents 
    scénarios de prix spot et de volatilité. Cela permet d'identifier rapidement les zones où l'option 
    a le plus de valeur.
    
    **2. Heatmaps de PnL (Profit & Loss)** : Montrent le profit ou la perte réalisé sur votre position 
    en fonction des variations de marché. Le PnL est calculé comme :
    
    ```
    PnL = Prix Actuel de l'Option - Prix d'Achat
    ```
    
    Ces visualisations vous aident à comprendre les risques et opportunités de vos positions d'options 
    dans différents scénarios de marché.
    """)
    
    st.info("👆 **Ajustez les paramètres dans la barre latérale et cliquez sur 'Calculer' pour générer les résultats.**")
    
else:
    # Table des entrées
    input_data = {
        "Prix Actuel de l'Actif": [current_price],
        "Prix d'Exercice (Strike)": [strike],
        "Temps jusqu'à Maturité (Années)": [time_to_maturity],
        "Volatilité (σ)": [volatility],
        "Taux d'Intérêt Sans Risque": [interest_rate],
    }
    input_df = pd.DataFrame(input_data)
    st.table(input_df)

    # Calcul des valeurs Call et Put
    bs_model = BlackScholes(time_to_maturity, strike, current_price, volatility, interest_rate)
    call_price, put_price = bs_model.calculate_prices()

    # Affichage des valeurs Call et Put dans des tableaux colorés
    col1, col2 = st.columns([1,1], gap="small")

    with col1:
        st.markdown(f"""
            <div class="metric-container metric-call">
                <div>
                    <div class="metric-label">Valeur du CALL</div>
                    <div class="metric-value">{call_price:.2f}€</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-container metric-put">
                <div>
                    <div class="metric-label">Valeur du PUT</div>
                    <div class="metric-value">{put_price:.2f}€</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    st.title("Prix des Options - Heatmaps Interactives")
    st.info("Explorez comment les prix des options fluctuent avec différents niveaux de 'Prix Spot et Volatilité', tout en maintenant un 'Prix d'Exercice' constant.")

    # Heatmaps interactives pour les prix des options Call et Put
    col1, col2 = st.columns([1,1], gap="small")

    with col1:
        st.subheader("Heatmap Prix du Call")
        heatmap_fig_call, _ = plot_heatmap(bs_model, spot_range, vol_range, strike)
        st.pyplot(heatmap_fig_call)

    with col2:
        st.subheader("Heatmap Prix du Put")
        _, heatmap_fig_put = plot_heatmap(bs_model, spot_range, vol_range, strike)
        st.pyplot(heatmap_fig_put)

    st.markdown("---")
    st.title("Profit & Loss (PnL) - Heatmaps Interactives")
    st.info("Visualisez le profit ou la perte sur vos positions d'options en fonction de différents niveaux de 'Prix Spot et Volatilité'. Le PnL est calculé comme : Prix Actuel de l'Option - Prix d'Achat.")

    # Heatmaps interactives pour le PnL des options Call et Put
    col1, col2 = st.columns([1,1], gap="small")

    with col1:
        st.subheader("Heatmap PnL du Call")
        heatmap_fig_call_pnl, _ = plot_pnl_heatmap(bs_model, spot_range, vol_range, strike, 
                                                    call_purchase_price, put_purchase_price)
        st.pyplot(heatmap_fig_call_pnl)

    with col2:
        st.subheader("Heatmap PnL du Put")
        _, heatmap_fig_put_pnl = plot_pnl_heatmap(bs_model, spot_range, vol_range, strike, 
                                                   call_purchase_price, put_purchase_price)
        st.pyplot(heatmap_fig_put_pnl)