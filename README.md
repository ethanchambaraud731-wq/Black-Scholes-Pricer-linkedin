# Black-Scholes Options Pricer

Application interactive de pricing d’options basée sur le modèle Black-Scholes, intégrant des visualisations avancées (heatmaps) et une interface Streamlit.

---

## 🎯 Objectif du projet

Ce projet fournit un outil visuel permettant d’analyser le prix théorique d’options européennes (Call / Put) via le modèle Black-Scholes.
L’application permet d’étudier l’impact des paramètres de marché sur :

* les prix des options
* les sensibilités (Greeks)
* le Profit & Loss (PnL) d’une position
* les surfaces Spot × Volatilité

Elle combine un moteur de calcul Python (`main.py`) et une interface utilisateur interactive (`streamlit_app.py`).

---

## 🧠 Modèle utilisé : Black-Scholes

Le pricing repose sur les paramètres suivants :

* **S** : prix spot
* **K** : prix d’exercice
* **T** : maturité (années)
* **σ** : volatilité
* **r** : taux sans risque

Formules :

**Call :**
`C = S·N(d1) − K·e^(−rT)·N(d2)`

**Put :**
`P = K·e^(−rT)·N(−d2) − S·N(−d1)`

Où :

```
d1 = [ln(S/K) + (r + σ²/2)T] / (σ√T)
d2 = d1 − σ√T
```

L’application calcule également :
**Delta**, **Gamma**, surfaces de prix, surfaces de PnL.

---

## 🖥️ Fonctionnalités principales

### ✔ Interface Streamlit interactive

* Paramétrage du spot, strike, taux, maturité, volatilité.
* Choix des plages pour les heatmaps.
* Sections séparées : Pricing, Greeks, Visualisations, PnL.

### ✔ Calcul en temps réel

* Prix Call / Put
* Delta & Gamma

### ✔ Visualisations avancées

* Heatmaps du prix (Spot × Vol)
* Heatmaps du PnL
* Courbes et outputs dynamiques

### ✔ Structure modulaire

* `main.py` : moteur de calcul
* `streamlit_app.py` : interface visuelle
* Architecture extensible

---

## 🚀 Déploiement local

### 1️⃣ Cloner le repository

```bash
git clone https://github.com/ethanchambaraud731-wq/black-scholes-pricer-linkedin.git
cd black-scholes-pricer
```

### 2️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3️⃣ Exécuter l’application

```bash
streamlit run streamlit_app.py
```

---

## 🌐 Déploiement en ligne (Streamlit Cloud)

1. Se connecter avec GitHub
2. Sélectionner le repository
3. Choisir `streamlit_app.py` comme fichier principal
4. Lancer le déploiement

Streamlit Cloud reconstruit automatiquement l’environnement à partir de `requirements.txt`.

---

## 📁 Architecture du projet

```
│
├── streamlit_app.py       # Interface utilisateur & visualisations
├── main.py                # Logique métier (pricing Black-Scholes)
├── requirements.txt       # Dépendances Python
└── README.md              # Documentation
```

---

## 👤 Auteur

**Ethan Chambaraud**
LinkedIn : [https://www.linkedin.com/in/ethan-chambaraud](https://www.linkedin.com/in/ethan-chambaraud)

---

## 📬 Contact

Pour toute question ou proposition de collaboration :
📧 ethanchambaraud731@gmail.com

---

