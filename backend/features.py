import os
import sqlite3
import webbrowser

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