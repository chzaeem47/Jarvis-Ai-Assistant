# JARVIS: Memory-Enhanced Agentic AI Assistant 🤖🎙️

JARVIS is a multi-lingual, voice-activated AI personal assistant designed to seamlessly handle tasks, automate desktop interactions, and retain contextual memory across conversations. Built using an agentic architecture, it combines speech-to-text intelligence, localized data management, automation scripts, and a robust Flask backend with a responsive frontend UI.

## ✨ Features

* **🗣️ Multi-Lingual Speech Recognition:** Seamless voice-to-text and text-to-speech capabilities.
* **🧠 Agentic Memory Modules:** Context-aware interactions powered by an intelligent chat memory layer.
* **🗄️ Embedded Relational Storage:** Utilizes a lightweight SQLite database (`jarvis.db`) for ultra-fast local data management and transaction logging.
* **🖥️ Desktop Automation:** Integrated with `pyautogui` and pixel-finding scripts to automate system-level tasks.
* **🎨 Clean UI Front-End:** Includes an interactive chat interface with built-in voice activation panels (Siri mode).

---

## 🚀 Getting Started (Step-by-Step)

Follow these instructions to get a copy of JARVIS up and running on your local machine.

### 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:
* **Python 3.10+** (Download from [python.org](https://www.python.org/downloads/))
* **Git** (Download from [git-scm.com](https://git-scm.com/))
* A modern web browser (Chrome, Edge, Firefox)

---

### 1. Clone the Repository
Open your terminal or command prompt and run the following commands to clone the project and navigate into its directory:

git clone https://github.com/YOUR_USERNAME/jarvis-agentic-assistant.git
cd jarvis-agentic-assistant

---

### 2. Set Up a Virtual Environment (Recommended)
A virtual environment keeps the project dependencies isolated from your global system.

**On Windows:**
python -m venv venv
venv\Scripts\activate

**On macOS/Linux:**
python3 -m venv venv
source venv/bin/activate

---

### 3. Install Dependencies
Install all the required Python packages using `pip` directly from the root directory:

pip install -r requirements.txt

---

### 4. Configure Environment Variables
Look at the `.env.example` file provided in the root directory for reference. Create a new file named `.env` in the root directory, open it, and add your configuration credentials:

FLASK_ENV=development
GEMINI_API_KEY=your_api_key_here

---

### 5. Run the Backend Application
Navigate into the backend folder and start the Flask development server:

cd backend
python app.py

Your backend server will now be running locally at `http://127.0.0.1:5000/`.

---

### 6. Launch the Front-End User Interface
Keep the backend terminal running, open a new file explorer window, navigate to the root folder of your project, and open **`index.html`** in any web browser to start chatting with JARVIS!

---

## 📁 Project Structure
Here is a breakdown of how the project is organized:

```text
├── backend/               # Core Python Flask API & Logic
│   ├── __pycache__/
│   ├── app.py             # Main backend application entry point
│   ├── chat_service.py    # LLM & reasoning integration handlers
│   ├── config.py          # Configuration and environmental setups
│   ├── contacts.csv       # Saved target contacts for automations
│   ├── db.py              # Database configuration logic
│   ├── features.py        # System control and action definitions
│   ├── find_pixels.py     # Desktop pixel-detection automation scripts
│   └── jarvis.db          # Embedded local database
│
├── data/                  # Local system memory storage
│   ├── chat_history.json  # Saved conversations for session persistence
│   └── sample_apps.txt    # Application routing definitions
│
├── frontend/              # Web client interface files
│   ├── chat.js            # Chat feed engine and formatting
│   ├── sidebar.js         # UI navigation logic
│   └── siri_mode.js       # Voice activation visualization scripts
│
├── pictures/              # Graphic assets and design resources
│   ├── icon.png
│   └── logo-removebg-preview.png
│
├── .env                   # Private environment variables (Local only)
├── .env.example           # Shared placeholder example template for variables
├── .gitignore             # Files to exclude from Git version tracking
├── index.html             # Core user interface landing page
├── jarvis.db              # Main relational database tracking layer
├── package.json           # Node project descriptors
├── package-lock.json      
├── README.md              # Documentation (This file!)
├── requirements.txt       # Automatically generated Python dependencies 
├── script.js              # Base root scripts
├── siri.html              # Dedicated voice-mode interface
└── style.js               # Global UI layout styles
```

---

🤝 Contributing
Contributions make the open-source community an amazing place to learn, inspire, and create.

• Fork the Project

• Create your Feature Branch: git checkout -b feature/AmazingFeature

• Commit your Changes: git commit -m 'Add some AmazingFeature'

• Push to the Branch: git push origin feature/AmazingFeature

• Open a Pull Request

---

📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The MIT License is a short and simple permissive license with conditions only requiring preservation of copyright and license notices. Licensed works, modifications, and larger works may be distributed under any different terms and without source code.
