// Global variables
let currentScale = 1;
let offsetX = 0;
let offsetY = 0;
let isDragging = false;
let startX, startY;
let svgElement = null;

// DOM elements
const svgDisplay = document.getElementById('svg-display');
const fileInput = document.getElementById('file-input');
const statusDisplay = document.getElementById('status');
const zoomInBtn = document.getElementById('zoom-in');
const zoomOutBtn = document.getElementById('zoom-out');
// const resetViewBtn = document.getElementById('reset-view');
const svgContainer = document.getElementById('svg-container');

// Event listeners
fileInput.addEventListener('change', handleFileSelect);
zoomInBtn.addEventListener('click', () => zoom(1.2));
zoomOutBtn.addEventListener('click', () => zoom(0.8));
// resetViewBtn.addEventListener('click', resetView);

// Mouse events for panning
svgContainer.addEventListener('mousedown', startDrag);
document.addEventListener('mousemove', drag);
document.addEventListener('mouseup', endDrag);

// Touch events for mobile
svgContainer.addEventListener('touchstart', handleTouchStart);
svgContainer.addEventListener('touchmove', handleTouchMove);
svgContainer.addEventListener('touchend', handleTouchEnd);

// Handle file selection
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = function(e) {
    svgDisplay.innerHTML = e.target.result;
    svgElement = svgDisplay.querySelector('svg');
    
    if (svgElement) {
        statusDisplay.textContent = `✅ Loaded: ${file.name}`;
    } else {
        statusDisplay.textContent = '❌ Error: Not a valid SVG file';
    }
    };
    reader.readAsText(file);
}

// Zoom function
function zoom(scaleFactor) {
    currentScale *= scaleFactor;
    updateTransform();
}

// Reset view
function resetView() {
    currentScale = 1;
    offsetX = 0;
    offsetY = 0;
    updateTransform();
}

// Update SVG transform
function updateTransform() {
    svgDisplay.style.transform = `translate(${offsetX}px, ${offsetY}px) scale(${currentScale})`;
}

// Dragging functions
function startDrag(e) {
    if (!svgElement) return;
    isDragging = true;
    startX = e.clientX - offsetX;
    startY = e.clientY - offsetY;
    svgContainer.style.cursor = 'grabbing';
}

function drag(e) {
    if (!isDragging) return;
    offsetX = e.clientX - startX;
    offsetY = e.clientY - startY;
    updateTransform();
}

function endDrag() {
    isDragging = false;
    svgContainer.style.cursor = 'grab';
}

// Touch event handlers
function handleTouchStart(e) {
    if (!svgElement) return;
    if (e.touches.length === 1) {
    isDragging = true;
    startX = e.touches[0].clientX - offsetX;
    startY = e.touches[0].clientY - offsetY;
    }
    e.preventDefault();
}

function handleTouchMove(e) {
    if (!isDragging || e.touches.length !== 1) return;
    offsetX = e.touches[0].clientX - startX;
    offsetY = e.touches[0].clientY - startY;
    updateTransform();
    e.preventDefault();
}

function handleTouchEnd() {
    isDragging = false;
}

// Initialize
svgContainer.style.cursor = 'grab';