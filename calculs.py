"""Fonctions de calcul du site (sans Streamlit), pour pouvoir les tester."""
import math

import pandas as pd

# ------------------------------------------------------------------ financement


def _taux_mensuel(taux_annuel_pct):
    return taux_annuel_pct / 100 / 12


def mensualite(capital, taux_annuel_pct, mois):
    """Mensualité constante d'un prêt amortissable (hors assurance)."""
    if capital <= 0 or mois <= 0:
        return 0.0
    t = _taux_mensuel(taux_annuel_pct)
    if t == 0:
        return capital / mois
    return capital * t / (1 - (1 + t) ** -mois)


def capital_empruntable(mensualite_max, taux_annuel_pct, mois):
    """Capital que l'on peut emprunter pour une mensualité donnée."""
    if mensualite_max <= 0 or mois <= 0:
        return 0.0
    t = _taux_mensuel(taux_annuel_pct)
    if t == 0:
        return mensualite_max * mois
    return mensualite_max * (1 - (1 + t) ** -mois) / t


def amortissement(capital, taux_annuel_pct, mois):
    """Tableau d'amortissement : capital et intérêts cumulés, capital restant dû."""
    t = _taux_mensuel(taux_annuel_pct)
    m = mensualite(capital, taux_annuel_pct, mois)
    reste, capital_cumule, interets_cumules = capital, 0.0, 0.0
    lignes = []
    for k in range(1, mois + 1):
        interets = reste * t
        rembourse = m - interets
        reste -= rembourse
        capital_cumule += rembourse
        interets_cumules += interets
        lignes.append(
            {
                "Mois": k,
                "Capital remboursé": capital_cumule,
                "Intérêts payés": interets_cumules,
                "Capital restant dû": max(reste, 0.0),
            }
        )
    return pd.DataFrame(lignes).set_index("Mois")


# ------------------------------------------------------------------ marges


def marge_commerciale(prix_achat_ht, prix_vente_ht):
    return prix_vente_ht - prix_achat_ht


def taux_de_marge(prix_achat_ht, prix_vente_ht):
    """Marge ÷ prix d'achat HT."""
    return (prix_vente_ht - prix_achat_ht) / prix_achat_ht


def taux_de_marque(prix_achat_ht, prix_vente_ht):
    """Marge ÷ prix de vente HT."""
    return (prix_vente_ht - prix_achat_ht) / prix_vente_ht


def coefficient_multiplicateur(prix_achat_ht, prix_vente_ht, tva_pct):
    """Prix de vente TTC ÷ prix d'achat HT."""
    return prix_vente_ht * (1 + tva_pct / 100) / prix_achat_ht


def pv_depuis_taux_de_marge(prix_achat_ht, taux_pct):
    return prix_achat_ht * (1 + taux_pct / 100)


def pv_depuis_taux_de_marque(prix_achat_ht, taux_pct):
    return prix_achat_ht / (1 - taux_pct / 100)


# ------------------------------------------------------------------ rentabilité


def seuil_rentabilite(charges_fixes, prix_vente_unitaire, cout_variable_unitaire):
    """Seuil de rentabilité, ou None si la marge sur coût variable est <= 0."""
    mcv_unitaire = prix_vente_unitaire - cout_variable_unitaire
    if mcv_unitaire <= 0:
        return None
    taux_mcv = mcv_unitaire / prix_vente_unitaire
    return {
        "mcv_unitaire": mcv_unitaire,
        "taux_mcv": taux_mcv,
        "quantite": math.ceil(round(charges_fixes / mcv_unitaire, 9)),
        "chiffre_affaires": charges_fixes / taux_mcv,
    }


def courbe_resultat(charges_fixes, mcv_unitaire, quantite_seuil, points=60):
    """Résultat (bénéfice ou perte) selon la quantité vendue."""
    q_max = max(math.ceil(quantite_seuil * 2), 10)
    pas = max(q_max // points, 1)
    quantites = list(range(0, q_max + 1, pas))
    return pd.DataFrame(
        {
            "Quantité vendue": quantites,
            "Résultat (€)": [q * mcv_unitaire - charges_fixes for q in quantites],
        }
    )
