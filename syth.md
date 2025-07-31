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
- Affichage des statistiques avec des options de tri et de filtre :
     - Recherche par adresse mail avec auto-complétion.
     - Recherche par tranche de score selon les différentes catégories.
     - Tri par date (plus récent au plus ancient ou inversement).
     - Tri par score (croissant/décroissant).
- Style des commentaires avec encadrement, mise en gras pour l'email, et coloration du score.
- Graphique représentant le nombre de commentaires par catégorie de score en fonction du tri.

## Instructions d'Utilisation
1. Cloner le script Python.
2. Installer les dépendances (`streamlit`, `requests`, `matplotlib`, `numpy`).
3. Exécuter localement (`streamlit run test_greenkub.py`).
4. Accéder à l'interface web générée sur `localhost`.
