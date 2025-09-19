def safe_find(driver, selectors, timeout=15):
    """
    Essaie plusieurs sélecteurs (CSS ou XPATH) jusqu'à trouver un élément cliquable.
    selectors = [("css", "input[...]"), ("xpath", "//input[...]"), ...]
    """
    for method, value in selectors:
        try:
            if method == "css":
                return WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, value))
                )
            elif method == "xpath":
                return WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, value))
                )
        except TimeoutException:
            continue
    raise TimeoutException(f"Aucun sélecteur valide trouvé parmi : {selectors}")
