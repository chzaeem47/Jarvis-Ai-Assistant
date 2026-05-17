from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from chat_service import ChatService
import os
import subprocess
import sys
import json
import sqlite3
import webbrowser
import csv
import urllib.parse
import pyautogui
import time
import win32gui
import win32con

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}}) 

app.config.from_object(Config)



def open_command(query: str) -> str | None:
    """Queries jarvis.db to launch a local app or a website.
    
    Returns a string detailing the action if successful, or None if no match 
    is found in the database.
    """
    app_name = query.lower().strip()
    db_path = os.path.join(os.path.dirname(__file__), "jarvis.db")
    
    if not app_name or not os.path.exists(db_path):
        return None
        
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
    
        cursor.execute("SELECT path FROM sys_command WHERE name = ?", (app_name,))
        results = cursor.fetchall()
        
        if len(results) != 0:
            target_path = results[0][0]
            os.startfile(target_path)
            conn.close()
            return f"Opening local application {app_name}"
            
       
        cursor.execute("SELECT url FROM web_command WHERE name = ?", (app_name,))
        results = cursor.fetchall()
        
        if len(results) != 0:
            target_url = results[0][0]
            webbrowser.open(target_url)
            conn.close()
            return f"Opening website {app_name}"
            
        conn.close()
        return None 
        
    except Exception as e:
        print(f"[AUTOMATION ERROR] Failed to run database lookup: {e}")
        return None


