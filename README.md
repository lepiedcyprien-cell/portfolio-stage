# Mon site de recherche de stage

Un petit site en Python (Streamlit) à mettre en lien sur LinkedIn : mon profil, plus deux outils utiles dans la vente automobile.

- **Simulateur de financement auto** : mensualité, coût du crédit, budget maximal selon les revenus du client
- **Calculateur de marge et de seuil de rentabilité** : taux de marge, taux de marque, coefficient multiplicateur, seuil en quantités et en chiffre d'affaires

## 1. Personnaliser

Ouvre `app.py` et modifie le bloc **À PERSONNALISER** tout en haut :
prénom et nom, liens LinkedIn / GitHub / e-mail, compétences, projets.
Mets `""` pour masquer un bouton. Relis bien chaque phrase : c'est ta vitrine.

## 2. Tester sur ton ordinateur

```bash
pip install -r requirements.txt
streamlit run app.py
```

Le site s'ouvre sur http://localhost:8501.
Les tests des calculs se lancent avec `pip install pytest` puis `pytest`.

## 3. Le mettre en ligne (lien ouvert à tous)

1. Crée un dépôt **public** sur GitHub (par exemple `portfolio-stage`) et envoie-y tous les fichiers de ce dossier, y compris `.streamlit/config.toml` (ce dernier est facultatif, il ne sert qu'au thème) :

   ```bash
   git init
   git add .
   git commit -m "Portfolio stage"
   git branch -M main
   git remote add origin https://github.com/TON-PSEUDO/portfolio-stage.git
   git push -u origin main
   ```

2. Va sur https://share.streamlit.io et connecte-toi avec ton compte GitHub.
3. Clique sur **Create app**, puis **Yup, I have an app**.
4. Choisis ton dépôt, la branche `main` et le fichier `app.py`.
5. Dans **App URL**, choisis un nom court (ce sera ton lien en `.streamlit.app`).
6. Clique sur **Deploy** et attends quelques minutes.

## 4. L'afficher sur LinkedIn

- Colle le lien dans **Coordonnées > Site web**.
- Ajoute-le aussi dans la section **En vedette**, avec le lien de ton dépôt GitHub.
- Ouvre ton lien une fois avant de le partager pour vérifier que tout s'affiche.

## Structure

| Fichier | Rôle |
|---|---|
| `app.py` | Interface (Streamlit) et contenu du profil |
| `calculs.py` | Formules, séparées de l'interface |
| `test_calculs.py` | Tests automatiques (pytest) |
| `requirements.txt` | Dépendances |

Les résultats sont des estimations pédagogiques, pas une offre de crédit.
