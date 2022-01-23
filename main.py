from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

def fill_temp():
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    #select browser
    driver.get("https://tts.sutd.edu.sg/tt_login.aspx?formmode=expire")

    #login
    username = driver.find_element_by_id("pgContent1_uiLoginid")
    username.send_keys(open(r"username.txt").read())
    pw = driver.find_element_by_id("pgContent1_uiPassword")
    pw.send_keys(open(r"pw.txt").read())
    pw.send_keys(Keys.RETURN)

    #get parent window handle
    parentGUID = driver.current_window_handle
    print(parentGUID)
    print()
    print()

    #setup clicks to fill form
    try:
        menu = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "mainsection")), "Timeout from waiting for main page"
        )

        declaration_pg = driver.find_element_by_link_text("Daily Declaration")
        declaration_pg.click()

        allGUID = driver.window_handles
        
        for GUID in allGUID:
            if GUID != parentGUID:
                driver.switch_to_window(GUID)

        waiting = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "form"))
        )
        declaration = driver.find_element_by_id("pgContent1_cbSetToNo")
        declaration.click()
        submit = driver.find_element_by_id("pgContent1_btnSave")
        submit.click()
        driver.switch_to_alert().accept()
        driver.close()
        #close 1st popup window
        driver.switch_to_window(parentGUID)

        temperature_pg = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Temperature Taking"))
        )
        temperature_pg.click()

        allGUID = driver.window_handles
        
        for GUID in allGUID:
            if GUID != parentGUID:
                driver.switch_to_window(GUID)
        
        temperature_page = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "pgContent1_uiTemperature"))
        )
        choose_temperature = driver.find_element_by_id("pgContent1_uiTemperature")
        choose_temperature.send_keys("less")
        choose_temperature.send_keys(Keys.RETURN)
        driver.find_element_by_id("pgContent1_btnSave").click()

    finally:
        driver.quit()

fill_temp()

while True:
    t = time.localtime()
    if t.tm_hour==8 and t.tm_min==0 and t.tm_sec==0:
        fill_temp()
    if t.tm_hour==16 and t.tm_min==0 and t.tm_sec==0:
        fill_temp()