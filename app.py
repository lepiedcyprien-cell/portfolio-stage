"""Portfolio interactif pour ma recherche de stage (Streamlit).

En local :  pip install -r requirements.txt  puis  streamlit run app.py
"""
import streamlit as st

from calculs import (
    amortissement,
    capital_empruntable,
    coefficient_multiplicateur,
    courbe_resultat,
    marge_commerciale,
    mensualite,
    pv_depuis_taux_de_marge,
    pv_depuis_taux_de_marque,
    seuil_rentabilite,
    taux_de_marge,
    taux_de_marque,
)

# =============================================================================
# À PERSONNALISER : tout ce qui est affiché sur ta page est ici
# =============================================================================
PRENOM_NOM = "Cyprien Lepied"
ACCROCHE = "Étudiant en 1re année de BUT Techniques de Commercialisation, passionné d'automobile"
ECOLE = "IUT de Rambouillet (Vélizy-Rambouillet)"
STAGE_PERIODE = "du 11 janvier au 5 février 2027"
SECTEUR = "Commerce et vente automobile"
LIEU = "Rambouillet et environs"

# Laisse "" pour masquer un bouton
LINKEDIN = "www.linkedin.com/in/cyprien-lepied-051102356"
GITHUB = "https://github.com/lepiedcyprien-cell/portfolio-stage"
EMAIL = "lepiedcyprien@gmail.com"
CV_URL = ""  # lien vers ton CV en PDF (Drive, GitHub...), optionnel

COMPETENCES = {
    "Vente & relation client": ["Techniques de vente", "Prospection et prise de contact", "Relation client"],
    "Marketing & communication": ["Communication commerciale", "Benchmark concurrentiel", "Analyse de campagnes"],
    "Gestion & outils": ["Marges et seuil de rentabilité", "Python (Streamlit, pandas)", "Git / GitHub"],
}

PROJETS = [
    ("Benchmark concurrentiel", "Étude comparative de marques concurrentes d'un même marché (SAÉ Communication commerciale)."),
    ("Analyse d'une campagne de communication", "Annonceur, agence, objectifs, cibles, médias et hors-médias, message, budget."),
    ("Démarche de recherche de stage", "Ciblage d’entreprises, candidatures (CV, lettre de motivation) et suivi dans un tableau (SAÉ Vente)."),
    ("Ce site", "Appli web en Python : interface Streamlit, calculs testés avec pytest, déployée en ligne."),
]
# =============================================================================

st.set_page_config(page_title=f"{PRENOM_NOM} · Recherche de stage", page_icon="🚗")


def eur(x, decimales=0):
    texte = f"{x:,.{decimales}f}".replace(",", " ").replace(".", ",")
    return f"{texte} €"


def pct(x, decimales=1):
    return f"{x:.{decimales}f}".replace(".", ",") + " %"


# ------------------------------------------------------------------ en-tête

st.title(PRENOM_NOM)
st.markdown(f"**{ACCROCHE}**  \n{ECOLE}")
st.success(f"🎯 **Je recherche un stage** {STAGE_PERIODE} · {SECTEUR} · {LIEU}")

liens = [("LinkedIn", LINKEDIN), ("GitHub", GITHUB), ("Email", f"mailto:{EMAIL}" if EMAIL else ""), ("Mon CV", CV_URL)]
liens = [(nom, url) for nom, url in liens if url]
if liens:
    for colonne, (nom, url) in zip(st.columns(len(liens)), liens):
        colonne.link_button(nom, url)

tab_profil, tab_credit, tab_marge, tab_capot = st.tabs(
    ["👋 Profil", "🚗 Financement auto", "📊 Marge et rentabilité", "🛠️ Sous le capot"]
)

# ------------------------------------------------------------------ profil

with tab_profil:
    st.subheader("Ce que je sais faire")
    for colonne, (categorie, items) in zip(st.columns(len(COMPETENCES)), COMPETENCES.items()):
        colonne.markdown(f"**{categorie}**")
        colonne.markdown("\n".join(f"- {i}" for i in items))

    st.subheader("Projets")
    for titre, description in PROJETS:
        st.markdown(f"**{titre}** : {description}")

    st.subheader("Pourquoi ce site ?")
    st.write(
        "Plutôt qu'un simple CV, j'ai codé deux outils que j'aurais envie d'utiliser en concession : "
        "expliquer un budget et une mensualité à un client, et savoir si un prix de vente laisse assez de marge. "
        "Essaie-les dans les onglets ci-dessus."
    )

# ------------------------------------------------------------------ financement

