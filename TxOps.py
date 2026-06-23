openRiskFromRegionAppUrl = 'http://ff.ignite.local:9980/link/openRiskfromRegionApp/'
loginUrl = 'http://ff.ignite.local:9980/login.html'
TEST_USER = 'Genny.Dradi@Chubb.com'

#PER VENV .\venv\Scripts\activate

#from sys import setrecursionlimit
#setrecursionlimit(10) #per sicurezza, in caso il login fallisca

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tkinter import messagebox
from time import sleep
import atexit
import Queries

options = Options()
defaultDriver = None
polling_started = False

def quit_driver():
    global defaultDriver, polling_started
    try:
        if defaultDriver:
            defaultDriver.quit()
    except Exception:
        pass
    finally:
        defaultDriver = None
        polling_started = False

atexit.register(quit_driver)

def login(driver = defaultDriver, loginUrl = None, username = TEST_USER):
    if(loginUrl is not None):
        driver.get(loginUrl)
    login_button = driver.find_element(By.ID, "loginButton")
    user_textBox = driver.find_element(By.ID, "usernameInput")
    psw_textBox = driver.find_element(By.ID, "passwordInput")
    user_textBox.send_keys(username)
    psw_textBox.send_keys(1)
    login_button.click()

def openRiskFromRegionApp(driver = defaultDriver, uniqueid = None):
    driver.get(openRiskFromRegionAppUrl + uniqueid)
    if (isDriverLoggedIn(driver) == False):
        login(driver)

def isDriverLoggedIn(driver = defaultDriver):
    return True if (not driver.find_elements(By.ID, "loginButton")) else False

def open_with_number(input_number, root=None):
    if not input_number or not str(input_number).strip():
        raise ValueError('a number is required')
    input_number = str(input_number).strip()
    open_with_uniqueid(Queries.get_uniqueid(input_number), root)    

def open_with_uniqueid(uniqueid, root=None):
    #It's assumed that a Webdriver is already running (should've been initialized already)
    if not uniqueid or not str(uniqueid).strip():
        raise ValueError('uniqueid is required')
    uniqueid = str(uniqueid).strip()

    openRiskFromRegionApp(defaultDriver, uniqueid)


def start_driver_polling(root):
    """Poll the webdriver to detect if the browser was closed manually and quit the driver only (keep GUI alive)."""
    global polling_started, defaultDriver
    if polling_started:
        return
    polling_started = True
    def _poll():
        global defaultDriver
        try:
            # access a property to check session validity
            if not defaultDriver:
                raise Exception("no driver")
            _ = defaultDriver.current_window_handle
        except Exception:
            # se browser chiuso o non trovo driver attivi, faccio driver.quit per evitar di lasciare aperte sessioni
            try:
                quit_driver()
            except Exception:
                pass
            try:
                messagebox.showinfo("Browser closed", "The WebDriver stopped because its browser windows was closed; use Open to start a new session.")
            except Exception:
                pass
            return
        # schedule next check
        try:
            root.after(1000, _poll)
        except Exception:
            pass
    root.after(1000, _poll)

def init(db_name, root=None):
    Queries.set_DB(db_name)
    global defaultDriver
    if defaultDriver is None:
        defaultDriver = webdriver.Chrome(options=options)
    #start Driver polling
    if root is not None:
        start_driver_polling(root)
      

# Note: GUI code (windows, widgets) was moved to GUI.py to keep this module GUI-agnostic.




