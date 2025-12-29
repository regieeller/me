// Memory Catcher App - V2
// Full-featured PWA for capturing and recalling memories

class MemoryCatcher {
    constructor() {
        this.memories = [];
        this.currentView = 'timeline';
        this.currentFilter = 'all';
        this.searchQuery = '';
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.recordingStartTime = null;
        this.recordingInterval = null;
        this.currentMemoryId = null;
        this.currentPhoto = null;
        this.currentAudio = null;

        this.init();
    }

    init() {
        this.loadMemories();
        this.setupEventListeners();
        this.registerServiceWorker();
        this.renderMemories();
        this.checkInstallPrompt();
    }

    // Storage Management
    loadMemories() {
        const stored = localStorage.getItem('memories');
        this.memories = stored ? JSON.parse(stored) : [];
    }

    saveMemories() {
        localStorage.setItem('memories', JSON.stringify(this.memories));
    }

    // Event Listeners
    setupEventListeners() {
        // Menu
        document.getElementById('menuBtn').addEventListener('click', () => this.showMenu());
        document.getElementById('closeMenuBtn').addEventListener('click', () => this.hideMenu());
        document.getElementById('menuOverlay').addEventListener('click', (e) => {
            if (e.target.id === 'menuOverlay') this.hideMenu();
        });

        // Menu Items
        document.getElementById('exportBtn').addEventListener('click', () => this.exportMemories());
        document.getElementById('randomMemoryBtn').addEventListener('click', () => this.showRandomMemory());
        document.getElementById('statsBtn').addEventListener('click', () => this.showStats());
        document.getElementById('aboutBtn').addEventListener('click', () => this.showAbout());

        // Search
        document.getElementById('searchInput').addEventListener('input', (e) => this.handleSearch(e.target.value));
        document.getElementById('clearSearch').addEventListener('click', () => this.clearSearch());

        // Filters
        document.querySelectorAll('.filter-tab').forEach(tab => {
            tab.addEventListener('click', (e) => this.setFilter(e.target.dataset.filter));
        });

        // FAB
        document.getElementById('fabBtn').addEventListener('click', () => this.toggleCapture());

        // Capture
        document.getElementById('cancelCapture').addEventListener('click', () => this.cancelCapture());
        document.getElementById('saveMemory').addEventListener('click', () => this.saveMemory());
        document.getElementById('photoInput').addEventListener('change', (e) => this.handlePhoto(e));
        document.getElementById('voiceBtn').addEventListener('click', () => this.startVoiceRecording());
        document.getElementById('stopRecording')?.addEventListener('click', () => this.stopVoiceRecording());

        // Detail
        document.getElementById('closeDetail').addEventListener('click', () => this.closeDetail());
        document.getElementById('deleteMemory').addEventListener('click', () => this.deleteCurrentMemory());
    }

    // View Management
    showView(viewName) {
        document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
        document.getElementById(`${viewName}View`).classList.add('active');
        this.currentView = viewName;

        // Update FAB
        const fab = document.getElementById('fabIcon');
        if (viewName === 'capture') {
            fab.textContent = '×';
        } else {
            fab.textContent = '+';
        }
    }

    showMenu() {
        document.getElementById('menuOverlay').classList.remove('hidden');
    }

    hideMenu() {
        document.getElementById('menuOverlay').classList.add('hidden');
    }

    // Capture Management
    toggleCapture() {
        if (this.currentView === 'capture') {
            this.cancelCapture();
        } else {
            this.showView('capture');
            document.getElementById('memoryText').focus();
        }
    }

    cancelCapture() {
        document.getElementById('memoryText').value = '';
        document.getElementById('mediaPreview').classList.add('hidden');
        document.getElementById('mediaPreview').innerHTML = '';
        document.getElementById('tagsPreview').classList.add('hidden');
        this.currentPhoto = null;
        this.currentAudio = null;
        this.showView('timeline');
    }

    async saveMemory() {
        const text = document.getElementById('memoryText').value.trim();

        if (!text && !this.currentPhoto && !this.currentAudio) {
            this.showToast('Please add some content to your memory');
            return;
        }

        const memory = {
            id: Date.now(),
            text: text,
            timestamp: new Date().toISOString(),
            photo: this.currentPhoto,
            audio: this.currentAudio,
            tags: this.extractTags(text)
        };

        this.memories.unshift(memory);
        this.saveMemories();
        this.showToast('Memory saved! 💭');
        this.cancelCapture();
        this.renderMemories();
    }

