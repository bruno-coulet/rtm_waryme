from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from dotenv import load_dotenv
import os
import time
from datetime import date, timedelta, datetime
from selenium.webdriver.common.action_chains import ActionChains
from utils import select_date
import logging
logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logging.info("Début du script")


# ========== Charger les variables d'environnement ==========
load_dotenv()
ID = os.getenv('ID')
PASSWORD = os.getenv('PASSWORD')
URL = os.getenv('URL')
URL_DOWLOAD = os.getenv('URL_DOWLOAD')

# ========== Repertoire de destination ==========
# Répertoire du script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Dossier "alertes" à côté du script
DOWNLOAD_DIR = os.path.join(BASE_DIR, "alertes")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


# ========== Options Chrome ==========
chrome_options = Options()
prefs = {
    "download.default_directory": DOWNLOAD_DIR,  # dossier où enregistrer
    "download.prompt_for_download": False,       # pas de popup
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--start-maximized")
service = Service(os.getenv('CHROMEDRIVER_PATH'))
driver = webdriver.Chrome(service=service, options=chrome_options)

# ========== Dates ==========
today = date.today()
# Lundi de la semaine précédente
start_date = today - timedelta(days=today.weekday() + 7)
# Dimanche de la semaine précédente
end_date = start_date + timedelta(days=6)
print(f"🗓️ Plage des alertes : {start_date} → {end_date}")

# Conversion en datetime pour Selenium
start_dt = datetime.combine(start_date, datetime.min.time())
end_dt = datetime.combine(end_date, datetime.min.time())



try:
    # ========== Accès page de connexion ==========
    print("Chargement de la page de connexion...")
    driver.get(URL)
    WebDriverWait(driver, 15).until(lambda d: d.execute_script('return document.readyState') == 'complete')

    # ========== Identifiant ==========
    username_element = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[formcontrolname='login']"))
    )
    username_element.click()
    username_element.clear()
    username_element.send_keys(ID)
    print(f"✅ Valeur saisie : {username_element.get_attribute('value')}")

    # ========== Clique sur "Se connecter" ==========
    next_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(),'Se connecter')]]"))
    )
    next_button.click()
    print("✅ Bouton 'Se connecter' cliqué après ID...")

    # ========== Mot de passe ==========
    password_element = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']"))
    )
    password_element.click()
    password_element.send_keys(PASSWORD + Keys.RETURN)
    print("✅ Identifiants saisis, attente de la redirection...")

    # ========== Redirection ==========
    WebDriverWait(driver, 15).until(lambda d: d.current_url != URL)
    print("✅ Redirection terminée.")

    # ========== Page de filtrage des alertes ==========
    print("✅ Accès à la page de filtrage des alertes.")
    # driver.get(URL_DOWLOAD)

    # ========= Clique sur "Alertes internes" =========
    alertes_btn = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//span[normalize-space(text())='Alertes internes']"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", alertes_btn)
    time.sleep(0.3)
    try:
        alertes_btn.click()
        print("✅ 'Alertes internes' cliqué avec click() direct")
    except:
        driver.execute_script("arguments[0].click();", alertes_btn)
        print("✅ 'Alertes internes' cliqué via JS click()")

    # =============== bouton Filtrer ===============
    print("Ciblage du bouton 'Filtrer' ")
    filtrer_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Filtrer']]"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", filtrer_btn)
    time.sleep(0.3)
    try:
        filtrer_btn.click()
        print("✅ Bouton 'Filtrer' cliqué avec click() direct")
    except:
        driver.execute_script("arguments[0].click();", filtrer_btn)
        print("✅ Bouton 'Filtrer' cliqué via JS fallback")




    # ======= Fonction pour sélectionner une date ==========
    # def select_date(driver, dt, toggle_selector="mat-datepicker-toggle[matSuffix] button", timeout=15):
    #     """
    #     Sélectionne la date `dt` (datetime) dans le mat-datepicker Angular Material :
    #     clic toggle → clic bouton période → clic année → clic mois → clic jour.
    #     """
    #     year_txt = str(dt.year)
    #     month_abbr = dt.strftime("%b").upper()
    #     day_txt = str(dt.day)

    #     def latest_overlay():
    #         overlays = driver.find_elements(By.CSS_SELECTOR, "div.cdk-overlay-pane")
    #         return overlays[-1] if overlays else None

    #     # 1) ouvrir le datepicker
    #     toggle = WebDriverWait(driver, timeout).until(
    #         EC.element_to_be_clickable((By.CSS_SELECTOR, toggle_selector))
    #     )
    #     driver.execute_script("arguments[0].click();", toggle)
    #     print("✅ Datepicker ouvert")
    #     time.sleep(0.3)

    #     overlay = WebDriverWait(driver, timeout).until(lambda d: latest_overlay())

    #     # 2) bouton période (mois/année)
    #     period_btn = WebDriverWait(overlay, timeout).until(
    #         lambda ov: ov.find_element(By.CSS_SELECTOR, "button.mat-calendar-period-button")
    #     )
    #     driver.execute_script("arguments[0].click();", period_btn)
    #     print("✅ Sélecteur mois/année ouvert")
    #     time.sleep(0.3)

    #     # 3) choisir l'année
    #     year_btn = WebDriverWait(overlay, timeout).until(
    #         lambda ov: ov.find_element(By.XPATH, f".//button[@aria-label='{year_txt}']")
    #     )
    #     driver.execute_script("arguments[0].scrollIntoView(true);", year_btn)
    #     driver.execute_script("arguments[0].click();", year_btn)
    #     print(f"✅ Année {year_txt} sélectionnée")
    #     time.sleep(0.3)

    #     # 4) choisir le mois
    #     month_btn = WebDriverWait(overlay, timeout).until(
    #         lambda ov: ov.find_element(By.XPATH, f".//span[normalize-space(text())='{month_abbr}']")
    #     )
    #     driver.execute_script("arguments[0].click();", month_btn)
    #     print(f"✅ Mois {month_abbr} sélectionné")
    #     time.sleep(0.3)

    #     # 5) choisir le jour
    #     day_btn = WebDriverWait(overlay, timeout).until(
    #         lambda ov: ov.find_element(By.XPATH, f".//span[normalize-space(text())='{day_txt}']")
    #     )
    #     driver.execute_script("arguments[0].click();", day_btn)
    #     print(f"✅ Jour {day_txt} sélectionné")
    #     time.sleep(0.3)

               
    # ======= Sélection des dates dans les datepickers ==========
    # select_date() dans le module utils.py 
    select_date(driver, start_dt, toggle_selector="mat-datepicker-toggle[data-mat-calendar='mat-datepicker-0'] button")
    select_date(driver, end_dt, toggle_selector="mat-datepicker-toggle[data-mat-calendar='mat-datepicker-1'] button")


    # ======= Cliquer sur "Appliquer les filtres" =======
    try:
        apply_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[normalize-space(text())='Appliquer les filtres']/ancestor::button")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", apply_btn)
        time.sleep(0.2)
        try:
            apply_btn.click()
            print("✅ Bouton 'Appliquer les filtres' cliqué")
        except:
            driver.execute_script("arguments[0].click();", apply_btn)
            print("✅ Bouton 'Appliquer les filtres' cliqué via JS fallback")
    except TimeoutException:
        print("❌ Bouton 'Appliquer les filtres' non trouvé ou non cliquable")



    # ======= Cliquer sur "Exporter" =======
    try:
        export_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[normalize-space(text())='Exporter']/ancestor::button")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", export_btn)
        time.sleep(0.2)
        try:
            before = set(os.listdir(DOWNLOAD_DIR))
            export_btn.click()
            print("✅ Bouton 'Exporter' cliqué, téléchargement CSV lancé")
        
            # --- Attente du fichier ---
            timeout = 60
            file_path = None
            end_time = time.time() + timeout

            while time.time() < end_time:
                after = set(os.listdir(DOWNLOAD_DIR))
                new_files = after - before
                csvs = [f for f in new_files if f.endswith(".csv") and not f.endswith(".crdownload")]
                if csvs:
                    file_path = os.path.join(DOWNLOAD_DIR, csvs[0])
                    # Vérifier si téléchargement terminé (pas de .crdownload)
                    if not file_path.endswith(".crdownload"):
                        break
                time.sleep(1)

            if not file_path:
                print("❌ Aucun fichier CSV téléchargé")
            else:
                # --- Construire le nouveau nom ---
                new_name = f"alertes_{start_date}_{end_date}.csv"
                new_path = os.path.join(DOWNLOAD_DIR, new_name)

                os.rename(file_path, new_path)
                print(f"✅ Fichier téléchargé et renommé : {new_path}")

        
        
        
        except:
            driver.execute_script("arguments[0].click();", export_btn)
            print("✅ Bouton 'Exporter' cliqué via JS fallback")
    except TimeoutException:
        print("❌ Bouton 'Exporter' non trouvé ou non cliquable")



except NoSuchElementException as e:
    print(f"❌ Élément non trouvé : {e}")
except TimeoutException as e:
    print(f"❌ Délai d'attente dépassé : {e}")
except Exception as e:
    print(f"❌ Erreur inattendue : {e}")
finally:
    print("Fermeture du navigateur...")
    driver.quit()
