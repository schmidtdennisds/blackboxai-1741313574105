// Initialize WaveSurfer with default settings
function initializeWaveSurfer(container) {
    return WaveSurfer.create({
        container: container,
        waveColor: '#C7D2FE',
        progressColor: '#6366F1',
        cursorColor: '#4F46E5',
        barWidth: 2,
        barRadius: 3,
        cursorWidth: 1,
        height: 100,
        barGap: 2,
        responsive: true,
        normalize: true
    });
}

// Format time in minutes:seconds
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}

// Update volume icon based on current volume
function updateVolumeIcon(volume, volumeBtn) {
    const icon = volumeBtn.querySelector('i');
    icon.className = volume === 0 
        ? 'fas fa-volume-mute' 
        : volume < 0.5 
            ? 'fas fa-volume-down' 
            : 'fas fa-volume-up';
}

// Initialize all UI elements and event listeners
function initializeLectureView(wavesurfer, audioPath, transcriptPath) {
    const playPauseButton = document.getElementById('playPause');
    const playPauseIcon = playPauseButton.querySelector('i');
    const volumeBtn = document.getElementById('volume-btn');
    const volumeInput = document.getElementById('volume');
    const loadingStatus = document.getElementById('loading-status');
    const errorMessage = document.getElementById('error-message');
    const currentTimeDisplay = document.getElementById('current-time');
    const totalDurationDisplay = document.getElementById('total-duration');

    // Load audio file
    wavesurfer.load(audioPath);

    // Load transcript
    fetch(transcriptPath)
        .then(response => response.text())
        .then(text => {
            const transcriptContainer = document.getElementById('transcript');
            const lines = text.split('\n').filter(line => line.trim());
            
            lines.forEach((line, index) => {
                const [timestamp, ...textParts] = line.split(' ');
                const div = document.createElement('div');
                div.className = 'transcript-segment p-3 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors duration-150';
                div.innerHTML = `
                    <div class="flex items-start">
                        <span class="time-marker">${timestamp}</span>
                        <p class="ml-3 text-gray-900">${textParts.join(' ')}</p>
                    </div>
                `;
                div.addEventListener('click', () => {
                    const [minutes, seconds] = timestamp.split(':').map(Number);
                    wavesurfer.setTime(minutes * 60 + seconds);
                });
                transcriptContainer.appendChild(div);
            });
        })
        .catch(error => {
            console.error('Error loading transcript:', error);
            document.getElementById('transcript').innerHTML = 'Error loading transcript';
        });

    // Play/Pause functionality
    playPauseButton.addEventListener('click', () => {
        wavesurfer.playPause();
    });

    // Previous/Next 10 seconds
    document.getElementById('previous').addEventListener('click', () => {
        wavesurfer.skip(-10);
    });

    document.getElementById('next').addEventListener('click', () => {
        wavesurfer.skip(10);
    });

    // Volume control
    volumeInput.addEventListener('input', (e) => {
        const volume = e.target.value / 100;
        wavesurfer.setVolume(volume);
        updateVolumeIcon(volume, volumeBtn);
    });

    volumeBtn.addEventListener('click', () => {
        const currentVolume = wavesurfer.getVolume();
        if (currentVolume > 0) {
            wavesurfer.setVolume(0);
            volumeInput.value = 0;
        } else {
            wavesurfer.setVolume(1);
            volumeInput.value = 100;
        }
        updateVolumeIcon(wavesurfer.getVolume(), volumeBtn);
    });

    // WaveSurfer events
    wavesurfer.on('ready', () => {
        loadingStatus.innerHTML = '<i class="fas fa-check-circle text-green-500"></i> Audio loaded';
        totalDurationDisplay.textContent = formatTime(wavesurfer.getDuration());
        errorMessage.classList.add('hidden');
        
        // Check for timestamp in URL
        const urlParams = new URLSearchParams(window.location.search);
        const timestamp = urlParams.get('t');
        if (timestamp) {
            wavesurfer.setTime(parseInt(timestamp));
        }
    });

    wavesurfer.on('error', (err) => {
        console.error('WaveSurfer error:', err);
        loadingStatus.innerHTML = '<i class="fas fa-exclamation-circle text-red-500"></i> Error loading audio';
        errorMessage.classList.remove('hidden');
    });

    wavesurfer.on('play', () => {
        playPauseIcon.className = 'fas fa-pause';
    });

    wavesurfer.on('pause', () => {
        playPauseIcon.className = 'fas fa-play';
    });

    wavesurfer.on('audioprocess', () => {
        const currentTime = wavesurfer.getCurrentTime();
        currentTimeDisplay.textContent = formatTime(currentTime);
        
        // Update active transcript segment
        document.querySelectorAll('.transcript-segment').forEach(segment => {
            const timeMarker = segment.querySelector('.time-marker').textContent;
            const [minutes, seconds] = timeMarker.split(':').map(Number);
            const segmentTime = minutes * 60 + seconds;
            
            if (Math.abs(currentTime - segmentTime) < 1) {
                segment.classList.add('active');
                segment.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            } else {
                segment.classList.remove('active');
            }
        });
    });
}
