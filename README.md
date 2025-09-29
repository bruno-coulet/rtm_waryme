## Scipt de scraping hebdomadaire du site waryme

### .env
Les identifiants de connexion sont sur le fichier .env (absent de ce repository)

### Chromedriver

Selenium utilise chrome driver qui "dialoguer" avec le lnavigateur
Pour installer Chrome driver, il faut vérifier la version de Chrome dans la barre d'adresse (URL):
chrome://settings/help

Par exemple :
>>> Version 140.0.7339.80 (Build officiel) (64 bits)

Il faut télécharger une version compatible de chromedriver à cette adresse :
https://googlechromelabs.github.io/chrome-for-testing/


Puis placer l’exécutable sur la machine (par exemple C:\Tools\chromedriver.exe) et indique le chemin dans .env :

CHROMEDRIVER_PATH=C:\Tools\chromedriver.exe

### Alternative webdriver-manager
webdriver-manager est une librairie qui gère ça automatiquement, pas besoin de télécharger ni de gérer la compatibilité :

`pip install webdriver-manager`

Dans le code Python, remplacer par exemple :

```python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
```
→ Dans ce cas, le CHROMEDRIVER_PATH de ton .env ne sert plus à rien.
