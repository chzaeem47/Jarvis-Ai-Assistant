# Jarvis AI Assistant - Setup Guide

## Project Structure

```
JARVIS/
├── index.html                 # Main UI (frontend)
├── style.css                  # Styling
├── package.json              # Node dependencies
├── .env                       # Environment variables (create from .env.example)
├── .env.example              # Example env file
├── backend/                  # Python backend
│   ├── app.py               # Flask application
│   ├── config.py            # Configuration
│   ├── chat_service.py      # Gemini chat service
│   └── requirements.txt      # Python dependencies
|   |_features.py            #AUtomation 
|   |_db.py                  #sqlLite DB
├── frontend/                # Frontend JavaScript
│   └── chat.js             # Chat client
├── data/                    # Data storage
│   └── chat_history.json   # Chat history (auto-generated)
└── pictures/               # Images
```

## Setup Instructions

### Step 1: Get Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key

### Step 2: Setup Environment Variable

1. Make your own  .env:

2. Open .env and replace your_api_key_here with your actual API key:
  
   GEMINI_API_KEY=your_actual_api_key_here
   FLASK_ENV=development

### Step 3: Install Python Dependencies

1. Open terminal in the project root
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Mac/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

### Step 4: Start the Backend

In your terminal (with virtual environment activated):
```bash
python backend/app.py
```

You should see:
```
Starting Jarvis Backend...
Environment: development
 * Running on http://127.0.0.1:5000
```

### Step 5: Open Frontend

1. Open `index.html` in your browser
2. Click the hamburger menu (three lines) → Click "Initialize Jarvis"
3. Type your message and press Enter or click the voice icon

## Features

- **Chat with Gemini**: Send messages and get AI responses
- **Chat History**: All conversations are saved in `data/chat_history.json`
- **Beautiful UI**: Maintains your original design with animations
- **Initialize Jarvis**: Checks if backend is running

## API Endpoints

- `POST /api/chat` - Send a message and get response
- `GET /api/history` - Get all chat history
- `DELETE /api/history` - Clear chat history
- `GET /api/health` - Health check

## Troubleshooting

### "Could not initialize Jarvis" error
- Make sure backend is running on `http://127.0.0.1:5000`
- Check terminal for backend errors

### "GEMINI_API_KEY environment variable is not set"
- Make sure `.env` file exists in project root
- Verify your API key is correctly set

### ModuleNotFoundError
- Ensure virtual environment is activated
- Run `pip install -r backend/requirements.txt`

## Environment Variables

Create a `.env` file (copy from `.env.example`):

```
GEMINI_API_KEY=your_google_gemini_api_key
FLASK_ENV=development
```

**Never commit `.env` to version control!**

---

Enjoy chatting with Jarvis! 🚀
