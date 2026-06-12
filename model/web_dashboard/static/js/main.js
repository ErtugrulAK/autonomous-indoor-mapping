document.addEventListener('DOMContentLoaded', () => {
    // 1. Audio Visualization
    const canvas = document.getElementById('audio-canvas');
    const ctx = canvas.getContext('2d');
    let audioCtx;
    let analyzer;
    let dataArray;
    let bufferLength;

    async function setupAudio() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            analyzer = audioCtx.createAnalyser();
            const source = audioCtx.createMediaStreamSource(stream);
            source.connect(analyzer);
            analyzer.fftSize = 256;
            bufferLength = analyzer.frequencyBinCount;
            dataArray = new Uint8Array(bufferLength);
            draw();
        } catch (err) {
            console.error('Audio access denied:', err);
            // Simulate audio if mic access is denied
            simulateAudio();
        }
    }

    function draw() {
        requestAnimationFrame(draw);
        analyzer.getByteFrequencyData(dataArray);

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        const barWidth = (canvas.width / bufferLength) * 2.5;
        let x = 0;

        for (let i = 0; i < bufferLength; i++) {
            const barHeight = (dataArray[i] / 255) * canvas.height;
            
            // Gradient color
            const gradient = ctx.createLinearGradient(0, canvas.height, 0, 0);
            gradient.addColorStop(0, '#7000ff');
            gradient.addColorStop(1, '#00f2ff');
            
            ctx.fillStyle = gradient;
            ctx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);

            x += barWidth + 1;
        }
    }

    function simulateAudio() {
        requestAnimationFrame(simulateAudio);
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const barWidth = (canvas.width / 40);
        for(let i=0; i<40; i++) {
            const h = Math.random() * canvas.height * 0.5;
            ctx.fillStyle = 'rgba(0, 242, 255, 0.2)';
            ctx.fillRect(i * (barWidth+2), canvas.height - h, barWidth, h);
        }
    }

    setupAudio();

    // 2. Detection Logs & Alerts
    const logList = document.getElementById('log-list');
    const statusMsg = document.getElementById('status-message');
    let lastAlertTime = 0;
    
    function showStatusAlert(label) {
        let text = "";
        const lowerLabel = label.toLowerCase();
        
        if (lowerLabel.includes('door') || lowerLabel.includes('kapı')) text = "KAPI GÖRÜNDÜ";
        else if (lowerLabel.includes('window') || lowerLabel.includes('pencere')) text = "PENCERE GÖRÜNDÜ";
        else return; // Only show for these

        statusMsg.innerText = text;
        statusMsg.classList.add('active');
        
        clearTimeout(window.alertTimeout);
        window.alertTimeout = setTimeout(() => {
            statusMsg.classList.remove('active');
        }, 3000);
    }

    function addLog(label, confidence) {
        const item = document.createElement('li');
        item.className = 'log-item';
        const time = new Date().toLocaleTimeString();
        item.innerHTML = `
            <span class="log-time">${time}</span>
            <span class="log-label">${label}</span>
            <span class="log-conf">Detected (${Math.round(confidence * 100)}%)</span>
        `;
        logList.prepend(item);
        
        // Keep only last 20 logs
        if (logList.children.length > 20) {
            logList.removeChild(logList.lastChild);
        }
    }

    // 3. Polling for detections (mocking or real)
    // In a real app, we might use EventSource or Socket.io
    // For now, we'll poll an endpoint or just mock it if we're not running the full backend yet
    setInterval(async () => {
        try {
            const response = await fetch('/detections');
            const data = await response.json();
            if (data && data.length > 0) {
                data.forEach(d => {
                    addLog(d.label, d.confidence);
                    showStatusAlert(d.label);
                });
            }
        } catch (e) {
            // Mock detections for demo if server not responding
            if (Math.random() > 0.9) {
                // addLog('Door', 0.85);
            }
        }
    }, 1000);
});
