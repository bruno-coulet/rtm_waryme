📄 README — WaryMe Extractor

Ce projet permet d’automatiser l’extraction des références du site WaryMe sur une période donnée (la dernière semaine complète lundi → dimanche).
Le script utilise Playwright pour interagir avec l’interface web et exporter les données au format CSV.

📦 Prérequis
1️⃣ Python

Assurez-vous d’avoir Python 3.9+ installé.

2️⃣ Dépendances

Installez les dépendances du projet :

pip install -r requirements.txt


⚠️ Si Playwright n’a jamais été installé sur la machine, exécuter ensuite :

playwright install

3️⃣ Variables d’environnement

Créez un fichier .env à la racine du projet :

WARYME_USER=mon.email@exemple.com
WARYME_PASSWORD=monMotDePasse
REPORT_EMAIL_DEST=user@exemple.com


Optionnel : configurer un serveur SMTP si l’envoi automatique par email est activé.

▶️ Lancer le script
python main.py


Le script :

Se connecte au site WaryMe

Sélectionne automatiquement la dernière semaine complète

Exporte les résultats en CSV

Sauvegarde le fichier dans le dossier du projet

Peut envoyer le CSV par email si configuré

🧠 Architecture
├─ main.py               → Script principal
├─ utils.py              → Fonctions utilitaires (dates, logs, navigation…)
├─ requirements.txt      → Dépendances Python
└─ .env                  → Identifiants / configuration privée (non versionnée)

🔒 Sécurité

Ne jamais commiter .env dans Git

Les identifiants sont chargés via variables d’environnement



🛠 Support & maintenance

Le passage à Playwright permet :

Une automatisation plus fiable

Moins de risques de dysfonctionnement en cas de mise à jour Chrome

Une meilleure gestion des applications Angular

Si le site évolue (nouvelles classes CSS, changement structure DOM),
adapter les sélecteurs dans utils.py.
