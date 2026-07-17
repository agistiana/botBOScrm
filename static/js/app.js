// static/js/app.js
document.addEventListener('DOMContentLoaded', function() {
    // Cek status bot secara periodik
    function checkStatus() {
        fetch('/api/status')
            .then(res => res.json())
            .then(data => {
                const statusBadge = document.getElementById('botStatus');
                if (data.status === 'running') {
                    statusBadge.textContent = 'Running';
                    statusBadge.className = 'badge bg-warning';
                    document.getElementById('startBotBtn').disabled = true;
                    document.getElementById('stopBotBtn').disabled = false;
                } else {
                    statusBadge.textContent = 'Idle';
                    statusBadge.className = 'badge bg-secondary';
                    document.getElementById('startBotBtn').disabled = false;
                    document.getElementById('stopBotBtn').disabled = true;
                }
            })
            .catch(() => {});
    }

    // Cek status setiap 3 detik
    setInterval(checkStatus, 3000);
    checkStatus();

    // Upload file handling sudah ada di index.html
    // Tapi kita bisa tambahkan kode untuk mengaktifkan tombol start setelah upload
    const savedFile = sessionStorage.getItem('uploadedFile');
    if (savedFile) {
        document.getElementById('uploadedFile').textContent = savedFile.split('/').pop();
        document.getElementById('startBotBtn').disabled = false;
    }
});