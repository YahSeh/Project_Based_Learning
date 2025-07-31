# Synthèse - Application d'Analyse de Retours Clients avec Streamlit

## Objectif
Développer une mini-application Python avec une interface web pour analyser les réponses à un questionnaire de satisfaction client, à partir d'un fichier JSON hébergé en ligne.

## Tâches Attendues
1. **Chargement Dynamique des Données**
   - Télécharger automatiquement le fichier JSON depuis l'URL au chargement de la page.
   - Lire les données en Python (utilisation de `requests` et `json`).

2. **Analyse des Données**
   - Calculer et afficher dans l'interface :
     - Nombre total de retours.
     - Score moyen.
     - Répartition des scores en détracteurs, neutres, satisfaits et promoteurs.
     - Pourcentage de promoteurs.

3. **Interface Utilisateur Web (Streamlit)**
   - Créer une interface web simple pour visualiser le rapport :
     - Affichage clair des statistiques d'analyse.
     - Présentation structurée et facile à lire.
     - Liste des commentaires des détracteurs avec leurs emails.

4. **Fonctionnalités Additionnelles**
   - Visualisation graphique de la répartition des scores (bonus).
   - Recherche par email.
   - Bouton pour recharger les données depuis l'URL.
   - Navigation simplifiée dans les avis (filtrage, tri).

## Implémentation
- Utilisation de Python avec les bibliothèques `streamlit`, `requests` et `json`.
- Gestion des requêtes HTTP pour récupérer les données JSON.
- Utilisation de `streamlit` pour créer une interface utilisateur interactive et réactive.

## Structure du Script
- **Chargement des Données :** Utilisation de `requests.post` pour récupérer les données JSON depuis l'URL.
- **Calcul des Statistiques :** Calcul du nombre total de retours, du score moyen et de la répartition des scores.
- **Interface Utilisateur (Streamlit) :** Utilisation de `st.title`, `st.header`, `st.write`, `st.subheader` pour afficher les informations d'analyse et les commentaires.
- **Gestion des Erreurs :** Gestion des exceptions pour les erreurs de requête HTTP et de décodage JSON.

## Personnalisation de l'Interface
- Affichage des statistiques avec des options de tri et de filtre.
- Style des commentaires avec encadrement, mise en gras pour l'email, et coloration du score.

## Instructions d'Utilisation
1. Cloner le script Python.
2. Installer les dépendances (`streamlit`, `requests`).
3. Exécuter localement (`streamlit run script.py`).
4. Accéder à l'interface web générée sur `localhost`.

## Exemple de Code
Voici un exemple simplifié du script principal :

```python
def fetch_data(url):
    try:
        response = requests.post(url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur lors de la récupération des données : {response.status_code}")
    except requests.RequestException as e:
        st.error(f"Erreur lors de la requête : {e}")
    return None

# URL de l'API JSON
url = "https://n8n.greenkub.fr/webhook/b8f3ceeb-2df0-435f-b44d-1c56cd8a8078"

# Chargement des données
data = fetch_data(url)
