// Agentic Notebook Generator - Frontend JavaScript

document.addEventListener('DOMContentLoaded', () => {
    initializeFileUpload();
    initializeForm();
    loadRecentNotebooks();
});

function initializeFileUpload() {
    const fileInput = document.getElementById('fileInput');
    const fileUploadDisplay = document.getElementById('fileUploadDisplay');
    
    fileUploadDisplay.addEventListener('click', () => fileInput.click());
    
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) displayFileInfo(file);
    });
    
    fileUploadDisplay.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileUploadDisplay.style.borderColor = 'var(--accent)';
    });
    
    fileUploadDisplay.addEventListener('drop', (e) => {
        e.preventDefault();
        const file = e.dataTransfer.files[0];
        if (file && file.name.endsWith('.csv')) {
            fileInput.files = e.dataTransfer.files;
            displayFileInfo(file);
        }
    });
}

function displayFileInfo(file) {
    const fileInfo = document.getElementById('fileInfo');
    const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
    fileInfo.innerHTML = `<strong>📄 ${file.name}</strong> (${sizeMB} MB)`;
    fileInfo.classList.add('show');
}

function initializeForm() {
    document.getElementById('uploadForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        await generateNotebook(new FormData(e.target));
    });
}

async function generateNotebook(formData) {
    const progressSection = document.getElementById('progressSection');
    const resultSection = document.getElementById('resultSection');
    const errorSection = document.getElementById('errorSection');
    const generateBtn = document.getElementById('generateBtn');
    
    resultSection.style.display = 'none';
    errorSection.style.display = 'none';
    progressSection.style.display = 'block';
    generateBtn.disabled = true;
    
    const steps = [
        { progress: 20, message: '📊 Analyzing dataset...' },
        { progress: 40, message: '🧠 Parsing intent...' },
        { progress: 60, message: '💻 Generating code...' },
        { progress: 80, message: '📓 Building notebook...' }
    ];
    
    let i = 0;
    const interval = setInterval(() => {
        if (i < steps.length) {
            document.getElementById('progressFill').style.width = steps[i].progress + '%';
            document.getElementById('progressStatus').textContent = steps[i].message;
            i++;
        }
    }, 800);
    
    try {
        const response = await fetch('/api/generate', { method: 'POST', body: formData });
        clearInterval(interval);
        
        if (!response.ok) throw new Error((await response.json()).detail);
        
        const result = await response.json();
        document.getElementById('progressFill').style.width = '100%';
        
        setTimeout(() => {
            progressSection.style.display = 'none';
            showSuccess(result);
            loadRecentNotebooks();
        }, 500);
    } catch (error) {
        clearInterval(interval);
        progressSection.style.display = 'none';
        showError(error.message);
    } finally {
        generateBtn.disabled = false;
    }
}

function showSuccess(result) {
    const resultSection = document.getElementById('resultSection');
    document.getElementById('resultMessage').innerHTML = 
        `Generated <strong>${result.sections_generated} sections</strong> in <strong>${result.notebook_filename}</strong>`;
    document.getElementById('downloadLink').href = result.download_url;
    resultSection.style.display = 'block';
}

function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('errorSection').style.display = 'block';
}

async function loadRecentNotebooks() {
    try {
        const response = await fetch('/api/notebooks');
        const data = await response.json();
        const list = document.getElementById('notebooksList');
        
        if (data.notebooks?.length > 0) {
            list.innerHTML = data.notebooks.slice(0, 5).map(nb => {
                const date = new Date(nb.created).toLocaleString();
                const size = (nb.size / (1024 * 1024)).toFixed(2);
                return `
                    <div class="notebook-item">
                        <div class="notebook-info">
                            <h4>📓 ${nb.filename}</h4>
                            <div class="notebook-meta">${date} • ${size} MB</div>
                        </div>
                        <a href="${nb.download_url}" class="btn-outline" download>⬇️ Download</a>
                    </div>`;
            }).join('');
        }
    } catch (error) {
        console.error('Failed to load notebooks:', error);
    }
}
