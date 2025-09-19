# select_date()
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

# click_menu_item()
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

def select_date(driver, dt: datetime, toggle_selector="mat-datepicker-toggle[matSuffix] button", timeout=15):
    """
    Sélectionne la date `dt` (datetime) dans le mat-datepicker Angular Material :
    - clic sur le toggle du datepicker
    - clic sur le bouton période (mois/année)
    - sélection de l'année
    - sélection du mois
    - sélection du jour
    """

    year_txt = str(dt.year)                     # ex: "2025"
    month_abbr = dt.strftime("%b").upper()      # ex: "SEP"
    day_txt = str(dt.day)                       # ex: "18"

    def latest_overlay():
        """Retourne le dernier overlay actif (popup calendrier)."""
        overlays = driver.find_elements(By.CSS_SELECTOR, "div.cdk-overlay-pane")
        return overlays[-1] if overlays else None

    # --- 1) ouvrir le datepicker
    toggle = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, toggle_selector))
    )

    driver.execute_script("arguments[0].click();", toggle)
    print("✅ Datepicker ouvert")
    time.sleep(0.3)

    overlay = WebDriverWait(driver, timeout).until(lambda d: latest_overlay())

    # --- 2) bouton période (mois/année)
    period_btn = WebDriverWait(overlay, timeout).until(
        lambda ov: ov.find_element(By.CSS_SELECTOR, "button.mat-calendar-period-button")
    )
    driver.execute_script("arguments[0].click();", period_btn)
    print("✅ Sélecteur mois/année ouvert")
    time.sleep(0.3)

    # --- 3) choisir l'année
    year_btn = WebDriverWait(overlay, timeout).until(
        lambda ov: ov.find_element(By.XPATH, f".//button[@aria-label='{year_txt}']")
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", year_btn)
    driver.execute_script("arguments[0].click();", year_btn)
    print(f"✅ Année {year_txt} sélectionnée")
    time.sleep(0.3)

    # --- 4) choisir le mois
    month_btn = WebDriverWait(overlay, timeout).until(
        lambda ov: ov.find_element(By.XPATH, f".//span[normalize-space(text())='{month_abbr}']")
    )
    driver.execute_script("arguments[0].click();", month_btn)
    print(f"✅ Mois {month_abbr} sélectionné")
    time.sleep(0.3)

    # --- 5) choisir le jour
    day_btn = WebDriverWait(overlay, timeout).until(
        lambda ov: ov.find_element(By.XPATH, f".//span[normalize-space(text())='{day_txt}']")
    )
    driver.execute_script("arguments[0].click();", day_btn)
    print(f"✅ Jour {day_txt} sélectionné")
    time.sleep(0.3)


# ============== Débuggage =============
def click_menu_item(driver, text, timeout=20, screenshot_path='debug_alertes.png'):
    """
    Tente de cliquer sur un item de menu contenant `text` en multipliant les approches.
    Sauvegarde un screenshot et l'outerHTML des éléments candidats si échec.
    """
    xpaths = [
        f"//span[normalize-space()='{text}']",
        f"//span[contains(normalize-space(.),'{text}')]",
        f"//*[normalize-space(text())='{text}']",
        f"//*[contains(normalize-space(.),'{text}')]"
    ]

    # Récupérer candidats (présence)
    candidates = []
    for xp in xpaths:
        try:
            elems = WebDriverWait(driver, timeout).until(
                EC.presence_of_all_elements_located((By.XPATH, xp))
            )
            if elems:
                candidates.extend(elems)
        except TimeoutException:
            pass

    if not candidates:
        print(f"❌ Aucun élément trouvé pour le texte '{text}' (xpaths testés). Je sauvegarde un screenshot.")
        driver.save_screenshot(screenshot_path)
        raise TimeoutException(f"Aucun élément trouvé pour '{text}'")

    print(f"Found {len(candidates)} candidate(s) — je vais tenter plusieurs méthodes de clic...")

    for idx, el in enumerate(candidates, start=1):
        try:
            outer = driver.execute_script("return arguments[0].outerHTML;", el)
            print(f"\n--- Candidate #{idx} ---\n{outer[:1000]}\n--- end outerHTML ---")
        except Exception:
            print(f"Candidate #{idx}: impossible d'obtenir outerHTML")

        # Assurer que l'élément est visible
        try:
            if not el.is_displayed():
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                time.sleep(0.3)
        except Exception:
            pass

        # 1) click() direct
        try:
            el.click()
            print("✅ click() direct réussi")
            return True
        except Exception as e:
            print("click() direct échoué :", repr(e))

        # 2) ActionChains move_to_element + click
        try:
            ActionChains(driver).move_to_element(el).click().perform()
            print("✅ ActionChains click réussi")
            return True
        except Exception as e:
            print("ActionChains échoué :", repr(e))

        # 3) JS click
        try:
            driver.execute_script("arguments[0].click();", el)
            print("✅ JS click réussi")
            return True
        except Exception as e:
            print("JS click échoué :", repr(e))

        # 4) clic par offset (au centre) + diagnostic overlay
        try:
            rect = driver.execute_script("return arguments[0].getBoundingClientRect();", el)
            cx = rect.get('left', 0) + rect.get('width', 0) / 2
            cy = rect.get('top', 0) + rect.get('height', 0) / 2
            try:
                top_html = driver.execute_script(
                    "let e = document.elementFromPoint(arguments[0], arguments[1]); return e ? e.outerHTML : null;",
                    cx, cy
                )
                print("Element au point central (peut être un overlay) :", (top_html or "")[:400])
            except Exception:
                pass

            ActionChains(driver).move_to_element_with_offset(el, rect.get('width', 1)/2 - 1, rect.get('height', 1)/2 - 1).click().perform()
            print("✅ move_to_element_with_offset click réussi")
            return True
        except Exception as e:
            print("move_to_element_with_offset échoué :", repr(e))

        # 5) tenter les ancêtres (monte jusqu'à 6 niveaux)
        try:
            ancestors = driver.execute_script("""
                let el = arguments[0];
                let res = [];
                let a = el.parentElement;
                while(a && res.length < 6){
                  res.push(a);
                  a = a.parentElement;
                }
                return res;
            """, el)
            for i, anc in enumerate(ancestors, start=1):
                try:
                    print(f"Essai clic sur ancêtre niveau {i}")
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", anc)
                except Exception:
                    pass
                try:
                    anc.click()
                    print(f"✅ click() sur ancêtre niveau {i} réussi")
                    return True
                except Exception:
                    try:
                        driver.execute_script("arguments[0].click();", anc)
                        print(f"✅ JS click sur ancêtre niveau {i} réussi")
                        return True
                    except Exception as e:
                        print(f"clic sur ancêtre niveau {i} échoué :", repr(e))
        except Exception as e:
            print("Erreur lors du parcours des ancêtres :", repr(e))

    # Si on arrive ici, aucun essai n'a marché
    print(f"❌ Impossible de cliquer sur '{text}' après plusieurs tentatives — je sauvegarde un screenshot : {screenshot_path}")
    driver.save_screenshot(screenshot_path)
    raise Exception(f"Impossible de cliquer sur '{text}'. Voir {screenshot_path} et les outerHTML imprimés pour debug.")

    driver.execute_script("arguments[0].click();", alertes_btn)
    print("Bouton 'Alertes internes' cliqué (JS fallback)")






