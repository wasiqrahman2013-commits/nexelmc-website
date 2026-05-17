function copyIP() {
    navigator.clipboard.writeText("nexelmc.falixsrv.me:25565");
    alert("✓ Server IP copied!");
}

async function checkStatus() {
    try {
        const res = await fetch('/api/status');
        const data = await res.json();
        const count = document.getElementById('playerCount');
        if (count) count.textContent = data.players || 0;
    } catch(e) { console.log('Status check failed'); }
}

document.addEventListener('DOMContentLoaded', function() {
    const toggle = document.querySelector('.nav-toggle');
    const links = document.querySelector('.nav-links');
    if (toggle && links) {
        toggle.onclick = () => {
            if (links.style.display === 'flex') {
                links.style.display = 'none';
            } else {
                links.style.display = 'flex';
                links.style.flexDirection = 'column';
                links.style.position = 'absolute';
                links.style.top = '60px';
                links.style.left = '0';
                links.style.right = '0';
                links.style.background = '#0a0a0a';
                links.style.padding = '1rem';
            }
        };
    }
    checkStatus();
    setInterval(checkStatus, 30000);
});
