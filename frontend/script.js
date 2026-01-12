const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const fileInfo = document.getElementById('file-info');
const filenameSpan = document.getElementById('filename');
const convertBtn = document.getElementById('convert-btn');
const resetBtn = document.getElementById('reset-btn');
const loadingDiv = document.getElementById('loading');
const loadingText = document.getElementById('loading-text');
const resultSection = document.getElementById('result-section');
const audioPlayer = document.getElementById('audio-player');
const scriptContent = document.getElementById('script-content');
const newBtn = document.getElementById('new-btn');
const uploadSection = document.getElementById('upload-section');

let selectedFile = null;
const API_URL = 'http://localhost:8000';

// Event Listeners
dropZone.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', handleFileSelect);
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    if (e.dataTransfer.files.length) {
        handleFile(e.dataTransfer.files[0]);
    }
});

resetBtn.addEventListener('click', resetUI);
newBtn.addEventListener('click', resetUI);

convertBtn.addEventListener('click', uploadAndConvert);

function handleFileSelect(e) {
    if (e.target.files.length) {
        handleFile(e.target.files[0]);
    }
}

function handleFile(file) {
    if (!file.name.endsWith('.ppt') && !file.name.endsWith('.pptx')) {
        alert('Please upload a PPT or PPTX file.');
        return;
    }
    selectedFile = file;
    filenameSpan.textContent = file.name;
    dropZone.classList.add('hidden');
    fileInfo.classList.remove('hidden');
}

function resetUI() {
    selectedFile = null;
    fileInput.value = '';
    dropZone.classList.remove('hidden');
    fileInfo.classList.add('hidden');
    resultSection.classList.add('hidden');
    loadingDiv.classList.add('hidden');
    uploadSection.classList.remove('hidden');
    audioPlayer.src = '';
    scriptContent.textContent = '';
}

async function uploadAndConvert() {
    if (!selectedFile) return;

    // Show Loading
    uploadSection.classList.add('hidden');
    loadingDiv.classList.remove('hidden');
    loadingText.textContent = "Uploading & Extracting text...";

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        // Step 1: Upload & Extract & Generate (Server does it all)
        loadingText.textContent = "AI is writing the script & recording audio... (this may take a minute)";

        const response = await fetch(`${API_URL}/upload`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Conversion failed');
        }

        const data = await response.json();

        // Show Results
        loadingDiv.classList.add('hidden');
        resultSection.classList.remove('hidden');

        scriptContent.textContent = data.script;
        audioPlayer.src = data.audio_url;
        audioPlayer.play();

    } catch (error) {
        console.error(error);
        alert(`Error: ${error.message}`);
        resetUI();
    }
}
