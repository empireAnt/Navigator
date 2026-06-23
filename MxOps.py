from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import tkinter as tk
from tkinter import messagebox
import atexit
import sys
import TransactionalUserOps as Ops

MX_ADMIN = 'MxAdmin'
loginUrl = 'http://ff.ignite.local:9980/login.html'

options = Options()
defaultDriver = None
polling_started = False

def open_mxadmin_index(driver = defaultDriver):
    Ops.login(driver = driver, loginUrl = loginUrl, username = MX_ADMIN)
