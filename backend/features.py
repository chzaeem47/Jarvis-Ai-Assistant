import os
import sqlite3
import webbrowser
import time
import pyautogui
from credential_manager import get_credential


def open_command(query):

    app_name = query.lower().strip()
    
    if not app_name:
        return "Command text was empty."
        
    try:

        conn = sqlite3.connect("jarvis.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT path FROM sys_command WHERE name = ?", (app_name,))
        results = cursor.fetchall()
        
        if len(results) != 0:
            target_path = results[0][0]
            os.startfile(target_path)
            conn.close()
            return f"Opening local application: {app_name}"
            
        cursor.execute("SELECT url FROM web_command WHERE name = ?", (app_name,))
        results = cursor.fetchall()
        
        if len(results) != 0:
            target_url = results[0][0]
            webbrowser.open(target_url)
            conn.close()
            return f"Opening website: {app_name}"
            
        os.system(f"start {app_name}")
        conn.close()
        return f"Attempting default system launch for: {app_name}"
        
    except sqlite3.Error as e:
        return f"Database interface error: {str(e)}"
    except Exception as e:
        return f"Execution failed: {str(e)}"
    


def automated_portal_login(portal_name: str) -> str:
    """Fetches credentials, runs auto-fill inputs, handles reCAPTCHA check, and logs in."""
    creds = get_credential(portal_name)
    
    if not creds:
        return f"I couldn't find any stored credentials for '{portal_name}'."
        
    print(f"[Automation] Launching browser window for: {portal_name}...")
    webbrowser.open(creds["login_url"])
    
    # 1. Wait for page load and focus field
    time.sleep(4.5) 
    
    print("[Automation] Injecting text credentials...")
    # Keystroke mapping: Username -> Tab Focus -> Password
    pyautogui.write(creds["username"], interval=0.04)
    time.sleep(0.2)
    pyautogui.press('tab')
    time.sleep(0.2)
    pyautogui.write(creds["password"], interval=0.04)
    time.sleep(0.5)
    
    # ============================================================
    # SCREEN PATTERN: COORDINATE INTERACTION 
    # ============================================================
    # TODO: Replace these placeholder numbers with values from find_pixels.py
    
    captcha_x = 1202  
    captcha_y = 457  
    
    login_btn_x = 1430
    login_btn_y = 524
    
    print("[Automation] Ticking reCAPTCHA 'I am not a robot' box...")
    pyautogui.moveTo(captcha_x, captcha_y, duration=10)
    pyautogui.click()
    
    # CRITICAL: Wait for Google's captcha validator script to register the tick green color
    print("[Automation] Waiting for verification verification token processing...")
    time.sleep(2.5) 
    
    print("[Automation] Clicking login confirmation button...")
    pyautogui.moveTo(login_btn_x, login_btn_y, duration=0.2)
    pyautogui.click()
    
    return f"Automated portal submission script executed for {portal_name}."