    // Photo Handling
    handlePhoto(event) {
        const file = event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            this.currentPhoto = e.target.result;
            this.showPhotoPreview(e.target.result);
        };
        reader.readAsDataURL(file);
    }

    showPhotoPreview(dataUrl) {
        const preview = document.getElementById('mediaPreview');
        preview.innerHTML = `
            <img src="${dataUrl}" alt="Memory photo">
            <button class="remove-media" onclick="app.removePhoto()">×</button>
        `;
        preview.classList.remove('hidden');
    }

    removePhoto() {
        this.currentPhoto = null;
        document.getElementById('mediaPreview').innerHTML = '';
        document.getElementById('mediaPreview').classList.add('hidden');
        document.getElementById('photoInput').value = '';
    }

    // Voice Recording
    async startVoiceRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.mediaRecorder = new MediaRecorder(stream);
            this.audioChunks = [];

            this.mediaRecorder.ondataavailable = (event) => {
                this.audioChunks.push(event.data);
            };

            this.mediaRecorder.onstop = () => {
                const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
                const reader = new FileReader();
                reader.onload = (e) => {
                    this.currentAudio = e.target.result;
                    this.showAudioPreview(e.target.result);
                };
                reader.readAsDataURL(audioBlob);

                // Try to transcribe
                this.transcribeAudio(audioBlob);
            };

            this.mediaRecorder.start();
            this.recordingStartTime = Date.now();
            this.showRecordingUI();

            // Update recording time
            this.recordingInterval = setInterval(() => {
                const elapsed = Math.floor((Date.now() - this.recordingStartTime) / 1000);
                const minutes = Math.floor(elapsed / 60);
                const seconds = elapsed % 60;
                document.getElementById('recordingTime').textContent =
                    `${minutes}:${seconds.toString().padStart(2, '0')}`;
            }, 1000);

        } catch (error) {
            this.showToast('Could not access microphone');
            console.error('Error accessing microphone:', error);
        }
    }

    stopVoiceRecording() {
        if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
            this.mediaRecorder.stop();
            this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
            clearInterval(this.recordingInterval);
            this.hideRecordingUI();
        }
    }

    showRecordingUI() {
        document.getElementById('voiceRecording').classList.remove('hidden');
        document.getElementById('voiceBtn').style.display = 'none';
    }

    hideRecordingUI() {
        document.getElementById('voiceRecording').classList.add('hidden');
        document.getElementById('voiceBtn').style.display = 'flex';
    }

    showAudioPreview(dataUrl) {
        const preview = document.getElementById('mediaPreview');
        preview.innerHTML = `
            <audio controls src="${dataUrl}"></audio>
            <button class="remove-media" onclick="app.removeAudio()">×</button>
        `;
        preview.classList.remove('hidden');
    }

    removeAudio() {
        this.currentAudio = null;
        const preview = document.getElementById('mediaPreview');
        if (!this.currentPhoto) {
            preview.innerHTML = '';
            preview.classList.add('hidden');
        } else {
            this.showPhotoPreview(this.currentPhoto);
        }
    }

    // Voice Transcription
    async transcribeAudio(audioBlob) {
        // Try Web Speech API for transcription
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            // Note: Real-time transcription would require different approach
            // For now, we'll skip auto-transcription and user can type
            this.showToast('Voice note saved! Add text description if needed.');
        }
    }

    // Auto-tagging
    extractTags(text) {
        if (!text) return [];

        const tags = new Set();
        const words = text.toLowerCase().split(/\s+/);

        // Common keywords
        const keywords = {
            people: ['mom', 'dad', 'family', 'friend', 'wife', 'husband', 'child', 'kids', 'son', 'daughter'],
            places: ['home', 'work', 'office', 'beach', 'park', 'restaurant', 'cafe', 'gym', 'school'],
            activities: ['work', 'meeting', 'lunch', 'dinner', 'workout', 'walk', 'run', 'travel', 'vacation'],
            emotions: ['happy', 'sad', 'excited', 'grateful', 'tired', 'stressed', 'relaxed', 'proud']
        };

        // Extract hashtags
        const hashtagMatches = text.match(/#\w+/g);
        if (hashtagMatches) {
            hashtagMatches.forEach(tag => tags.add(tag.toLowerCase()));
        }

        // Extract @mentions
        const mentionMatches = text.match(/@\w+/g);
        if (mentionMatches) {
            mentionMatches.forEach(mention => tags.add(mention.toLowerCase()));
        }

        // Match keywords
        Object.entries(keywords).forEach(([category, categoryWords]) => {
            categoryWords.forEach(keyword => {
                if (words.includes(keyword)) {
                    tags.add(`#${keyword}`);
                }
            });
        });

        // Capitalize names if found
        const names = text.match(/\b[A-Z][a-z]+\b/g);
        if (names) {
            names.forEach(name => {
                if (name.length > 2 && !['The', 'A', 'An', 'And'].includes(name)) {
                    tags.add(`@${name}`);
                }
            });
        }

        return Array.from(tags).slice(0, 10); // Limit to 10 tags
    }

    // Search and Filter
    handleSearch(query) {
        this.searchQuery = query.toLowerCase().trim();

        if (this.searchQuery) {
            document.getElementById('clearSearch').classList.remove('hidden');
        } else {
            document.getElementById('clearSearch').classList.add('hidden');
        }

        this.renderMemories();
    }

    clearSearch() {
        document.getElementById('searchInput').value = '';
        this.searchQuery = '';
        document.getElementById('clearSearch').classList.add('hidden');
        this.renderMemories();
    }

    setFilter(filter) {
        this.currentFilter = filter;
        document.querySelectorAll('.filter-tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.filter === filter);
        });
        this.renderMemories();
    }

    filterMemories() {
        let filtered = [...this.memories];

        // Apply search
        if (this.searchQuery) {
            filtered = filtered.filter(memory => {
                const textMatch = memory.text?.toLowerCase().includes(this.searchQuery);
                const tagMatch = memory.tags?.some(tag =>
                    tag.toLowerCase().includes(this.searchQuery)
                );
                return textMatch || tagMatch;
            });
        }

        // Apply time filter
        const now = new Date();
        if (this.currentFilter !== 'all') {
            filtered = filtered.filter(memory => {
                const memoryDate = new Date(memory.timestamp);
                const diffMs = now - memoryDate;
                const diffDays = diffMs / (1000 * 60 * 60 * 24);

                if (this.currentFilter === 'today') return diffDays < 1;
                if (this.currentFilter === 'week') return diffDays < 7;
                if (this.currentFilter === 'month') return diffDays < 30;
                return true;
            });
        }

        return filtered;
    }

    // Rendering
    renderMemories() {
        const filtered = this.filterMemories();
        const container = document.getElementById('memoriesList');
        const emptyState = document.getElementById('emptyState');

        if (filtered.length === 0) {
            container.innerHTML = '';
            emptyState.classList.remove('hidden');
            return;
        }

        emptyState.classList.add('hidden');

        container.innerHTML = filtered.map(memory => `
            <div class="memory-card" onclick="app.showMemoryDetail(${memory.id})">
                <div class="memory-date">${this.formatDate(memory.timestamp)}</div>
                ${memory.text ? `<div class="memory-text">${this.escapeHtml(memory.text)}</div>` : ''}
                ${memory.photo ? `<div class="memory-media"><img src="${memory.photo}" alt="Memory"></div>` : ''}
                ${memory.audio ? `<div class="memory-media">🎤 Voice note</div>` : ''}
                ${memory.tags && memory.tags.length > 0 ? `
                    <div class="memory-tags">
                        ${memory.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                    </div>
                ` : ''}
            </div>
        `).join('');
    }

    // Memory Detail
    showMemoryDetail(id) {
        const memory = this.memories.find(m => m.id === id);
        if (!memory) return;

        this.currentMemoryId = id;
        const content = document.getElementById('detailContent');

        content.innerHTML = `
            <div class="detail-date">${this.formatDate(memory.timestamp, true)}</div>
            ${memory.text ? `<div class="detail-text">${this.escapeHtml(memory.text)}</div>` : ''}
            ${memory.photo ? `<div class="memory-media"><img src="${memory.photo}" alt="Memory"></div>` : ''}
            ${memory.audio ? `<div class="memory-media"><audio controls src="${memory.audio}"></audio></div>` : ''}
            ${memory.tags && memory.tags.length > 0 ? `
                <div class="memory-tags">
                    ${memory.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>
            ` : ''}
        `;

        this.showView('detail');
    }

    closeDetail() {
        this.currentMemoryId = null;
        this.showView('timeline');
    }

    deleteCurrentMemory() {
        if (!this.currentMemoryId) return;

        if (confirm('Are you sure you want to delete this memory?')) {
            this.memories = this.memories.filter(m => m.id !== this.currentMemoryId);
            this.saveMemories();
            this.showToast('Memory deleted');
            this.closeDetail();
            this.renderMemories();
        }
    }

    // Special Features
    showRandomMemory() {
        this.hideMenu();

        if (this.memories.length === 0) {
            this.showToast('No memories yet!');
            return;
        }

        const randomIndex = Math.floor(Math.random() * this.memories.length);
        const memory = this.memories[randomIndex];
        this.showMemoryDetail(memory.id);
    }

    showStats() {
        this.hideMenu();

        const total = this.memories.length;
        const withPhotos = this.memories.filter(m => m.photo).length;
        const withVoice = this.memories.filter(m => m.audio).length;
        const allTags = this.memories.flatMap(m => m.tags || []);
        const uniqueTags = new Set(allTags);

        const oldest = this.memories.length > 0 ?
            new Date(this.memories[this.memories.length - 1].timestamp) : null;
        const daysSince = oldest ?
            Math.floor((new Date() - oldest) / (1000 * 60 * 60 * 24)) : 0;

        alert(`📊 Your Memory Stats\n\n` +
            `Total Memories: ${total}\n` +
            `With Photos: ${withPhotos}\n` +
            `With Voice: ${withVoice}\n` +
            `Unique Tags: ${uniqueTags.size}\n` +
            `Days Tracking: ${daysSince}`);
    }

    showAbout() {
        this.hideMenu();
        alert(`💭 Memory Catcher\n\n` +
            `Version 2.0\n\n` +
            `A simple, private way to capture and recall life's moments.\n\n` +
            `Features:\n` +
            `• Text, photo, and voice memories\n` +
            `• Auto-tagging\n` +
            `• Smart search\n` +
            `• Works offline\n` +
            `• Your data stays on your device\n\n` +
            `Made with ❤️`);
    }

    // Export
    exportMemories() {
        this.hideMenu();

        if (this.memories.length === 0) {
            this.showToast('No memories to export');
            return;
        }

        const exportData = {
            exportDate: new Date().toISOString(),
            totalMemories: this.memories.length,
            memories: this.memories
        };

        const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `memories-${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        URL.revokeObjectURL(url);

        this.showToast('Memories exported! 📤');
    }

    // Utility Functions
    formatDate(timestamp, full = false) {
        const date = new Date(timestamp);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);

        if (!full) {
            if (diffMins < 1) return 'Just now';
            if (diffMins < 60) return `${diffMins}m ago`;
            if (diffHours < 24) return `${diffHours}h ago`;
            if (diffDays < 7) return `${diffDays}d ago`;
        }

        return date.toLocaleString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML.replace(/\n/g, '<br>');
    }

    showToast(message) {
        const toast = document.getElementById('toast');
        toast.textContent = message;
        toast.classList.remove('hidden');
        toast.classList.add('show');

        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                toast.classList.add('hidden');
            }, 300);
        }, 3000);
    }

    // PWA Support
    registerServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('service-worker.js')
                .then(reg => console.log('Service Worker registered'))
                .catch(err => console.log('Service Worker registration failed'));
        }
    }

    checkInstallPrompt() {
        let deferredPrompt;

        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;

            // Show install button or prompt
            setTimeout(() => {
                if (confirm('Install Memory Catcher to your home screen?')) {
                    deferredPrompt.prompt();
                    deferredPrompt.userChoice.then((choiceResult) => {
                        if (choiceResult.outcome === 'accepted') {
                            console.log('User accepted install');
                        }
                        deferredPrompt = null;
                    });
                }
            }, 5000);
        });
    }
}

// Initialize app
const app = new MemoryCatcher();
