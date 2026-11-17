import pytest

from calculs import (
    amortissement,
    capital_empruntable,
    coefficient_multiplicateur,
    marge_commerciale,
    mensualite,
    pv_depuis_taux_de_marge,
    pv_depuis_taux_de_marque,
    seuil_rentabilite,
    taux_de_marge,
    taux_de_marque,
)


def test_mensualite_sans_interets():
    assert mensualite(10_000, 0, 10) == pytest.approx(1_000)


def test_mensualite_et_capital_sont_inverses():
    m = mensualite(13_000, 5.9, 48)
    assert capital_empruntable(m, 5.9, 48) == pytest.approx(13_000)


def test_amortissement_solde_le_pret():
    df = amortissement(13_000, 5.9, 48)
    assert len(df) == 48
    assert df["Capital restant dû"].iloc[-1] == pytest.approx(0, abs=1e-6)
    assert df["Capital remboursé"].iloc[-1] == pytest.approx(13_000)
    total_paye = mensualite(13_000, 5.9, 48) * 48
    assert df["Capital remboursé"].iloc[-1] + df["Intérêts payés"].iloc[-1] == pytest.approx(total_paye)


def test_pas_de_pret_si_capital_nul():
    assert mensualite(0, 5, 12) == 0


def test_marges():
    assert marge_commerciale(100, 150) == 50
    assert taux_de_marge(100, 150) == pytest.approx(0.5)
    assert taux_de_marque(100, 150) == pytest.approx(1 / 3)
    assert coefficient_multiplicateur(100, 150, 20) == pytest.approx(1.8)


def test_prix_de_vente_depuis_les_taux():
    assert pv_depuis_taux_de_marge(100, 50) == pytest.approx(150)
    assert pv_depuis_taux_de_marque(60, 40) == pytest.approx(100)


def test_seuil_de_rentabilite():
    s = seuil_rentabilite(3_000, 50, 30)
    assert s["quantite"] == 150
    assert s["taux_mcv"] == pytest.approx(0.4)
    assert s["chiffre_affaires"] == pytest.approx(7_500)


def test_seuil_impossible_si_prix_inferieur_au_cout():
    assert seuil_rentabilite(3_000, 30, 30) is None
    assert seuil_rentabilite(3_000, 20, 30) is None
