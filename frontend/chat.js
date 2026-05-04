let chatInstance = null;

class ChatClient {
    constructor(backendUrl = 'http://127.0.0.1:5000') {
        this.backendUrl = backendUrl;

        this.messageInput = document.querySelector('.input-container input');
        this.activityItems = document.getElementById('activityItems');
        this.sendBtn = document.getElementById('sendBtn');
        this.micBtn = document.getElementById('micBtn');
        this.initButton = document.getElementById('initButton');
        
        this.historyItems = document.getElementById('historyItems');
        this.sidebarDeleteBtn = document.getElementById('deleteBtn');
        this.activityDeleteBtn = document.querySelector('.activity-delete');

        this.isListening = false;
        this.recognition = null;
        this.siriWave = null;

        this.initializeEventListeners();
        this.initializeSiriWave();
    }

    initializeEventListeners() {
        if (this.messageInput) {
            this.messageInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault(); 
                    if (this.messageInput.value.trim()) this.sendMessage();
                }
            });
        }

        if (this.sendBtn) {
            this.sendBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.sendMessage();
            });
        }

        if (this.initButton) {
            this.initButton.addEventListener('click', () => this.initializeJarvis());
        }

        if (this.activityDeleteBtn) {
            this.activityDeleteBtn.addEventListener('click', () => this.clearActivityLog());
        }

        if (this.sidebarDeleteBtn) {
            this.sidebarDeleteBtn.addEventListener('click', () => this.clearSidebarHistory());
        }
    }

    updateSidebarHistory(text) {
        if (!this.historyItems) return;
        const empty = this.historyItems.querySelector('.empty-history');
        if (empty) empty.remove();

        const item = document.createElement('div');
        item.className = 'history-item';
        item.textContent = text.length > 25 ? text.substring(0, 25) + '...' : text;
        this.historyItems.prepend(item);
    }

    clearActivityLog() {
        if (this.activityItems) {
            this.activityItems.innerHTML = '<p class="empty-activity">Waiting for Messages</p>';
        }
    }

    clearSidebarHistory() {
        if (confirm("Clear all chat history?")) {
            if (this.historyItems) {
                this.historyItems.innerHTML = '<p class="empty-history">No chat history yet</p>';
            }
            
        }
    }


    initializeSiriWave() {

        const siriContainer = document.getElementById('siri-container');

        if (!siriContainer) return;



        this.siriWave = new SiriWave({

            container: siriContainer,

            width: 600,

            height: 120,

            style: 'ios9',

            amplitude: 1,

            speed: 0.2,

            autostart: false

        });



        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (SpeechRecognition) {

            this.recognition = new SpeechRecognition();

            this.recognition.lang = 'en-US';

            this.recognition.interimResults = false;



            this.recognition.onresult = (event) => {

                const transcript = event.results[0][0].transcript.trim();

                if (transcript) this.sendMessage(transcript);

            };


            this.recognition.onend = () => this.stopListening();

            this.recognition.onerror = () => this.stopListening();


            this.micBtn?.addEventListener('click', () => {

                this.isListening ? this.stopListening() : this.startListening();

            });

        }

    }


    startListening() {

        if (!this.recognition) return;

        this.recognition.start();

        this.isListening = true;

        document.getElementById('siri-container').style.display = 'flex';

        this.siriWave?.start();

        this.micBtn?.classList.add('mic-active');

        document.getElementById('typed').style.display = 'none';

    }

    stopListening() {

        this.recognition?.stop();

        this.isListening = false;

        document.getElementById('siri-container').style.display = 'none';

        this.siriWave?.stop();

        this.micBtn?.classList.remove('mic-active');

        document.getElementById('typed').style.display = 'block';

    }

    addMessageToUI(text, type) {
        if (!this.activityItems) return;

        const empty = this.activityItems.querySelector('.empty-activity');
        if (empty) empty.remove();

        const messageDiv = document.createElement('div');
        messageDiv.className = `activity-item ${type}`;

        const box = document.createElement('div');
        box.className = 'activity-item-box';

        const label = document.createElement('div');
        label.className = 'activity-item-label';
        label.textContent = type === 'user' ? 'You' : 'Jarvis';

        const content = document.createElement('div');
        content.className = 'activity-item-content';

        if (type === 'assistant' && typeof marked !== 'undefined') {
            content.innerHTML = marked.parse(text);
        } else {
            content.textContent = text;
        }

        box.append(label, content);

        const actionGroup = document.createElement('div');
        actionGroup.className = 'action-group';
        const copyBtn = document.createElement('button');
        copyBtn.className = 'action-btn';
        copyBtn.innerHTML = `<box-icon name="copy-alt" color="#ffff" size="xs"></box-icon>`;
        copyBtn.onclick = () => {
            navigator.clipboard.writeText(text);
            const orig = copyBtn.innerHTML;
            copyBtn.innerHTML = `<box-icon name="circle" color="#09ff00" size="xs"></box-icon>`;
            setTimeout(() => copyBtn.innerHTML = orig, 2000);
        };
        actionGroup.appendChild(copyBtn);

        if (type === 'user') {
            messageDiv.appendChild(box);
            messageDiv.appendChild(actionGroup);
            this.updateSidebarHistory(text); 
        } else {
            messageDiv.appendChild(actionGroup);
            messageDiv.appendChild(box);
        }

        const wrapper = document.createElement('div');
        wrapper.className = 'slide-wrapper';
        wrapper.appendChild(messageDiv);

        this.activityItems.appendChild(wrapper);

        requestAnimationFrame(() => {
            wrapper.style.opacity = '1';
            wrapper.style.visibility = 'visible';
        });

        setTimeout(() => {
            this.activityItems.scrollTop = this.activityItems.scrollHeight;
        }, 100);
    }



    async sendMessage(voiceText = null) {

        const message = (voiceText || this.messageInput?.value || '').trim();

        if (!message) return;

        this.addMessageToUI(message, 'user');        

        if (this.messageInput) this.messageInput.value = '';

        const loadingId = this.addLoadingSpinner();

        try {

            const res = await fetch(`${this.backendUrl}/api/chat`, {

                method: 'POST',

                headers: { 'Content-Type': 'application/json' },

                body: JSON.stringify({ message })

            });

            const data = await res.json();

            this.removeLoadingSpinner(loadingId);

            if (data.status === 'success' && data.response) {

                this.addMessageToUI(data.response, 'assistant');

            } else {

                this.addMessageToUI("Sorry, I couldn't process that.", 'assistant');

            }

        } catch (err) {

            this.removeLoadingSpinner(loadingId);

            this.addMessageToUI(`Connection Error: ${err.message}`, 'assistant');

        }

    }

    addLoadingSpinner() {

        const id = 'loading-' + Date.now();

        const div = document.createElement('div');

        div.className = 'slide-wrapper';

        div.id = `wrapper-${id}`;

        div.innerHTML = `

            <div class="activity-item assistant">

                <div class="activity-item-box loading">

                    <div class="spinner"></div>

                    <span>Jarvis is thinking...</span>

                </div>

            </div>`;

        this.activityItems.appendChild(div);

        this.activityItems.scrollTop = this.activityItems.scrollHeight;

        return id;

    }



    removeLoadingSpinner(id) {

        const el = document.getElementById(`wrapper-${id}`);

        if (el) el.remove();

    }

    async initializeJarvis() {

        console.log("Jarvis Initialized");

        this.addMessageToUI("Jarvis Initialized Developed By Zaeem With ♥︎", 'assistant');

    }

}

document.addEventListener('DOMContentLoaded', () => {

    chatInstance = new ChatClient();

});