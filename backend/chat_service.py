"""Bulletproof ChatService with smart model detection and fallbacks."""

from typing import List, Dict, Optional
import importlib
import json
import os
from datetime import datetime


class ChatService:
    def __init__(self, api_key: str = '', history_file: str = '../data/chat_history.json', openai_api_key: str = ''):
        self.history_file = history_file
        if not os.path.isabs(self.history_file):
            self.history_file = os.path.normpath(os.path.join(os.path.dirname(__file__), self.history_file))

        self.chat_history = self.load_history()

        self.provider = 'none'
        self.genai_module = None
        self.openai_module = None
        self.genai_api_key = None
        self.openai_api_key = None
        self.last_init_error: Optional[str] = None
        self.available_genai_models = []

        
        print(f"[ChatService] Initializing with GEMINI_API_KEY={bool(api_key)}, OPENAI_API_KEY={bool(openai_api_key)}")

       
        try:
            self.genai_module = importlib.import_module('google.generativeai')
            key = api_key or os.getenv('GEMINI_API_KEY', '')
            if key:
                if hasattr(self.genai_module, 'configure'):
                    self.genai_module.configure(api_key=key)
                self.genai_api_key = key
               
                self._discover_genai_models()
                if self.available_genai_models:
                    self.provider = 'genai'
                    print(f"[ChatService] GenAI initialized. Available models: {self.available_genai_models[:3]}")
                else:
                    print(f"[ChatService] GenAI configured but no models available")
            else:
                print("[ChatService] GenAI not configured (no API key)")
        except Exception as e:
            self.last_init_error = f"GenAI init: {str(e)}"
            print(f"[ChatService] {self.last_init_error}")

      
        if not self.available_genai_models:
            try:
                self.openai_module = importlib.import_module('openai')
                key = openai_api_key or os.getenv('OPENAI_API_KEY', '')
                if key:
                    self.openai_module.api_key = key
                    self.openai_api_key = key
                    self.provider = 'openai'
                    print(f"[ChatService] OpenAI initialized")
                else:
                    print("[ChatService] OpenAI not configured (no API key)")
            except Exception as e:
                print(f"[ChatService] OpenAI init failed: {str(e)}")

    def _discover_genai_models(self):
        """Discover which GenAI models are actually available."""
        if not self.genai_module:
            return

        try:
            if hasattr(self.genai_module, 'list_models'):
                for m in self.genai_module.list_models():
                    
                    name = m.name if hasattr(m, 'name') else str(m)
                    self.available_genai_models.append(name)
                print(f"[GenAI] Discovered {len(self.available_genai_models)} models")
        except Exception as e:
            print(f"[GenAI] Model discovery failed: {str(e)}")

    def send_message(self, user_message: str):
        if not user_message or not user_message.strip():
            return 'Error: empty message'

        cleaned_msg = user_message.lower().strip()
        
        # 1. Intercept WhatsApp automation phrases
        if any(trigger in cleaned_msg for trigger in ["send message", "phone call", "video call"]):
            from command import execute_command
            cmd_result = execute_command(user_message)
            if cmd_result:
                return cmd_result

        # 2. Intercept system "open" actions
        if cleaned_msg.startswith("open "):
            from features import open_command
            open_command(user_message)
            return {"action": "complete", "response": f"Command executed for: '{user_message}'"}
                
        # 3. ROUTE TO GEMINI (Since your terminal log shows GenAI is active!)
        if hasattr(self, 'provider') and self.provider == 'genai':
            try:
                # Use your existing internal call method for Gemini
                result = self._call_genai(user_message)
                if result:
                    self.save_to_history(user_message, result)
                    return result
            except Exception as e:
                print(f"[Gemini] send_message failed: {str(e)}")

        # 4. Fallback to OpenAI provider if configured
        if self.openai_module and self.openai_api_key:
            try:
                result = self._call_openai(user_message)
                if result:
                    self.save_to_history(user_message, result)
                    return result
            except Exception as e:
                print(f"[OpenAI] send_message failed: {str(e)}")

        # 5. Ultimate Fallback Error Display
        return (
            'All AI providers are unavailable.\n\n'
            'To fix:\n'
            '1. For Gemini: Set GEMINI_API_KEY in .env\n'
            '2. For OpenAI: Set OPENAI_API_KEY in .env\n'
            '3. Restart backend after updating .env'
        )

    def _call_genai(self, user_message: str) -> Optional[str]:
        """Call GenAI with discovered models."""
        if not self.genai_module or not self.available_genai_models:
            return None

       
        system_instruction = (
            "You are Jarvis, a helpful AI assistant. "
            "For responses longer than 2 sentences, use Markdown formatting with bold text, "
            "bullet points (- or *), numbered lists, and headers (# ## ###) to make content readable. "
            "Use ** for bold, - for bullets, and # for headers. Make responses concise and well-organized."
        )

        
        last_error = None
        for model_name in self.available_genai_models[:5]:  
            try:
                if hasattr(self.genai_module, 'GenerativeModel'):
                    
                    full_model_name = model_name if model_name.startswith('models/') else f'models/{model_name}'
                    model = self.genai_module.GenerativeModel(full_model_name, system_instruction=system_instruction)
                    response = model.generate_content(user_message)
                    if hasattr(response, 'text') and response.text:
                        print(f"[GenAI] Success with {full_model_name}")
                        return response.text
            except Exception as e:
                last_error = e
                print(f"[GenAI] {model_name} failed: {str(e)[:100]}")
                continue

        raise Exception(f"All GenAI models failed. Last: {last_error}")

    def _call_openai(self, user_message: str) -> Optional[str]:
        """Call OpenAI API."""
        if not self.openai_module or not self.openai_api_key:
            return None

        try:
          
            if hasattr(self.openai_module, 'ChatCompletion'):
                response = self.openai_module.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages=[{'role': 'user', 'content': user_message}],
                    temperature=0.7,
                    max_tokens=1024,
                )
                text = response.choices[0].message.content
                print(f"[OpenAI] Success")
                return text
        except Exception as e:
            print(f"[OpenAI] ChatCompletion failed: {str(e)[:50]}")

        return None

    def save_to_history(self, user_msg: str, ai_msg: str) -> None:
        entry = {
            'timestamp': datetime.now().isoformat(),
            'user': user_msg,
            'assistant': ai_msg,
        }
        self.chat_history.append(entry)
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.chat_history, f, indent=2, ensure_ascii=False)

    def load_history(self) -> List[Dict]:
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"[ChatService] load_history failed: {str(e)}")
            return []
        return []

    def get_history(self) -> List[Dict]:
        return self.chat_history

    def clear_history(self) -> None:
        self.chat_history = []
        try:
            if os.path.exists(self.history_file):
                os.remove(self.history_file)
        except Exception:
            pass

    def list_models(self) -> List[str]:
        """Return available models."""
        if self.available_genai_models:
            return self.available_genai_models
        if self.openai_module:
            return ['gpt-3.5-turbo', 'gpt-4']
        return []

    def status(self) -> Dict[str, str]:
        return {
            'provider': self.provider,
            'models_available': len(self.available_genai_models),
            'history_file': self.history_file,
            'last_init_error': self.last_init_error or '',
        }