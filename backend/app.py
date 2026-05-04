from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from chat_service import ChatService
import os
import subprocess
import sys
import json

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

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

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle chat messages
    
    Expected JSON: {'message': 'user message'}
    Returns: {'response': 'ai response', 'status': 'success'}
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required', 'status': 'error'}), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty', 'status': 'error'}), 400
        
        
        try:
            svc = get_chat_service()
        except Exception:
            err = chat_service_error or 'Failed to initialize chat service'
            return jsonify({'error': err, 'status': 'error'}), 503

        if getattr(svc, 'provider', 'none') == 'none':
            return jsonify({'error': 'No AI provider configured. Check backend debug.', 'status': 'error'}), 503

        
        ai_response = svc.send_message(user_message)
        
        return jsonify({
            'response': ai_response,
            'status': 'success'
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """
    Get all chat history
    
    Returns: {'history': [...], 'status': 'success'}
    """
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
    """
    Clear chat history
    
    Returns: {'message': 'History cleared', 'status': 'success'}
    """
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
    print(f"Environment: {app.config['FLASK_ENV']}")
    app.run(debug=app.config['DEBUG'], host='127.0.0.1', port=5000)