with tab_credit:
    st.subheader("Simulateur de financement automobile")
    st.caption("Mensualité, coût du crédit, et budget maximal selon les revenus du client.")

    c1, c2 = st.columns(2)
    prix = c1.number_input("Prix du véhicule (€)", min_value=0, value=15000, step=500, key="prix")
    apport = c2.number_input("Apport (€)", min_value=0, value=2000, step=500, key="apport")
    duree = c1.slider("Durée (mois)", min_value=12, max_value=96, value=48, step=6, key="duree")
    taux = c2.number_input("Taux annuel nominal (%)", min_value=0.0, max_value=25.0, value=5.9, step=0.1, key="taux")

    emprunt = max(prix - apport, 0)
    if emprunt == 0:
        st.info("L'apport couvre le prix du véhicule : aucun crédit nécessaire.")
    else:
        mens = mensualite(emprunt, taux, duree)
        total_credit = mens * duree
        m1, m2, m3 = st.columns(3)
        m1.metric("Mensualité", eur(mens, 2))
        m2.metric("Coût du crédit", eur(total_credit - emprunt))
        m3.metric("Total payé, apport inclus", eur(apport + total_credit))

        tableau = amortissement(emprunt, taux, duree)
        st.area_chart(tableau[["Capital remboursé", "Intérêts payés"]])
        st.caption(
            f"Montant emprunté : {eur(emprunt)}. Le graphique montre ce qui a été payé au fil des mois, "
            "réparti entre capital et intérêts."
        )

    st.divider()
    st.markdown("#### Quel budget selon les revenus du client ?")
    c1, c2 = st.columns(2)
    revenu = c1.number_input("Revenu mensuel net (€)", min_value=0, value=2000, step=100, key="revenu")
    charges = c2.number_input("Crédits déjà en cours (€ par mois)", min_value=0, value=0, step=50, key="charges")
    endettement = st.slider("Taux d'endettement maximum (%)", min_value=20, max_value=40, value=35, key="endettement")

    mens_max = max(revenu * endettement / 100 - charges, 0)
    budget_emprunt = capital_empruntable(mens_max, taux, duree)
    b1, b2 = st.columns(2)
    b1.metric("Mensualité maximale", eur(mens_max, 2))
    b2.metric("Budget véhicule maximal", eur(budget_emprunt + apport), help="Capital empruntable + apport saisi plus haut.")
    st.caption(
        "35 % est un repère couramment utilisé ; chaque organisme de crédit applique sa propre politique. "
        "Les calculs sont hors assurance emprunteur et frais de dossier, avec un taux nominal (et non un TAEG)."
    )

# ------------------------------------------------------------------ marge

with tab_marge:
    st.subheader("Calculateur de marge commerciale")
    c1, c2 = st.columns(2)
    pa = c1.number_input("Prix d'achat HT (€)", min_value=0.01, value=100.0, step=1.0, key="pa")
    tva = c2.selectbox("TVA", [20.0, 10.0, 5.5, 0.0], format_func=lambda v: f"{v:g} %", key="tva")
    depart = st.radio(
        "Je pars de…",
        ["un prix de vente HT", "un taux de marge", "un taux de marque"],
        horizontal=True,
        key="depart",
    )
    if depart == "un prix de vente HT":
        pv = st.number_input("Prix de vente HT (€)", min_value=0.01, value=150.0, step=1.0, key="pv_in")
    elif depart == "un taux de marge":
        tm = st.number_input("Taux de marge souhaité (%)", min_value=0.0, value=50.0, step=1.0, key="tm_in")
        pv = pv_depuis_taux_de_marge(pa, tm)
    else:
        tq = st.number_input("Taux de marque souhaité (%)", min_value=0.0, max_value=95.0, value=33.0, step=1.0, key="tq_in")
        pv = pv_depuis_taux_de_marque(pa, tq)

    r1, r2, r3 = st.columns(3)
    r1.metric("Prix de vente HT", eur(pv, 2))
    r2.metric("Prix de vente TTC", eur(pv * (1 + tva / 100), 2))
    r3.metric("Marge commerciale", eur(marge_commerciale(pa, pv), 2))
    r4, r5, r6 = st.columns(3)
    r4.metric("Taux de marge", pct(taux_de_marge(pa, pv) * 100))
    r5.metric("Taux de marque", pct(taux_de_marque(pa, pv) * 100))
    r6.metric("Coefficient multiplicateur", f"{coefficient_multiplicateur(pa, pv, tva):.2f}".replace(".", ","))

    with st.expander("Les formules"):
        st.markdown(
            "- Marge commerciale = prix de vente HT − prix d'achat HT\n"
            "- Taux de marge = marge ÷ prix d'achat HT\n"
            "- Taux de marque = marge ÷ prix de vente HT\n"
            "- Coefficient multiplicateur = prix de vente TTC ÷ prix d'achat HT"
        )

    st.divider()
    st.subheader("Seuil de rentabilité")
    a, b, c = st.columns(3)
    cf = a.number_input("Charges fixes (€ par mois)", min_value=0.0, value=3000.0, step=100.0, key="cf")
    pvu = b.number_input("Prix de vente unitaire HT (€)", min_value=0.0, value=50.0, step=1.0, key="pvu")
    cvu = c.number_input("Coût variable unitaire (€)", min_value=0.0, value=30.0, step=1.0, key="cvu")

    seuil = seuil_rentabilite(cf, pvu, cvu)
    if seuil is None:
        st.warning("Le prix de vente doit être supérieur au coût variable unitaire pour atteindre un seuil.")
    else:
        s1, s2, s3 = st.columns(3)
        s1.metric("Seuil en quantités", f"{seuil['quantite']} unités")
        s2.metric("Seuil en chiffre d'affaires", eur(seuil["chiffre_affaires"]))
        s3.metric("Taux de marge sur coût variable", pct(seuil["taux_mcv"] * 100))
        if seuil["quantite"] == 0:
            st.write("Sans charges fixes, l'activité est rentable dès la première vente.")
        else:
            st.write(f"Au-delà de **{seuil['quantite']} ventes** par mois, l'activité dégage un bénéfice.")
        st.line_chart(courbe_resultat(cf, seuil["mcv_unitaire"], seuil["quantite"]), x="Quantité vendue", y="Résultat (€)")

# ------------------------------------------------------------------ sous le capot

with tab_capot:
    st.subheader("Comment ce site est fait")
    st.markdown(
        "- **Python 3**, interface avec **Streamlit**, tableaux et graphiques avec **pandas**\n"
        "- `app.py` : l'interface ; `calculs.py` : les formules, séparées de l'interface ; "
        "`test_calculs.py` : les tests automatiques (pytest)\n"
        "- Déployé gratuitement depuis GitHub, avec un lien ouvert à tous"
    )
    if GITHUB:
        st.link_button("Voir le code sur GitHub", GITHUB)
    st.caption("Les résultats sont des estimations pédagogiques, pas une offre de crédit.")
