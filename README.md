# back-olympic (Billetterie des JO)

**Description** : Ce projet étudiant comprend une version back-end pour l'administration de la billetterie des Jeux
olympiques.  Il utilise Django.


## Prérequis

- [Python 3.13.3](https://www.python.org/downloads/)

- [PostgreSQL 17.4](https://www.postgresql.org/download/)

## Installation

Pour une installation en local via le terminal de commande, suivre les étapes suivantes:

  1. Cloner le dépôt :
      ```bash
      git clone https://github.com/loki-patera/back-olympic.git
      ```

  2. À la racine du projet, entrer dans le dossier `back-olympic` :
      ```bash
      cd back-olympic
      ```
  
  3. Créer un environnement virtuel (commande Windows) :
      ```powershell
      py -m venv venv
      ```
  
  4. Activer l'environnement virtuel (commande Windows) :
      ```powershell
      venv\Scripts\activate
      ```
  
  5. Mettre à jour `pip`, si nécessaire, pour gérer les dépendances (commande Windows) :
      ```powershell
      py -m pip install --upgrade pip
      ```
  
  6. Installer les dépendances nécessaires :
      ```bash
      pip install -r requirements.txt
      ```
  
  7. Créer une base de données `posgresql` avec `pgAdmin` par exemple

  8. Créer un fichier `.env` dans le dossier `back-olympic` et, créer et compléter les variables d'environnement
  suivantes :
      ```py
      DEBUG=True

      SECRET_KEY=                     # Clé à générer pour la protection de l'application

      DJANGO_ALLOWED_HOSTS=127.0.0.1

      POSTGRES_DB=                    # Nom de la base de données créée précédemment
      POSTGRES_USER=                  # Nom de l'utilisateur de la base de données
      POSTGRES_PASSWORD=              # Mot de passe de l'utilisateur de la base de données
      POSTGRES_HOST=127.0.0.1
      POSTGRES_PORT=                  # Port utilisé pour se connecter à la base de données
      ```

  9. Préparer les migrations (commande Windows) :
      ```powershell
      py manage.py makemigrations
      ```
  
  10. Appliquer les migrations à la base de données (commande Windows) :
      ```powershell
      py manage.py migrate
      ```
  
  11. Créer un super utilisateur pour vous connecter à l'interface d'administration (commande Windows) :
      ```powershell
      py manage.py createsuperuser
      ```

## Tests

Pour consulter le résultat des tests incorporés à l'application, suivre les étapes suivantes :

  1. Lancer les tests et collecter les données de couverture :
      ```bash
      coverage run manage.py test
      ```
  
  2. Afficher un rapport des données de couverture dans le terminal :
      ```bash
      coverage report -m
      ```
  
  3. Pour obtenir un rapport détaillé en format html :
      ```bash
      coverage html
      ```

  4. Pour consulter le rapport, ouvrir le fichier `index.html` dans un navigateur.  Il se trouve dans le dossier
  `htmlcov` créé lors de l'exécution des tests.

## Utilisation

Pour utiliser l'application en local, suivre les étapes suivantes :

  1. Lancer le serveur en local (commande Windows) :
      ```powershell
      py manage.py runserver
      ```
  
  2. Ouvrir le serveur à l'adresse [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

  3. Entrer l'email et le mot de passe que vous avez créer précédemment pour le super utilisateur afin d'accéder à
  l'interface d'administration