import logging
from black_scholes import BlackScholesPricer

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


def display_header():
    """Affiche le header du bot."""
    print("\n" + "="*60)
    print("     BLACK-SCHOLES OPTION PRICING BOT")
    print("="*60)


def get_validated_input(prompt, validation_func=None, error_msg="Valeur invalide"):
    """
    Récupère et valide un input utilisateur.
    
    Args:
        prompt (str): Message à afficher
        validation_func (callable): Fonction de validation
        error_msg (str): Message d'erreur personnalisé
        
    Returns:
        float: Valeur validée
    """
    while True:
        try:
            value = float(input(prompt))
            if validation_func and not validation_func(value):
                print(f"❌ {error_msg}")
                continue
            return value
        except ValueError:
            print("❌ Veuillez entrer un nombre valide.")
        except KeyboardInterrupt:
            print("\n\n👋 Programme interrompu par l'utilisateur.")
            exit(0)


def run_bot():
    """Point d'entrée principal du bot de pricing."""
    display_header()
    
    try:
        print("\n📊 Entrez les paramètres de l'option :\n")
        
        # Récupération des inputs avec validation
        S = get_validated_input(
            "   Cours actuel du sous-jacent (S) : ",
            lambda x: x > 0,
            "Le prix doit être strictement positif"
        )
        
        K = get_validated_input(
            "   Strike (K) : ",
            lambda x: x > 0,
            "Le strike doit être strictement positif"
        )
        
        r = get_validated_input(
            "   Taux sans risque (r, ex: 0.03 pour 3%) : ",
            None,
            "Taux invalide"
        )
        
        sigma = get_validated_input(
            "   Volatilité (sigma, ex: 0.25 pour 25%) : ",
            lambda x: x >= 0,
            "La volatilité ne peut pas être négative"
        )
        
        T = get_validated_input(
            "   Maturité (T en années, ex: 0.5 pour 6 mois) : ",
            lambda x: x >= 0,
            "La maturité ne peut pas être négative"
        )
        
        logger.info("Calcul des prix et Greeks en cours...")
        
        # Instanciation du pricer
        pricer = BlackScholesPricer(S, K, r, sigma, T)
        
        # Calcul des prix
        call_price = pricer.call_price()
        put_price = pricer.put_price()
        
        # Calcul des Greeks
        greeks_call = pricer.get_all_greeks('call')
        greeks_put = pricer.get_all_greeks('put')
        
        # Affichage des résultats
        print("\n" + "="*60)
        print("                    RÉSULTATS")
        print("="*60)
        
        print("\n💰 PRIX DES OPTIONS")
        print("-" * 60)
        print(f"   Call Price : {call_price:>10.4f} €")
        print(f"   Put Price  : {put_price:>10.4f} €")
        
        print("\n📈 GREEKS DU CALL")
        print("-" * 60)
        print(f"   Delta      : {greeks_call['delta']:>10.4f}")
        print(f"   Gamma      : {greeks_call['gamma']:>10.4f}")
        print(f"   Vega       : {greeks_call['vega']:>10.4f}")
        print(f"   Theta      : {greeks_call['theta']:>10.4f} (par jour)")
        print(f"   Rho        : {greeks_call['rho']:>10.4f}")
        
        print("\n📉 GREEKS DU PUT")
        print("-" * 60)
        print(f"   Delta      : {greeks_put['delta']:>10.4f}")
        print(f"   Gamma      : {greeks_put['gamma']:>10.4f}")
        print(f"   Vega       : {greeks_put['vega']:>10.4f}")
        print(f"   Theta      : {greeks_put['theta']:>10.4f} (par jour)")
        print(f"   Rho        : {greeks_put['rho']:>10.4f}")
        
        print("\n" + "="*60)
        
        # Informations additionnelles
        moneyness = S / K
        if moneyness > 1.05:
            status = "ITM (In The Money) pour le Call"
        elif moneyness < 0.95:
            status = "OTM (Out of The Money) pour le Call"
        else:
            status = "ATM (At The Money)"
        
        print(f"\n💡 Statut : {status}")
        print(f"   Moneyness (S/K) : {moneyness:.4f}")
        
        logger.info("Calculs terminés avec succès")
        
    except ValueError as e:
        logger.error(f"Erreur de validation : {e}")
        print(f"\n❌ Erreur : {e}")
        print("Veuillez vérifier vos paramètres et réessayer.\n")
        
    except Exception as e:
        logger.error(f"Erreur inattendue : {e}")
        print(f"\n❌ Erreur inattendue : {e}")
        print("Veuillez contacter le support si le problème persiste.\n")
    
    finally:
        print("\n👋 Merci d'avoir utilisé le Black-Scholes Pricing Bot !")
        print("="*60 + "\n")


if __name__ == "__main__":
    run_bot()
