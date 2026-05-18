# JARVIS: Memory-Enhanced Agentic AI Assistant🤖

JARVIS is a multi-lingual, voice-activated AI personal assistant designed to seamlessly handle tasks, automate desktop interactions, and retain contextual memory across conversations. Built using an agentic architecture, it combines speech-to-text intelligence, localized data management, automation scripts, and a robust Flask backend with a responsive frontend UI.

---

## ✨ Features

* **🗣️ Multi-Lingual Speech Recognition:** Seamless voice-to-text and text-to-speech capabilities.
* **🧠 Agentic Memory Modules:** Context-aware interactions powered by an intelligent chat memory layer.
* **🗄️ Embedded Relational Storage:** Utilizes a lightweight SQLite database (`jarvis.db`) for ultra-fast local data management, system path mapping, and transaction logging.
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

```bash
git clone https://github.com/YOUR_USERNAME/jarvis-agentic-assistant.git
cd jarvis-agentic-assistant
2. Set Up a Virtual Environment (Recommended)
A virtual environment keeps the project dependencies isolated from your global system.

On Windows:

DOS
python -m venv venv
venv\Scripts\activate
On macOS/Linux:

Bash
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Install all the required Python packages using pip directly from the root directory:

Bash
pip install -r requirements.txt
```
---

### 2. Configure Environment Variables
Look at the .env.example file provided in the root directory for reference. Create a new file named .env in the root directory, open it, and add your configuration credentials:

FLASK_ENV=development

GEMINI_API_KEY=your_gemini_api_key_here

---

### 3. Setup Local Data Files
To ensure security and personalization, certain local configuration files must be prepared manually:

Export Google Contacts: Export your contacts from Google Contacts as a .csv file. Rename this file to contacts.csv and place it inside the backend/ folder.

Credential Manager Key: Ensure your local password manager environment initializes its secure key (secret.key) locally inside the backend/ folder.

### 4. Initialize the Local SQLite Database
JARVIS relies on a local relational SQLite database to reference custom system shortcuts and app mappings. Before running the application for the first time, initialize the database file:

Open backend/db.py.

Uncomment the initialization section and insert your preferred target URLs, custom application names, or executable local system file paths.

Run the database setup script:
```
Bash
cd backend
python db.py
cd ..
```
This will successfully compile and establish the local jarvis.db data tracking file.

### 5. Run the Backend Application
Navigate into the backend folder and start your Flask automation and reasoning server:

```
Bash
python backend/app.py
```
Your backend server will now be running locally at [http://127.0.0.1:5000/](http://127.0.0.1:5000/). Keep this terminal window open!

### 6. Launch the Front-End User Interface
With the backend server running, open a separate terminal or use your system file explorer, navigate to the root folder of the project, and open index.html in any modern web browser to start chatting and utilizing JARVIS!

📁 Project Structure
Here is a breakdown of how the project is organized:
```
Plaintext
├── backend/               # Core Python Flask API & Logic
│   ├── app.py             # Main backend application entry point
│   ├── chat_service.py    # LLM reasoning & agentic fallback handlers
│   ├── config.py          # Configuration and environmental setups
│   ├── contacts.csv       # Private target contact records for automated actions (Local only)
│   ├── db.py              # Relational database generation logic & schema rules
│   ├── features.py        # System controls, hotkeys, and action definitions
│   ├── find_pixels.py     # Desktop UI coordinate mapping & pixel-detection tools
│   ├── secret.key         # Local Fernet credential encryption key (Local only)
│   └── jarvis.db          # Main local SQLite database file (Local only)
│
├── data/                  # Local system memory storage
│   ├── chat_history.json  # Local session tracking for conversational persistence
│   └── sample_apps.txt    # Fallback application routing definitions
│
├── frontend/              # Client-side asset components
│   ├── chat.js            # Chat feed layout, event rendering & message formatting
│   ├── sidebar.js         # Navigation layouts and quick-panel UI control
│   └── siri_mode.js       # Voice capturing interface and waveform visualizations
│
├── pictures/              # Graphic assets and design resources
│   ├── icon.png
│   └── logo-removebg-preview.png
│
├── .env                   # Private API tokens & development configurations (Local only)
├── .env.example           # Non-sensitive variable templates for community use
├── .gitignore             # Formatted tracking rules to secure private environments
├── index.html             # Core application web interface dashboard
├── requirements.txt       # Automatically managed project software packages
├── siri.html              # Dedicated viewport for standalone voice automation
└── style.js               # Global UI visual design configurations
```
---

### 7. Contributing
Contributions make the open-source community an amazing place to learn, inspire, and create.

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

### 8. License
This project is licensed under the MIT License - see the LICENSE file for details.