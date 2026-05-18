
var typed = new Typed('#typed', {
    strings: ['HEY HAVE A NICE DAY!', 'ASK ME ANYTHING ♥'],
    typeSpeed: 50,
    loop: true,
});

const hamburger = document.getElementById('hamburger');
const sidebar = document.getElementById('sidebar');
const closeBtn = document.getElementById('closeBtn');
const initButton = document.getElementById('initButton');
const historyItems = document.getElementById('historyItems');

hamburger.addEventListener('click', function() {
    hamburger.classList.toggle('active');
    sidebar.classList.toggle('active');
    addOverlay();
});

closeBtn.addEventListener('click', function() {
    hamburger.classList.remove('active');
    sidebar.classList.remove('active');
    removeOverlay();
});

function addOverlay() {
    if (!document.querySelector('.sidebar-overlay')) {
        const overlay = document.createElement('div');
        overlay.className = 'sidebar-overlay';
        document.body.appendChild(overlay);
    }
    const overlay = document.querySelector('.sidebar-overlay');
    overlay.classList.add('active');
    overlay.addEventListener('click', closeSidebar);
}

function removeOverlay() {
    const overlay = document.querySelector('.sidebar-overlay');
    if (overlay) {
        overlay.classList.remove('active');
    }
}

function closeSidebar() {
    hamburger.classList.remove('active');
    sidebar.classList.remove('active');
    removeOverlay();
}

function addChatHistoryItem(text) {
    if (historyItems.querySelector('.empty-history')) {
        historyItems.innerHTML = '';
    }
    const item = document.createElement('div');
    item.className = 'history-item';
    item.textContent = text;
    item.addEventListener('click', function() {
        console.log('Clicked history item: ' + text);
    });
    historyItems.appendChild(item);
}