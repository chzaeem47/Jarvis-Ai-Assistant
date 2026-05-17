window.onload = function () {

    // ── SiriWave ─────────────────────────────────────────────────────────────
    // Generates the primary responsive sound wave visualizes system interaction states
    const siriContainer = document.getElementById('siri-container');
    if (!siriContainer || typeof SiriWave === 'undefined') return;

    const wave = new SiriWave({
        container: siriContainer,
        width:     800,
        height:    160,
        style:     'ios9',
        amplitude: 1,
        speed:     0.2,
        autostart: true
    });

    // ── DOM refs ──────────────────────────────────────────────────────────────
    const speakerLabel   = document.getElementById('speaker-label');
    const displayText    = document.getElementById('display-text');
    const listeningLabel = document.getElementById('listening-label');
    const checkBtn       = document.getElementById('check-btn');

    // ── State ─────────────────────────────────────────────────────────────────
    let capturedTranscript = '';
    let appState           = 'idle'; // 'idle' | 'listening' | 'processing' | 'speaking'
    let mic                = null;
    let restartTimer       = null;

    // ═════════════════════════════════════════════════════════════════════════
    // Helpers
    // ═════════════════════════════════════════════════════════════════════════

    function setState(s) {
        appState = s;
        console.log('[siri_mode] State updated to:', s);
    }

    function setLabel(who) {
        speakerLabel.className = who;
        speakerLabel.textContent = who === 'you' ? 'YOU' : who === 'jarvis' ? 'JARVIS' : '';
    }

    function showText(text) {
        displayText.textContent = text;
    }

    function animateText(text) {
        displayText.textContent = text;
        try {
            if (typeof $ !== 'undefined' && $.fn.textillate) {
                $(displayText).textillate('stop');
                $(displayText).textillate({
                    in:   { effect: 'fadeInUp', delayScale: 0.8, delay: 15, sync: false },
                    loop: false
                });
            }
        } catch (e) { console.warn("Textillate error:", e); }
    }

    // ═════════════════════════════════════════════════════════════════════════
    // TTS — safe speak with voice pre-loading
    // ═════════════════════════════════════════════════════════════════════════

    function getVoice() {
        const voices = window.speechSynthesis ? window.speechSynthesis.getVoices() : [];
        return (
            voices.find(v => v.lang === 'en-US' && /David|Mark|George|Google UK Male|Microsoft/i.test(v.name)) ||
            voices.find(v => v.lang === 'en-US') ||
            voices[0] ||
            null
        );
    }

    function speak(text, onDone) {
        if (!window.speechSynthesis) { if (onDone) onDone(); return; }

        const plain = text
            .replace(/#{1,6}\s*/g, '')
            .replace(/\*\*(.+?)\*\*/g, '$1')
            .replace(/\*(.+?)\*/g, '$1')
            .replace(/[-*]\s/g, '')
            .replace(/\n+/g, '. ')
            .substring(0, 500);

        window.speechSynthesis.cancel();

        setTimeout(() => {
            const utter   = new SpeechSynthesisUtterance(plain);
            utter.lang    = 'en-US';
            utter.rate    = 0.85; 
            utter.pitch   = 1.0;
            utter.volume  = 1.0;

            const v = getVoice();
            if (v) utter.voice = v;

            let cbFired = false;
            const fireOnce = () => {
                if (cbFired) return;
                cbFired = true;
                wave.setAmplitude(0.4);
                if (onDone) onDone();
            };

            const safetyMs = Math.max(4000, plain.length * 80);
            const safetyTimer = setTimeout(fireOnce, safetyMs);

            utter.onstart = () => wave.setAmplitude(2.5);
            utter.onend   = () => { clearTimeout(safetyTimer); fireOnce(); };
            utter.onerror = () => { clearTimeout(safetyTimer); fireOnce(); };

            window.speechSynthesis.speak(utter);
        }, 120);
    }

    // ═════════════════════════════════════════════════════════════════════════
    // Backend fetch
    // ═════════════════════════════════════════════════════════════════════════

    function sendToBackend(message) {
        console.log('[Jarvis] Attempting API call...');
        setState('processing');
        setLabel('jarvis');
        showText('Thinking...');

        fetch('http://127.0.0.1:5000/api/chat', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(async res => {
            if (!res.ok) {
                const errorData = await res.json();
                throw new Error(errorData.error || `Server Error ${res.status}`);
            }
            return res.json();
        })
        .then(data => {
            console.log('[Jarvis] Response received', data);
            let reply = data.response;
            
            reply = reply
                .replace(/#{1,6}\s*/g, '')
                .replace(/\*{1,3}(.*?)\*{1,3}/g, '$1') 
                .replace(/[-*]\s/g, '')
                .trim();

            setState('speaking');

            const phrases = reply.split(/(?<=[.,?!:;])\s+|\n+/).filter(p => p.trim().length > 0);
            displayPhrasesSequentially(phrases);

            speak(reply, () => {
                if (checkBtn) checkBtn.style.display = 'block';
                
                // If backend requires a message body context parameter, force wake the microphone up!
                if (data.action === 'prompt_message_content') {
                    window.pendingWhatsApp = {
                        number: data.metadata?.number || '',
                        name: data.metadata?.name || ''
                    };
                    
                    console.log("[Jarvis System] Prompt complete. Activating voice capture tracking...");
                    
                    clearTimeout(restartTimer);
                    capturedTranscript = '';
                    
                    if (listeningLabel) {
                        listeningLabel.classList.remove('hidden');
                        listeningLabel.style.opacity = '1';
                    }
                    wave.setAmplitude(1.5);
                    
                    // Small delay to let speech execution drop audio focus cleanly before capture starts
                    setTimeout(() => {
                        killMic(); 
                        setState('listening');
                        startMic();
                    }, 400);
                } else if (appState === 'speaking') {
                    restartTimer = setTimeout(resetToListening, 600);
                }
            });
        })
        .catch(err => {
            console.error('[Jarvis] API Error:', err);
            setState('speaking');
            const errorMsg = "I am having trouble connecting to my servers.";
            showText(errorMsg);
            speak(errorMsg, () => {
                restartTimer = setTimeout(resetToListening, 3000);
            });
        });
    }

    // ═════════════════════════════════════════════════════════════════════════
    // Reset / Mic Management
    // ═════════════════════════════════════════════════════════════════════════

    function resetToListening() {
        clearTimeout(restartTimer);
        capturedTranscript = '';
        setState('idle');

        if (window.speechSynthesis) window.speechSynthesis.cancel();

        if (checkBtn) checkBtn.style.display = 'block'; 

        if (listeningLabel) {
            listeningLabel.classList.remove('hidden');
            listeningLabel.style.opacity = '1';
        }

        wave.setAmplitude(1.0);
        setTimeout(startMic, 400);
    }

    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;

    function killMic() {
        if (!mic) return;
        mic.onstart = null; mic.onresult = null; mic.onend = null; mic.onerror = null;
        try { mic.stop(); } catch (e) {}
        mic = null;
    }

    function startMic() {
        if (appState === 'processing' || appState === 'speaking') return;

        killMic();
        setState('listening');

        mic = new SR();
        mic.lang = 'en-US';
        mic.interimResults = true;
        mic.continuous = false;

        mic.onstart = () => {
            if (!window.pendingWhatsApp) {
                setLabel(''); 
                showText('Listening...'); 
            }
            wave.setAmplitude(1.5);
            if (listeningLabel) listeningLabel.classList.remove('hidden');
        };

        mic.onresult = (event) => {
            if (appState !== 'listening') return;

            let interim = '';
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    capturedTranscript = transcript.trim();
                    setState('processing'); 
                    killMic();
                    
                    setLabel('you');
                    showText(capturedTranscript);
                    
                    // Routing branch logic for automated sessions
                    if (window.pendingWhatsApp) {
                        const targetName = window.pendingWhatsApp.name;
                        const structuralPrompt = `send message to ${targetName} body ${capturedTranscript}`;
                        
                        window.pendingWhatsApp = null;
                        sendToBackend(structuralPrompt);
                    } else {
                        sendToBackend(capturedTranscript);
                    }
                    return; 
                } else {
                    interim += transcript;
                }
            }
            if (interim) {
                setLabel('you');
                showText(interim);
            }
        };

        mic.onend = () => {
            if (appState === 'listening') {
                restartTimer = setTimeout(startMic, 300);
            }
        };

        mic.onerror = (e) => {
            if (e.error === 'no-speech') {
                if (appState === 'listening') restartTimer = setTimeout(startMic, 500);
                return;
            }
            console.error("Mic error:", e.error);
            setState('idle');
        };

        try { mic.start(); } catch (e) { console.error("Start failed:", e); }
    }

    // ── Check Result button ──────────────────────────────────────────────────
    if (checkBtn) {
        checkBtn.addEventListener('click', () => {
            if (window.speechSynthesis) window.speechSynthesis.cancel();
            clearTimeout(restartTimer);
            killMic();
            window.location.href = 'index.html';
        });
    }

    if (window.speechSynthesis) {
        window.speechSynthesis.getVoices();
        window.speechSynthesis.onvoiceschanged = () => window.speechSynthesis.getVoices();
    }

    function displayPhrasesSequentially(phrases) {
        if (!phrases || phrases.length === 0) return;

        let currentPhraseIndex = 0;

        function showNextLine() {
            if (currentPhraseIndex >= phrases.length) return;

            const currentText = phrases[currentPhraseIndex];
            animateText(currentText);

            const wordCount = currentText.split(/\s+/).length;
            const displayDuration = Math.max(1800, (wordCount * 430) + 600);

            currentPhraseIndex++;

            setTimeout(() => {
                if (currentPhraseIndex < phrases.length) {
                    displayText.style.opacity = '0';
                    setTimeout(() => {
                        displayText.style.opacity = '1';
                        showNextLine();
                    }, 150);
                }
            }, displayDuration);
        }

        showNextLine();
    }

    startMic();
};