def get_contact_phone(contact_name: str) -> str | None:
    """Helper to lookup a contact's phone number from contacts.csv.
    Forcefully strips hidden whitespace, carriage returns, and case mismatches.
    """
    csv_path = os.path.join(os.path.dirname(__file__), 'contacts.csv')
    if not os.path.exists(csv_path):
        print("[AUTOMATION ERROR] contacts.csv missing.")
        return None
        
    normalized_target = contact_name.lower().strip().replace('"', '').replace("'", "")
    print(f"[DEBUG LOG] JARVIS is looking for contact: '{normalized_target}'")
    
    with open(csv_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:

            name_field = row.get('name') or row.get('First Name')
            phone_field = row.get('phone') or row.get('Phone 1 - Value')
            
            if not name_field or not phone_field:
                continue
                
            
            clean_db_name = "".join(c for c in name_field if c.isalnum() or c.isspace()).lower().strip()
            clean_phone = phone_field.strip().replace('\r', '').replace('\n', '')
            
            print(f"[DEBUG LOG] Checking against CSV Row -> Name: '{clean_db_name}', Phone: '{clean_phone}'")
            
            if normalized_target == clean_db_name or normalized_target in clean_db_name or clean_db_name in normalized_target:
                print(f"[DEBUG LOG] SUCCESS! Match found. Returning: {clean_phone}")
                return clean_phone
                
    print("[DEBUG LOG] FAILED: No matching contact found in CSV.")
    return None

def force_focus_whatsapp():
    """Finds the WhatsApp window and forces it to the foreground to clear taskbar blinking."""
    def window_enum_callback(hwnd, wildcard):
        if wildcard.lower() in win32gui.GetWindowText(hwnd).lower():
            try:
                # If minimized, restore it
                if win32gui.IsIconic(hwnd):
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                # Force it to the foreground
                win32gui.SetForegroundWindow(hwnd)
            except Exception as e:
                print(f"[DEBUG LOG] Focus force warning: {e}")

    # Give Windows a split second to send the URI intent to WhatsApp
    time.sleep(1.0)
    win32gui.EnumWindows(window_enum_callback, "WhatsApp")

def force_focus_whatsapp():
    """Finds the WhatsApp window and forces it to the foreground to clear taskbar blinking."""
    def window_enum_callback(hwnd, wildcard):
        if wildcard.lower() in win32gui.GetWindowText(hwnd).lower():
            try:
                if win32gui.IsIconic(hwnd):
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(hwnd)
            except Exception as e:
                print(f"[DEBUG LOG] Focus force warning: {e}")

    # Give Windows a split second to send the URI intent to WhatsApp
    time.sleep(1.0)
    win32gui.EnumWindows(window_enum_callback, "WhatsApp")



# def whatsapp_automation(action_type: str, contact_name: str, message_body: str = "") -> str:
#     """Uses UI position tracking to find the WhatsApp chat and physically click the call buttons."""
#     phone = get_contact_phone(contact_name)
    
#     if not phone:
#         return f"Sorry, I couldn't find {contact_name} in your contacts list."
    
#     try:
#         print(f"[DEBUG LOG] Maximizing WhatsApp Window...")
#         os.startfile("whatsapp://")
#         time.sleep(1.2)  # Give the app window a second to open
        
#         # 1. Grab window handle and force focus
#         hwnd = win32gui.FindWindow(None, "WhatsApp")
#         if hwnd:
#             if win32gui.IsIconic(hwnd):
#                 win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
#             win32gui.SetForegroundWindow(hwnd)
            
#             # Get the exact window coordinates dynamically
#             rect = win32gui.GetWindowRect(hwnd)
#             x_start, y_start, x_end, y_end = rect
#             window_width = x_end - x_start
            
#             # 2. Focus the search bar using the one hotkey that STILL works
#             pyautogui.hotkey('ctrl', 'f')
#             time.sleep(0.3)
            
#             # Type contact details
#             pyautogui.press('backspace', presses=20)
#             pyautogui.write(phone, interval=0.04) 
#             time.sleep(1.2)  # Wait for row population
            
#             # Press enter to open the message view box
#             pyautogui.press('enter')
#             time.sleep(1.0)  # Wait for the chat toolbar to load
            
#             # 3. Calculate call icon coordinates relative to your window position
#             # On the Windows client, the calling utilities live in the top right corner.
#             if action_type == "call":
#                 # Audio call icon is slightly to the left of the video icon
#                 click_x = 1733
#                 click_y = 78
#                 print(f"[DEBUG LOG] Clicking Audio Call Icon at coordinate: ({click_x}, {click_y})")
#                 pyautogui.click(click_x, click_y)
#                 return f"Voice call initiated via screen interaction for {contact_name}."
                
#             elif action_type == "video call":
#                 # Video call icon is further to the right
#                 click_x = 1660
#                 click_y = 91
#                 print(f"[DEBUG LOG] Clicking Video Call Icon at coordinate: ({click_x}, {click_y})")
#                 pyautogui.click(click_x, click_y)
#                 return f"Video call initiated via screen interaction for {contact_name}."

#         else:
#             return "Could not locate open WhatsApp Desktop Window process."

#     except Exception as e:
#         print(f"[AUTOMATION ERROR] Coordinate click routine failed: {e}")
#         return f"Failed to execute click automation."
        
#     return "Unknown action type."
def whatsapp_automation(action_type: str, contact_name: str, message_body: str = "") -> str:
    """Uses UI position tracking to find the WhatsApp chat and physically interacts with the window."""
    phone = get_contact_phone(contact_name)
    
    if not phone:
        return f"Sorry, I couldn't find {contact_name} in your contacts list."
    
    try:
        print(f"[DEBUG LOG] Maximizing WhatsApp Window...")
        os.startfile("whatsapp://")
        time.sleep(1.2)  # Give the app window a second to open
        
        # 1. Grab window handle and force focus
        hwnd = win32gui.FindWindow(None, "WhatsApp")
        if hwnd:
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            
            # Get the exact window coordinates dynamically
            rect = win32gui.GetWindowRect(hwnd)
            x_start, y_start, x_end, y_end = rect
            window_width = x_end - x_start
            
            # 2. Focus the search bar using the hotkey
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(0.3)
            
            # Type contact details
            pyautogui.press('backspace', presses=20)
            pyautogui.write(phone, interval=0.04) 
            time.sleep(1.2)  # Wait for row population
            
            # Press enter to open the message view box
            pyautogui.press('enter')
            time.sleep(1.0)  # Wait for the chat toolbar and input field to load
            
            # 3. Handle Actions
            if action_type == "message":
                print(f"[DEBUG LOG] Typing message payload...")
                # Since 'enter' on the search result focuses the chat input field, 
                # we can directly write the message and send it.
                pyautogui.write(message_body, interval=0.04)
                time.sleep(0.5)
                pyautogui.press('enter')
                return f"Message sent to {contact_name}: '{message_body}'"
                
            elif action_type == "call":
                # Audio call icon is slightly to the left of the video icon
                click_x = 1733
                click_y = 78
                print(f"[DEBUG LOG] Clicking Audio Call Icon at coordinate: ({click_x}, {click_y})")
                pyautogui.click(click_x, click_y)
                return f"Voice call initiated via screen interaction for {contact_name}."
                
            elif action_type == "video call":
                # Video call icon is further to the right
                click_x = 1660
                click_y = 91
                print(f"[DEBUG LOG] Clicking Video Call Icon at coordinate: ({click_x}, {click_y})")
                pyautogui.click(click_x, click_y)
                return f"Video call initiated via screen interaction for {contact_name}."

        else:
            return "Could not locate open WhatsApp Desktop Window process."

    except Exception as e:
        print(f"[AUTOMATION ERROR] UI interaction routine failed: {e}")
        return f"Failed to execute click/type automation."
        
    return "Unknown action type."


def import_csv_contacts(path):
    print(f"[INFO] Importing contacts from {path}")

csv_path = os.path.join(os.path.dirname(__file__), 'contacts.csv')
if os.path.exists(csv_path):
    import_csv_contacts(csv_path)
else:
    print("[WARNING] contacts.csv not found — add it to backend/ folder")

chat_service: ChatService | None = None
chat_service_error: str | None = None


def get_chat_service() -> ChatService:
    """Create and cache the ChatService instance, returning it.

    If creation fails, set `chat_service_error` with a helpful message and
    re-raise the exception for callers to handle.
    """
    global chat_service, chat_service_error
    if chat_service is not None:
        return chat_service

    try:
        from dotenv import load_dotenv
        load_dotenv(override=True)
        
        gemini_key = os.getenv('GEMINI_API_KEY', '')
        openai_key = os.getenv('OPENAI_API_KEY', '')
        
        print(f"[app.py] Loading ChatService with GEMINI={bool(gemini_key)}, OPENAI={bool(openai_key)}")
        
        chat_service = ChatService(api_key=gemini_key, history_file=app.config['CHAT_HISTORY_FILE'], openai_api_key=openai_key)
        chat_service_error = None
        return chat_service
    except Exception as e:
        chat_service_error = str(e)
        raise

# Place this tracking variable right above your routes
PENDING_WHATSAPP_SESSION = {
    "is_waiting_for_body": False,
    "contact_name": None
}

@app.route('/api/chat', methods=['POST'])
def chat():
    global PENDING_WHATSAPP_SESSION
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required', 'status': 'error'}), 400
        
        user_message = data['message'].strip()
        user_message_lower = user_message.lower()
        
        # ============================================================
        # STEP 2: Catching the follow-up text spoken into the mic
        # ============================================================
        if PENDING_WHATSAPP_SESSION["is_waiting_for_body"]:
            contact_name = PENDING_WHATSAPP_SESSION["contact_name"]
            message_body = user_message  # The whole text from the mic is the message body
            
            # Clear state immediately so the next command handles fresh queries
            PENDING_WHATSAPP_SESSION["is_waiting_for_body"] = False
            PENDING_WHATSAPP_SESSION["contact_name"] = None
            
            # Call your automated typing routine
            automation_result = whatsapp_automation("message", contact_name, message_body)
            return jsonify({'action': 'automation', 'response': automation_result, 'status': 'success'}), 200

        # System application commands
        if user_message_lower.startswith("open "):
            cleaned_query = user_message_lower[5:].strip()
            automation_result = open_command(cleaned_query)
            if automation_result:
                return jsonify({'action': 'automation', 'response': automation_result, 'status': 'success'}), 200

        # ============================================================
        # STEP 1: Initializing the command (e.g., "Send message to Alisha")
        # ============================================================
        elif "send message to" in user_message_lower:
            parts = user_message.split("send message to", 1)
            target_data = parts[1].strip()
            
            # Check if the user already provided the whole message in one go
            if " saying " in target_data.lower():
                contact_part, message_part = target_data.split(" saying ", 1)
                automation_result = whatsapp_automation("message", contact_part.strip(), message_part.strip())
                return jsonify({'action': 'automation', 'response': automation_result, 'status': 'success'}), 200
                
            elif " that " in target_data.lower():
                contact_part, message_part = target_data.split(" that ", 1)
                automation_result = whatsapp_automation("message", contact_part.strip(), message_part.strip())
                return jsonify({'action': 'automation', 'response': automation_result, 'status': 'success'}), 200
                
            else:
                # No body provided! Save the state and prompt the user via response
                PENDING_WHATSAPP_SESSION["is_waiting_for_body"] = True
                PENDING_WHATSAPP_SESSION["contact_name"] = target_data
                
                return jsonify({
                    'action': 'chat', 
                    'response': f"What message would you like to send to {target_data}?", 
                    'status': 'success'
                }), 200

        # Call handlers
        elif "video call to" in user_message_lower:
            parts = user_message.split("video call to", 1)
            automation_result = whatsapp_automation("video call", parts[1].strip())
            return jsonify({'action': 'automation', 'response': automation_result, 'status': 'success'}), 200

        elif "call to" in user_message_lower:
            parts = user_message.split("call to", 1)
            automation_result = whatsapp_automation("call", parts[1].strip())
            return jsonify({'action': 'automation', 'response': automation_result, 'status': 'success'}), 200

        # Default fallback to standard model responses
        svc = get_chat_service()
        ai_response = svc.send_message(user_message)
        
        if isinstance(ai_response, dict):
            return jsonify({**ai_response, 'status': 'success'}), 200
            
        return jsonify({'action': 'chat', 'response': ai_response, 'status': 'success'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get all chat history"""
    try:
        try:
            svc = get_chat_service()
        except Exception:
            try:
                path = app.config.get('CHAT_HISTORY_FILE')
                if not os.path.isabs(path):
                    path = os.path.normpath(os.path.join(os.path.dirname(__file__), path))
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        history = json.load(f)
                else:
                    history = []
                return jsonify({'history': history, 'status': 'success'}), 200
            except Exception as e:
                return jsonify({'error': str(e), 'status': 'error'}), 500

        history = svc.get_history()
        return jsonify({
            'history': history,
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/history', methods=['DELETE'])
def clear_history():
    """Clear chat history"""
    try:
        try:
            svc = get_chat_service()
        except Exception:
            try:
                path = app.config.get('CHAT_HISTORY_FILE')
                if not os.path.isabs(path):
                    path = os.path.normpath(os.path.join(os.path.dirname(__file__), path))
                if os.path.exists(path):
                    os.remove(path)
                return jsonify({'message': 'Chat history cleared successfully', 'status': 'success'}), 200
            except Exception as e:
                return jsonify({'error': str(e), 'status': 'error'}), 500

        svc.clear_history()
        return jsonify({
            'message': 'Chat history cleared successfully',
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        svc = get_chat_service()
        provider = getattr(svc, 'provider', 'none')
        if provider and provider != 'none':
            return jsonify({'status': 'healthy', 'provider': provider, 'message': 'Jarvis backend is running'}), 200
        else:
            return jsonify({'status': 'degraded', 'provider': 'none', 'message': 'No AI provider configured', 'service_status': svc.status()}), 200
    except Exception:
        return jsonify({'status': 'degraded', 'message': 'Backend initialized but provider not configured', 'error': chat_service_error}), 200


@app.route('/api/debug', methods=['GET'])
def debug():
    """Return diagnostic information useful for debugging provider imports and keys."""
    info = {
        'python_version': sys.version,
        'gemini_env': app.config.get('GEMINI_API_KEY', '') != '',
        'openai_env': os.getenv('OPENAI_API_KEY', '') != '',
        'chat_history_file': app.config.get('CHAT_HISTORY_FILE'),
    }

    try:
        def show(pkg):
            try:
                out = subprocess.check_output([sys.executable, '-m', 'pip', 'show', pkg], stderr=subprocess.STDOUT, text=True)
                return out
            except Exception:
                return None

        info['pip_google_genai'] = bool(show('google-genai'))
        info['pip_google'] = bool(show('google'))
        info['pip_openai'] = bool(show('openai'))
    except Exception:
        pass
    
    try:
        svc = get_chat_service()
        info['provider'] = svc.provider
        info['service_status'] = svc.status()
        try:
            info['models'] = svc.list_models() if svc.provider != 'none' else []
        except Exception:
            info['models'] = []
    except Exception:
        info['provider'] = 'none'
        info['service_error'] = chat_service_error

    return jsonify(info), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found', 'status': 'error'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error', 'status': 'error'}), 500

if __name__ == '__main__':
    print("Starting Jarvis Backend...")
    print(f"Environment: {app.config.get('FLASK_ENV', 'development')}")
    app.run(debug=app.config.get('DEBUG', True), host='127.0.0.1', port=5000)